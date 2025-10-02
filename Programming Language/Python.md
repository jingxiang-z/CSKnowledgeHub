# Python

## Multithread

- **`threading` Module**: Python provides the `threading` module, a higher-level threading interface that includes classes and methods to create and manage threads, synchronize thread execution, and share data between threads.
- **Global Interpreter Lock (GIL)**: Python's GIL ensures that only one thread executes Python bytecode at a time, which simplifies memory management but can limit the performance of CPU-bound multithreaded programs. However, I/O-bound and certain concurrent operations can still benefit significantly.
- **Creating Threads**: Threads can be created by instantiating the `Thread` class with a target function and arguments. Threads are started with the `start()` method and wait for completion with the `join()` method.
- **Synchronization Primitives**: The `threading` module provides various synchronization primitives such as Locks, RLocks, Semaphores, Conditions, and Barriers to manage concurrent access to resources and coordinate thread execution.

### Thread Create

- **Creating a Thread:** To create a new thread, you instantiate a `Thread` object by providing the target callable and any arguments it needs:

```python
from threading import Thread

def my_function(arg1, arg2):
    print(f"Function running with arguments: {arg1}, {arg2}")

thread = Thread(target=my_function, args=("Hello", "World"))
```

- **Starting a Thread:** After creating a `Thread` object, you start it with the `start()` method. This invokes the target callable in a new, concurrent thread:

```python
thread.start()
```

- **Waiting for a Thread to Complete:** You can wait for a thread to finish its execution by calling its `join()` method. This is useful when the main program or other threads need to wait for the thread’s task to complete:

```python
thread.join()
```

- **Daemon Threads:** Threads can be made daemon threads by setting the `daemon` attribute to `True`. Daemon threads are automatically killed when the main program exits, and they do not prevent the program from exiting. They are useful for background tasks that should not block the program from ending:

```python
thread.daemon = True
```

Alternatively, you can set the `daemon` flag through the `Thread` constructor:

```python
thread = Thread(target=my_function, args=("Hello", "Daemon"), daemon=True)
```

- **`start()`**: Begin the thread’s execution.
- **`join(timeout=None)`**: Wait for the thread to finish. An optional `timeout` can be provided.
- **`is_alive()`**: Returns `True` if the thread is still running.
- **`name`**: You can get or set the name of the thread. This is useful for debugging.
- **`daemon`**: A boolean value that indicates whether the thread is a daemon thread.

### Thread Synchronization

- **Lock:** A `Lock` in Python's `threading` module is a synchronization primitive that is used to ensure that only one thread can execute a block of code or access a shared resource at a time.
  - **Acquire Lock:** Before accessing a shared resource, a thread must acquire the lock. If the lock is already held by another thread, the requesting thread will block until the lock becomes available.
  - **Release Lock:** After finishing with the shared resource, the thread must release the lock, allowing other threads to acquire it.
  - **With Statement:** Locks are typically used with the `with` statement in Python, which ensures that the lock is properly released, even if an exception occurs within the block.

```python
import threading

# A shared variable
counter = 0
# Create a lock
lock = threading.Lock()

# The target function for our threads
def increment_counter():
    global counter
    for _ in range(10000):
        # Acquire the lock before accessing the shared data
        # can also be used as follows
        # lock.acquire()
        # counter += 1
        # lock.release()
        with lock:
            counter += 1

# Create threads
threads = [threading.Thread(target=increment_counter) for _ in range(10)]

# Start threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print(f"Final counter value: {counter}")
```

- **Conditional Variable:** A threading Condition Variable is a synchronization primitive that allows threads to wait for certain conditions to be met before proceeding.
  - **Waiting for a Condition**: A thread that needs a certain condition to be true before it can proceed calls `wait()`, which releases the lock and blocks the thread until another thread calls `notify()` or `notify_all()`.
  - **Notifying about a Condition Change**: A thread that changes a condition in such a way that it might allow waiting threads to proceed calls `notify()` to wake up one waiting thread or `notify_all()` to wake up all waiting threads.

```python
import threading
import time

# Shared resource and condition variable
items = []
condition = threading.Condition()

# Producer thread class
class Producer(threading.Thread):
    def run(self):
        global items
        for i in range(5):
            with condition:  # Acquire the lock
                print(f"Producing item {i}")
                items.append(i)  # Add an item to the resource
                condition.notify()  # Notify the consumer that an item is available
                time.sleep(1)

# Consumer thread class
class Consumer(threading.Thread):
    def run(self):
        global items
        while True:
            with condition:  # Acquire the lock
                if not items:
                    condition.wait()  # Wait for an item to be produced
                item = items.pop(0)
                print(f"Consuming item {item}")
            time.sleep(2)

producer = Producer()
consumer = Consumer()

consumer.start()
producer.start()

producer.join()
consumer.join()

```

