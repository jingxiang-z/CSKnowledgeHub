/*
 * thread_pool.c
 * 
 * A complete thread pool implementation with a work queue using POSIX threads.
 * This demonstrates the producer-consumer pattern for efficient task execution.
 * 
 * ARCHITECTURE:
 * - Fixed number of worker threads created at initialization
 * - FIFO task queue implemented as a linked list
 * - Threads wait on condition variable when queue is empty
 * - Tasks are enqueued by main thread, dequeued and executed by workers
 * - Graceful shutdown ensures all threads complete current tasks
 * 
 * SYNCHRONIZATION:
 * - Mutex (queue_mutex): Protects shared queue data structures
 * - Condition Variable (queue_not_empty): Signals workers when tasks available
 * - Condition Variable (queue_empty): Signals when all tasks completed
 * 
 * KEY FEATURES:
 * - Thread reuse (no overhead of creating/destroying per task)
 * - Lock held only during queue operations (tasks execute outside critical section)
 * - Safe shutdown with proper cleanup of resources
 * 
 * Compilation: gcc -o thread_pool thread_pool.c -pthread
 * Usage: ./thread_pool
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

/*
 * Task structure representing a unit of work.
 * Tasks are organized in a linked list (FIFO queue).
 */
typedef struct task {
    void (*function)(void*); // function pointer to the task to execute
    void* arg;               // argument to pass to the task function
    struct task* next;       // pointer to the next task in the queue
} task_t;

/*
 * Thread pool structure managing worker threads and task queue.
 * Uses producer-consumer pattern with condition variables for synchronization.
 */
typedef struct thread_pool {
    pthread_t *threads;              // array of worker threads
    task_t *task_queue_head;         // pointer to the head of the task queue (dequeue end)
    task_t *task_queue_tail;         // pointer to the tail of the task queue (enqueue end)

    pthread_mutex_t queue_mutex;     // mutex protecting shared queue data
    pthread_cond_t queue_not_empty;  // condition variable: signals when tasks are available
    pthread_cond_t queue_empty;      // condition variable: signals when queue becomes empty

    int thread_count;                // number of worker threads in the pool
    int task_count;                  // current number of pending tasks in the queue
    int shutdown;                    // flag to signal graceful shutdown (1 = shutting down)
} thread_pool_t;

/*
 * Worker thread function - the main loop for each thread in the pool.
 * Each worker continuously:
 * 1. Waits for tasks to become available
 * 2. Dequeues a task from the queue
 * 3. Executes the task
 * 4. Repeats until shutdown is signaled
 */
void *worker_thread(void *arg) {
    // Cast the argument back to thread_pool_t pointer
    thread_pool_t *pool = (thread_pool_t *) arg;
    task_t *task;
    
    while (1) {
        // Lock the mutex before accessing shared queue data
        pthread_mutex_lock(&pool->queue_mutex);

        // Wait while queue is empty AND not shutting down
        // pthread_cond_wait atomically releases mutex and waits
        // When signaled, it re-acquires the mutex before returning
        while (pool->task_count == 0 && !pool->shutdown) {
            pthread_cond_wait(&pool->queue_not_empty, &pool->queue_mutex);
        }

        // Exit condition: shutdown flag is set AND no tasks remain
        if (pool->shutdown && pool->task_count == 0) {
            pthread_mutex_unlock(&pool->queue_mutex);
            pthread_exit(NULL);
        }

        // Dequeue task from the head of the queue (FIFO)
        task = pool->task_queue_head;
        pool->task_queue_head = task->next;
        
        // If queue is now empty, update tail pointer
        if (pool->task_queue_head == NULL) {
            pool->task_queue_tail = NULL;
        }
        pool->task_count--;

        // Signal if queue just became empty (for thread_pool_wait)
        if (pool->task_count == 0) {
            pthread_cond_signal(&pool->queue_empty);
        }

        // Release lock before executing task (minimize lock contention)
        pthread_mutex_unlock(&pool->queue_mutex);

        // Execute the task outside the critical section
        task->function(task->arg);
        free(task);
    }

    return NULL;
}

/*
 * Creates and initializes a thread pool with the specified number of worker threads.
 * 
 * Parameters:
 *   num_threads - number of worker threads to create
 * 
 * Returns:
 *   Pointer to the created thread pool, or NULL on failure
 */
thread_pool_t *thread_pool_create(int num_threads) {
    // Allocate memory for the thread pool structure
    thread_pool_t *pool = (thread_pool_t *) malloc(sizeof(thread_pool_t));
    if (pool == NULL) {
        return NULL;
    }

    // Initialize pool fields
    pool->thread_count = num_threads;
    pool->task_count = 0;
    pool->shutdown = 0;
    pool->task_queue_head = NULL;
    pool->task_queue_tail = NULL;

    // Initialize synchronization primitives
    pthread_mutex_init(&pool->queue_mutex, NULL);
    pthread_cond_init(&pool->queue_not_empty, NULL);
    pthread_cond_init(&pool->queue_empty, NULL);

    // Allocate memory for thread handles
    pool->threads = (pthread_t *) malloc(num_threads * sizeof(pthread_t));
    if (pool->threads == NULL) {
        free(pool);
        return NULL;
    }

    // Create and start worker threads
    for (int i = 0; i < num_threads; i++) {
        if (pthread_create(&pool->threads[i], NULL, worker_thread, pool) != 0) {
            // If thread creation fails, clean up and return NULL
            pool->shutdown = 1;
            for (int j = 0; j < i; j++) {
                pthread_join(pool->threads[j], NULL);
            }
            free(pool->threads);
            free(pool);
            return NULL;
        }
    }

    return pool;
}

