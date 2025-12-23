/*
 * producer_consumer.c
 * 
 * Demonstrates the producer-consumer pattern.
 * Producers create data and put it in a buffer.
 * Consumers take data from the buffer and process it.
 * 
 * Compilation: gcc -o producer_consumer producer_consumer.c -pthread
 * Usage: ./producer_consumer
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define BUFFER_SIZE 10
#define NUM_PRODUCERS 5
#define NUM_CONSUMERS 2
#define ITEMS_TO_PRODUCE 20

// Circular buffer implementation (FIFO queue)
int buffer[BUFFER_SIZE];
int count = 0;      // Number of items currently in buffer
int in = 0;         // Index where producer inserts (rear)
int out = 0;        // Index where consumer removes (front)

// Synchronization for buffer access
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;  // Signals consumers
pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;   // Signals producers

// Global counter for item generation (shared across producers)
int item_produce = 0;
pthread_mutex_t item_mutex = PTHREAD_MUTEX_INITIALIZER;

void *producer(void *arg) {
    int id = *(int *)arg;

    while(1) {
        // Check termination condition and generate unique item ID
        pthread_mutex_lock(&item_mutex);
        if(item_produce >= ITEMS_TO_PRODUCE) {
            pthread_mutex_unlock(&item_mutex);
            break;
        }
        int item = item_produce++;  // Each producer gets unique item number
        pthread_mutex_unlock(&item_mutex);

        // Simulate production time (outside critical section)
        usleep(rand() % 100000);

        // Enter critical section for buffer access
        pthread_mutex_lock(&mutex);

        // Wait while buffer is full
        while (count == BUFFER_SIZE) {
            printf("Producer %d: Buffer full (%d/%d), waiting...\n", id, count, BUFFER_SIZE);
            pthread_cond_wait(&not_full, &mutex);  // Releases mutex, waits, re-acquires
        }

        // Add item to circular buffer (enqueue)
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;  // Circular increment
        count++;

        printf("Producer %d: Produced item %d (buffer: %d/%d)\n", id, item, count, BUFFER_SIZE);

        pthread_cond_signal(&not_empty);  // Wake one waiting consumer

        pthread_mutex_unlock(&mutex);
    }
    printf("Producer %d: Finished (produced %d items)\n", id, ITEMS_TO_PRODUCE);
    return NULL;
}

void *consumer(void * arg) {
    int id = *(int *)arg;
    int consumed_count = 0;

    while(1) {
        // Enter critical section for buffer access
        pthread_mutex_lock(&mutex);

        // Wait while buffer is empty
        while (count == 0) {
            // Check if production is complete
            pthread_mutex_lock(&item_mutex);
            int all_produced = (item_produce >= ITEMS_TO_PRODUCE);
            pthread_mutex_unlock(&item_mutex);

            // Exit if no more items will be produced
            if (all_produced) {
                pthread_mutex_unlock(&mutex);
                printf("Consumer %d: Finished (consumed %d items)\n", id, consumed_count);
                return NULL;
            }

            printf("Consumer %d: Buffer empty (%d/%d), waiting...\n", id, count, BUFFER_SIZE);
            pthread_cond_wait(&not_empty, &mutex);  // Releases mutex, waits, re-acquires
        }

        // Remove item from circular buffer (dequeue)
        int item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;  // Circular increment
        count--;
        consumed_count++;

        printf("Consumer %d: Consumed item %d (buffer: %d/%d)\n", id, item, count, BUFFER_SIZE);

        pthread_cond_signal(&not_full);  // Wake one waiting producer

        pthread_mutex_unlock(&mutex);

        // Simulate consumption time (outside critical section)
        usleep(rand() % 10000);
    }
    return NULL;
}


int main() {
    pthread_t producers[NUM_PRODUCERS];
    pthread_t consumers[NUM_CONSUMERS];
    int producer_ids[NUM_PRODUCERS];
    int consumer_ids[NUM_CONSUMERS];

    printf("=== Producer-Consumer Simulation ===\n");
    printf("Buffer size: %d\n", BUFFER_SIZE);
    printf("Producers: %d, Consumers: %d\n", NUM_PRODUCERS, NUM_CONSUMERS);
    printf("Items to produce: %d\n", ITEMS_TO_PRODUCE);
    printf("====================================\n\n");

    srand(time(NULL));

    // Create producer threads
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        producer_ids[i] = i + 1;
        if (pthread_create(&producers[i], NULL, producer, &producer_ids[i])) {
            perror("Failed to create producer thread");
            exit(1);
        }
    }

    // Create consumer threads
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        consumer_ids[i] = i + 1;
        if (pthread_create(&consumers[i], NULL, consumer, &consumer_ids[i])) {
            perror("Failed to create consumer thread");
            exit(1);
        }
    }

    // Wait for all producers to finish
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        pthread_join(producers[i], NULL);
    }

    // Wake all consumers so they can check termination condition
    pthread_cond_broadcast(&not_empty);

    // Wait for all consumers to finish
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        pthread_join(consumers[i], NULL);
    }

    printf("\n====================================\n");
    printf("All threads completed successfully!\n");
    printf("====================================\n");

    // Cleanup synchronization primitives
    pthread_mutex_destroy(&mutex);
    pthread_mutex_destroy(&item_mutex);
    pthread_cond_destroy(&not_full);
    pthread_cond_destroy(&not_empty);
    
    return 0;
}