- **Semaphore:** a semaphore allows a fixed number of threads to access a shared resource simultaneously. This is useful in scenarios where you want to limit the number of concurrent accesses to a resource.
  - **Initialization**: `sem = threading.Semaphore(value=N)` where `N` is the initial number of permits. By default, `N` is 1.
  - **Acquiring a Permit**: `sem.acquire(blocking=True, timeout=None)` attempts to decrement the semaphore's counter, blocking until a permit is available unless `blocking` is set to `False`.
  - **Releasing a Permit**: `sem.release()` increments the semaphore's counter, potentially unblocking a waiting thread.

```python
import threading
import time
import random

# A semaphore to limit access to a resource
max_connections = 3
pool_semaphore = threading.Semaphore(max_connections)

def access_database(thread_id):
    print(f"Thread {thread_id} is waiting to access the database.")
    with pool_semaphore:
        # Simulate database access
        print(f"Thread {thread_id} has accessed the database.")
        time.sleep(random.uniform(0.5, 2.0))  # Simulate time taken for database operations
    print(f"Thread {thread_id} is done with the database.")

# Create multiple threads that need database access
threads = [threading.Thread(target=access_database, args=(i,)) for i in range(10)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All threads have completed their database operations.")

```

- **Barrier:** A threading Barrier is a synchronization primitive used to ensure that a fixed number of threads wait at a certain point in their execution until all of the threads have reached this point.
  - **Initialization**: `barrier = threading.Barrier(parties, action=None, timeout=None)` where `parties` is the number of threads that must call `wait()` for the barrier to trip, `action` is a callable to be executed by one of the threads when the barrier is tripped, and `timeout` is the default timeout for the `wait()` method.
  - **Waiting at the Barrier**: Each thread calls `barrier.wait(timeout=None)` to wait for the other threads. The call blocks until the specified number of threads have called `wait()`. Once the last thread calls `wait()`, all threads are simultaneously released.
  - **Resetting the Barrier**: The `reset()` method resets the barrier to its initial state. It can be used if you need to reuse the barrier.
  - **Aborting the Barrier**: The `abort()` method puts the barrier into a broken state. This causes all current and future calls to `wait()` to fail with a `BrokenBarrierError`, which can be useful for error handling.

```python
import threading
import time

# Define a barrier for 3 threads
barrier = threading.Barrier(3)

def phase1():
    print(f"Thread {threading.current_thread().name} is starting phase 1")
    time.sleep(1)  # Simulate work
    print(f"Thread {threading.current_thread().name} is waiting at the barrier")
    barrier.wait()  # Wait for other threads
    print(f"Thread {threading.current_thread().name} passed the barrier")

def phase2():
    print(f"Thread {threading.current_thread().name} is starting phase 2")
    time.sleep(1)  # Simulate work
    print(f"Thread {threading.current_thread().name} is waiting at the barrier")
    barrier.wait()  # Wait for other threads
    print(f"Thread {threading.current_thread().name} passed the barrier and is completing")

# Create threads for each phase
threads = [threading.Thread(target=phase1) for _ in range(3)] + [threading.Thread(target=phase2) for _ in range(3)]

# Start and join threads
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All threads have completed their work")

```

- **Event:** An event object manages an internal flag that can be set to true with the `set()` method and reset to false with the `clear()` method. Threads can wait for the flag to be set to true using the `wait()` method, which blocks until the flag becomes true.
  - **Set**: Marks the event as true. All threads waiting for it to become true are awakened.
  - **Clear**: Resets the event's state to false.
  - **Wait**: Blocks until the event's state becomes true. An optional timeout can be specified.

```python
import threading
import time

# Create the Event object
event = threading.Event()

def task():
    print("Task started. Doing some work.")
    time.sleep(2)  # Simulate a task taking some time
    print("Task completed. Notifying the main thread.")
    event.set()  # Signal that the task is done

# Create and start the worker thread
worker = threading.Thread(target=task)
worker.start()

# Main thread waiting for the task to complete
print("Main thread waiting for the task to complete.")
event.wait()  # Block until the event is set by the worker thread
print("Main thread notified. Continuing execution.")

# Optionally, you might want to join the thread
# to wait for it to complete before exiting the program.
worker.join()

```