/*
 * Adds a new task to the thread pool's work queue.
 * 
 * Parameters:
 *   pool     - pointer to the thread pool
 *   function - function pointer to execute
 *   arg      - argument to pass to the function
 * 
 * Returns:
 *   0 on success, -1 on failure
 */
int thread_pool_add_task(thread_pool_t *pool, void (*function)(void*), void* arg) {
    // Validate input parameters
    if (pool == NULL || function == NULL) {
        return -1;
    }

    // Allocate and initialize a new task
    task_t *task = (task_t *) malloc(sizeof(task_t));
    if (task == NULL) {
        return -1;
    }
    task->function = function;
    task->arg = arg;
    task->next = NULL;

    // Enter critical section
    pthread_mutex_lock(&pool->queue_mutex);

    // Don't accept new tasks if pool is shutting down
    if (pool->shutdown) {
        pthread_mutex_unlock(&pool->queue_mutex);
        free(task);
        return -1;
    }

    // Add task to the tail of the queue (FIFO)
    if (pool->task_queue_head == NULL) {
        // Queue is empty - task becomes both head and tail
        pool->task_queue_head = task;
        pool->task_queue_tail = task;
    } else {
        // Queue has items - append to tail
        pool->task_queue_tail->next = task;
        pool->task_queue_tail = task;
    }

    pool->task_count++;

    // Signal one waiting worker thread that a task is available
    pthread_cond_signal(&pool->queue_not_empty);
    
    // Exit critical section
    pthread_mutex_unlock(&pool->queue_mutex);

    return 0;
}

/*
 * Waits for all tasks in the queue to be completed.
 * This is a blocking call that returns when task_count reaches 0.
 * 
 * Parameters:
 *   pool - pointer to the thread pool
 */
void thread_pool_wait(thread_pool_t *pool) {
    pthread_mutex_lock(&pool->queue_mutex);
    
    // Wait while there are still tasks in the queue
    // Note: This only waits for tasks to be dequeued, not for them to finish executing
    while (pool->task_count > 0) {
        pthread_cond_wait(&pool->queue_empty, &pool->queue_mutex);
    }
    
    pthread_mutex_unlock(&pool->queue_mutex);
}

/*
 * Destroys the thread pool and frees all associated resources.
 * This function:
 * 1. Signals all worker threads to shutdown
 * 2. Waits for all threads to complete
 * 3. Frees any remaining tasks in the queue
 * 4. Destroys synchronization primitives
 * 5. Frees all allocated memory
 * 
 * Parameters:
 *   pool - pointer to the thread pool to destroy
 */
void thread_pool_destroy(thread_pool_t *pool) {
    if (pool == NULL) {
        return;
    }

    // Set shutdown flag and wake all threads
    pthread_mutex_lock(&pool->queue_mutex);
    pool->shutdown = 1;
    
    // Broadcast to wake ALL waiting threads (not just one)
    pthread_cond_broadcast(&pool->queue_not_empty);
    pthread_mutex_unlock(&pool->queue_mutex);

    // Wait for all worker threads to finish and join them
    for (int i = 0; i < pool->thread_count; i++) {
        pthread_join(pool->threads[i], NULL);
    }

    // Free any remaining tasks in the queue
    while (pool->task_queue_head != NULL) {
        task_t *task = pool->task_queue_head;
        pool->task_queue_head = task->next;
        free(task);
    }

    // Destroy synchronization primitives
    pthread_mutex_destroy(&pool->queue_mutex);
    pthread_cond_destroy(&pool->queue_not_empty);
    pthread_cond_destroy(&pool->queue_empty);

    // Free allocated memory
    free(pool->threads);
    free(pool);
}

/*
 * Example task function that demonstrates how tasks are executed.
 * Each task prints its ID, sleeps for 1 second, then prints completion.
 * 
 * Note: This function is responsible for freeing the argument memory
 * since it was allocated in main().
 */
void task(void *arg) {
    int id = *(int *) arg;
    printf("Task %d executing on thread %p\n", id, (void *)pthread_self());
    
    // Simulate some work
    sleep(1);
    
    printf("Task %d completed\n", id);
    
    // Free the argument memory allocated in main
    free(arg);
}

/*
 * Main function demonstrating thread pool usage.
 * Creates a pool with 4 threads and submits 10 tasks for execution.
 */
int main() {
    printf("=== Thread Pool Example ===\n\n");
    
    // Create a thread pool with 4 worker threads
    printf("Creating thread pool with 4 worker threads...\n");
    thread_pool_t *pool = thread_pool_create(4);
    if (pool == NULL) {
        fprintf(stderr, "Failed to create thread pool\n");
        return 1;
    }
    printf("Thread pool created successfully\n\n");

    // Submit 10 tasks to the pool
    printf("Submitting 10 tasks to the pool...\n");
    for (int i = 0; i < 10; i++) {
        // Allocate memory for task argument
        // Note: task function is responsible for freeing this memory
        int *arg = (int *) malloc(sizeof(int));
        *arg = i;
        
        if (thread_pool_add_task(pool, task, arg) != 0) {
            fprintf(stderr, "Failed to add task %d\n", i);
            free(arg);
        }
    }
    printf("All tasks submitted\n\n");

    // Wait for all tasks to complete
    printf("Waiting for all tasks to complete...\n");
    thread_pool_wait(pool);
    
    // Give tasks time to finish executing (since wait only waits for dequeue)
    sleep(2);
    
    printf("\nAll tasks completed. Destroying thread pool...\n");
    thread_pool_destroy(pool);
    printf("Thread pool destroyed\n");
    
    printf("\n=== Program Complete ===\n");
    return 0;
}

