# 08 Concurrency and Asynchronous Programming

## Table of Contents

1. [Overview](#overview)
2. [Concurrency and Parallelism](#concurrency-and-parallelism)
3. [Shared State](#shared-state)
4. [Message Passing](#message-passing)
5. [Asynchronous Programming](#asynchronous-programming)
6. [Cancellation and Structured Lifetime](#cancellation-and-structured-lifetime)
7. [Design Guidelines](#design-guidelines)
8. [Concept Mapping](#concept-mapping)
9. [References](#references)

## Overview

Concurrent programs make progress on multiple tasks during overlapping periods. Parallel programs execute multiple computations at the same instant. A concurrent design may run on one thread, and multiple threads do not guarantee useful parallelism. The goal is coordinated work with clear ownership, ordering, failure, and shutdown rules.

## Concurrency and Parallelism

Use concurrency to manage independent activities, such as serving multiple connections while waiting for I/O. Use parallelism to reduce the elapsed time of CPU-bound work when the computation can be divided safely.

Creating more tasks than the system can support adds scheduling and synchronization overhead. Bound queues and worker counts so load produces backpressure instead of unbounded memory growth.

## Shared State

A **data race** occurs when concurrent execution accesses the same memory, at least one access writes, and the accesses lack the synchronization required by the language's memory model. Higher-level race conditions can occur even when every individual access is protected—for example, checking a balance and withdrawing in two separately locked operations.

### Rust

Rust prevents many data races through `Send`, `Sync`, ownership, and borrowing. Shared mutable state commonly combines `Arc<T>` with `Mutex<T>` or `RwLock<T>`.

~~~rust
use std::sync::{Arc, Mutex};
use std::thread;

let total = Arc::new(Mutex::new(0));
let worker_total = Arc::clone(&total);

let worker = thread::spawn(move || {
    *worker_total.lock().unwrap() += 1;
});

worker.join().unwrap();
~~~

The type system prevents unsynchronized shared mutation, but it cannot prevent deadlock or every logical race.

### Go

Goroutines are lightweight concurrent function executions. Shared state can be guarded by a mutex; the race detector helps discover executed data-race paths.

~~~go
var mu sync.Mutex
total := 0
var workers sync.WaitGroup

workers.Add(1)
go func() {
    defer workers.Done()
    mu.Lock()
    total++
    mu.Unlock()
}()
workers.Wait()
~~~

### Python

`threading` is useful for many I/O-bound tasks. Interpreter implementation details may limit CPU-bound parallel execution, so use processes or native/vectorized code where appropriate. A lock is still necessary for shared invariants; do not treat an implementation's global interpreter lock as application-level synchronization.

~~~python
from threading import Lock, Thread

lock = Lock()
total = 0

def increment() -> None:
    global total
    with lock:
        total += 1

worker = Thread(target=increment)
worker.start()
worker.join()
~~~

### C++

C++ threads share process memory. Access shared state with mutexes, atomics, or another synchronization design that establishes the required happens-before relationships.

~~~cpp
std::mutex mutex;
int total = 0;

std::jthread worker([&] {
    std::lock_guard lock(mutex);
    ++total;
});
~~~

Prefer RAII lock guards so a return or exception cannot leave a mutex locked.

## Message Passing

Message passing transfers values or requests between tasks and can reduce shared-state coupling.

Go channels combine communication with synchronization. Rust provides channels in its standard library and async ecosystems. Python offers queues for threads, processes, and asynchronous tasks. C++ has mutexes, condition variables, futures, and third-party channel abstractions rather than one standard channel type.

Channels do not automatically eliminate races: a message may contain a pointer or reference to data that remains shared. Define who owns a value after it is sent, whether order is guaranteed, and what closing the channel means.

## Asynchronous Programming

Asynchronous code lets a task yield while waiting instead of blocking an operating-system thread. A future, coroutine, or task represents work that may complete later. `await` suspends the current async task while allowing the runtime to execute other ready work.

- Rust uses `Future` and `async`/`await`, with an executor supplied by a library or framework.
- Go often expresses concurrent I/O directly with goroutines and blocking-looking calls managed by the runtime.
- Python's `asyncio` supplies an event loop, tasks, and async synchronization primitives.
- Modern C++ has language-level coroutines, but an application still needs library/runtime support for scheduling and I/O.

Do not call blocking I/O or perform long CPU-bound work directly on an event-loop thread. Move it to an appropriate worker pool or use an asynchronous API.

## Cancellation and Structured Lifetime

Cancellation is a normal outcome, not an exceptional afterthought. A task should stop at safe checkpoints, release resources, and communicate whether partial work occurred.

Prefer structured concurrency: child tasks should normally finish or be cancelled before their parent scope exits. Propagate deadlines and cancellation signals rather than creating detached background work with no owner. Go commonly uses `context.Context`; Python tasks propagate cancellation exceptions; Rust async libraries use cancellation tokens or dropping/selecting futures; C++20 provides cooperative stop tokens for compatible operations.

## Design Guidelines

- Minimize shared mutable state and protect invariants, not merely individual fields.
- Establish a consistent lock order and never hold a lock across slow or unknown code without a clear reason.
- Bound task creation, queues, and retries.
- Specify ordering, timeout, cancellation, and partial-failure behavior.
- Use race detectors, sanitizers, and stress tests; one successful run proves little about interleavings.
- Measure whether concurrency improves throughput or latency for the actual workload.

## Concept Mapping

| Purpose | Rust | Go | Python | C++ |
|---|---|---|---|---|
| OS-thread-style work | `std::thread` | runtime-managed goroutine | `threading.Thread` | `std::thread` / `std::jthread` |
| Mutual exclusion | `Mutex<T>` | `sync.Mutex` | `threading.Lock` / async lock | `std::mutex` |
| Message passing | channel libraries / `std::sync::mpsc` | channel | `queue` / `asyncio.Queue` | promise/future or library channel |
| Async task | executor task | goroutine | `asyncio.Task` | coroutine plus runtime/library |
| Cooperative cancellation | token or dropped future, ecosystem-dependent | `context.Context` | task cancellation | `std::stop_token` |

## References

- [The Rust Book — Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)
- [Go Memory Model](https://go.dev/ref/mem)
- [Python documentation — Concurrent Execution](https://docs.python.org/3/library/concurrency.html)
- [C++ working draft — Concurrency support library](https://eel.is/c++draft/thread)
