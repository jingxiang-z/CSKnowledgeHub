# 02 Process and Thread Management

## Table of Contents

1. [Overview](#overview)
2. [Process Fundamentals](#process-fundamentals)
3. [Thread Fundamentals](#thread-fundamentals)
4. [Process vs Thread Comparison](#process-vs-thread-comparison)
5. [Multithreading Models](#multithreading-models)
6. [Scheduling](#scheduling)
7. [Inter-Process Communication](#inter-process-communication)
8. [Signals and Interrupts](#signals-and-interrupts)
9. [Design Patterns](#design-patterns)
10. [Performance](#performance)
11. [Related Topics](#related-topics)
12. [References](#references)

## Overview

Process and thread management are fundamental responsibilities of modern operating systems. A **process** represents an independent program execution unit with its own memory space and resources, while a **thread** is a lightweight execution unit within a process that shares the process's memory space with other threads.

### Key Concepts

**Process:**
- Independent execution unit representing a running program
- Contains program code, data, heap, stack, and system resources
- Isolated memory space provides protection between processes
- Managed through Process Control Block (PCB) or Task Control Block (TCB)
- Heavy-weight: significant overhead for creation and context switching

**Thread:**
- Smallest unit of execution within a process
- Shares process memory space, code, data, and heap with other threads
- Has its own stack, registers, and program counter
- Light-weight: minimal overhead for creation and context switching
- Enables concurrent execution within a single process

### Why Both Exist

**Processes provide:**
- Strong isolation and fault tolerance
- Security boundaries between different applications
- Resource management at the application level
- Protection from bugs in other processes

**Threads provide:**
- Efficient parallelism within an application
- Shared memory communication without IPC overhead
- Responsive user interfaces (UI thread + worker threads)
- Better resource utilization on multi-core systems

## Process Fundamentals

An operating system process is a fundamental concept where each program's execution is represented as an independent unit. Processes allow the operating system to manage and execute multiple tasks concurrently, ensuring efficient resource use and isolation of programs from one another.

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Process Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Process Control Block (PCB)                 │  │
│  │  • Process ID (PID)                                   │  │
│  │  • Process State (Running/Ready/Blocked)              │  │
│  │  • Program Counter                                    │  │
│  │  • CPU Registers                                      │  │
│  │  • Memory Management Info                             │  │
│  │  • I/O Status                                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Memory Layout                            │  │
│  │                                                       │  │
│  │  High Address                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │            Stack (grows down ↓)                 │  │  │
│  │  │  • Local variables                              │  │  │
│  │  │  • Function parameters                          │  │  │
│  │  │  • Return addresses                             │  │  │
│  │  ├─────────────────────────────────────────────────┤  │  │
│  │  │                     ↕                           │  │  │
│  │  │              (Free Space)                       │  │  │
│  │  │                     ↕                           │  │  │
│  │  ├─────────────────────────────────────────────────┤  │  │
│  │  │            Heap (grows up ↑)                    │  │  │
│  │  │  • Dynamic allocations (malloc/new)             │  │  │
│  │  ├─────────────────────────────────────────────────┤  │  │
│  │  │            Data Section                         │  │  │
│  │  │  • Global variables                             │  │  │
│  │  │  • Static variables                             │  │  │
│  │  ├─────────────────────────────────────────────────┤  │  │
│  │  │            Code (Text) Section                  │  │  │
│  │  │  • Program instructions                         │  │  │
│  │  │  • Read-only                                    │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  Low Address                                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              File Descriptors                         │  │
│  │  • stdin (0), stdout (1), stderr (2)                  │  │
│  │  • Open files and I/O streams                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Components of a Process:**

1. **Program Code:** The executable code that the CPU executes
2. **Process Control Block (PCB):** Data structure storing process information
3. **Process State:** Current state (running, ready, blocked, or terminated)
4. **Program Counter (PC):** Keeps track of the next instruction
5. **CPU Registers:** Store data and control process execution
6. **Stack:** For local variables and function call management
7. **Data Section:** Global and static variables
8. **Heap:** For dynamic memory allocation
9. **File Descriptors:** Access to files and I/O devices
10. **Parent-Child Relationship:** Process hierarchy
11. **Inter-Process Communication (IPC):** Channels for communication
12. **Signal Handlers:** Registered signals and associated handlers
13. **Resource Usage:** CPU time, memory, and other resource consumption

### Process Control Block (PCB)

A process is represented using a **Process Control Block (PCB)** or **Task Control Block (TCB)**, which is a data structure containing all information about a process.

**PCB Contents:**
- Process state (running, ready, blocked, etc.)
- Program counter and CPU registers
- Stack pointer
- Memory management information (page tables, segment tables)
- Priority and scheduling information
- Program code and data pointers
- I/O status information
- File descriptor table
- Accounting information (CPU time used, time limits)

**PCB Operations:**
- Stored in the kernel of the operating system
- During context switch, current process state saved to its PCB
- Next process state loaded from its PCB
- Enables efficient process management and multitasking

### Stack and Heap

The stack and heap are two distinct regions within a process's address space serving different purposes.

#### Stack

**Purpose:** Management of function call frames, including parameter passing, return addresses, and local variables. It is a last-in, first-out (LIFO) data structure.

**Characteristics:**
- Fixed-size: Typically determined during process creation
- Fast access: Simple pointer manipulation
- Automatic allocation/deallocation: Implicit as functions are called and return
- Limited lifetime: Variables tied to function scope
- Thread-specific: Each thread has its own stack
- Grows downward (typically) from high memory addresses

**Use Cases:**
- Local variables
- Function parameters
- Return addresses
- Function call frames

#### Heap

**Purpose:** Dynamic memory allocation where data can be allocated and deallocated at runtime. Suitable for data structures with non-deterministic lifetime.

**Characteristics:**

- Variable size: Can grow or shrink during program execution
- Slower access: Involves memory management overhead
- Explicit allocation/deallocation: Programmer manages (malloc/free, new/delete)
- Longer lifetime: Variables persist across function calls
- Shared among threads: All threads in a process share the heap
- Grows upward (typically) from low memory addresses

**Use Cases:**
- Dynamic data structures (linked lists, trees)
- Large objects
- Objects with lifetime beyond function scope
- Shared data between threads

**Key Differences:**

| Aspect | Stack | Heap |
|--------|-------|------|
| **Usage** | Function call management | Dynamic memory allocation |
| **Allocation** | Automatic (implicit) | Explicit (programmer-managed) |
| **Lifetime** | Function scope | Arbitrary (programmer-controlled) |
| **Speed** | Fast (pointer manipulation) | Slower (memory management) |
| **Scope** | Thread-specific | Process-wide (shared) |
| **Size** | Fixed at creation | Variable during execution |
| **Fragmentation** | None | Can occur over time |
| **Management** | OS/compiler automatic | Programmer responsibility |

### Process Lifecycle

![image-20260108213943040](C:\Users\78649\CSKnowledgeHub\assets\os-process-lifecycle.png)

The process lifecycle refers to the various states and transitions that a process goes through during its existence. These states are managed by the operating system's process scheduler.

#### States

**1. New:**
The process is being created by the operating system but has not yet started executing. Resources such as memory and data structures are being allocated.

**2. Ready:**
The process is prepared to run but the CPU is currently allocated to another process. It waits in a ready queue to be executed when the CPU becomes available.

**3. Running:**
The process is currently being executed by the CPU. It is the active state where the program's instructions are being executed.

**4. Blocked (or Waiting):**
The process needs to wait for some event or resource to become available (e.g., user input, I/O completion). While blocked, the process does not consume CPU time.

**5. Terminated (or Exit):**
The process has finished execution (successfully or due to error) and is being terminated. Resources are released and the process is removed from the system.

#### Transitions

- **New → Ready:** Process creation completes, ready to run
- **Ready → Running:** CPU becomes available, scheduler selects process
- **Running → Ready:** Time quantum expires (preemption) or voluntary yield
- **Running → Blocked:** Process waits for I/O or event
- **Blocked → Ready:** I/O completes or event occurs
- **Running → Terminated:** Process completes or is killed

The lifecycle is dynamic, with processes moving between states based on scheduling policies, external events, and program logic. Understanding and managing this lifecycle is crucial for efficient resource utilization and multitasking.

### Process Categories

#### I/O-Bound Process

An I/O-bound process spends significant execution time performing input/output operations such as disk reads/writes, network communication, or user interaction.

**Characteristics:**
- Frequently pauses execution waiting for I/O
- Spends more time in blocked state than using CPU
- Short CPU bursts between I/O operations
- Benefits from higher scheduling priority for responsiveness

**Examples:**
- Web servers handling client requests
- Database servers with frequent disk access
- Interactive applications waiting for user input
- Text editors, IDEs

#### CPU-Bound Process

A CPU-bound process primarily requires CPU resources for computation and data processing, characterized by long and intense computations.

**Characteristics:**
- Keeps CPU busy for extended periods
- Minimal time waiting for I/O operations
- Long CPU bursts
- Benefits from longer time quantums

**Examples:**
- Mathematical simulations
- Video encoding and rendering
- Scientific calculations
- Cryptographic operations
- Machine learning training

**Scheduling Implications:**

Different strategies are employed to handle these process types effectively:
- I/O-bound: Priority and responsiveness to I/O operations are vital
- CPU-bound: Fair distribution of CPU time and optimization of computational resources are key

## Thread Fundamentals

Threads are the smallest unit of execution within a process, enabling concurrent and parallel programming within a single application.

### Basic Concepts

**1. Thread:**
An independent sequence of instructions that can be scheduled and run by the operating system's thread scheduler. A process can contain multiple threads executing concurrently and sharing the same process resources.

**2. Multithreading:**
A technique where a program is divided into multiple threads that execute independently but share the same memory space, allowing concurrent execution of tasks within the same process.

**3. Concurrency:**
Multiple tasks being executed in overlapping time periods, not necessarily simultaneously. Threads enable concurrency by allowing multiple tasks to make progress independently.

**4. Parallelism:**
Multiple tasks executing at the same time, often on multiple CPU cores or processors. Threads can achieve parallelism, but not all multithreaded programs are inherently parallel.

**5. Thread Safety:**
Code that behaves correctly and reliably when accessed by multiple threads simultaneously. Thread-safe code avoids data races and conflicts that occur in multithreaded environments.

**6. Context Switching:**
The process of saving the state of a running thread, loading the state of another thread, and switching between them. Essential for the thread scheduler but incurs overhead.

**7. Thread Priority:**
Many operating systems allow threads to have different priorities affecting scheduling order. Higher-priority threads receive preference from the scheduler.

**8. Thread Lifecycle:**
Threads have a lifecycle including creation, running, and termination. They can be created, started, paused, resumed, and eventually terminated.

### Thread Components

Each thread within a process has:

**Thread-Specific:**
- Thread ID (TID)
- Program Counter (PC)
- Register set
- Stack (for local variables and function calls)
- Thread-local storage
- State (running, ready, blocked, terminated)

**Shared with Process:**
- Code section (program instructions)
- Data section (global and static variables)
- Heap (dynamically allocated memory)
- Open file descriptors
- Signal handlers
- Process ID (PID)

### Advantages of Threads

**1. Resource Sharing:**
Threads share memory and resources of the process, making communication efficient without explicit IPC mechanisms.

**2. Responsiveness:**
Multithreaded applications remain responsive; one thread can continue execution while others are blocked.

**3. Economy:**
Thread creation and context switching are less expensive than process operations.

**4. Scalability:**
Multithreaded programs can leverage multi-core processors for true parallelism.

**5. Modularity:**
Different aspects of a program can be separated into threads (e.g., UI thread, worker threads, I/O threads).

### Challenges with Threads

**1. Race Conditions:**
Multiple threads accessing shared data simultaneously can lead to unpredictable results.

**2. Deadlock:**
Two or more threads permanently blocked, each waiting for resources held by others.

**3. Complexity:**
Designing, debugging, and testing multithreaded programs is more complex than single-threaded alternatives.

**4. Synchronization Overhead:**
Coordinating threads through locks and other mechanisms adds overhead.

## Process vs Thread Comparison

| Aspect | Process | Thread |
|--------|---------|--------|
| **Definition** | Independent program execution unit | Execution unit within a process |
| **Memory Space** | Separate address space | Shares process address space |
| **Communication** | IPC mechanisms (pipes, sockets, shared memory) | Direct memory access (shared variables) |
| **Creation Overhead** | High (heavy-weight) | Low (light-weight) |
| **Context Switch** | Expensive (full context) | Cheap (minimal context) |
| **Isolation** | Strong (protected from other processes) | Weak (shared memory with other threads) |
| **Resource Usage** | Each has own resources | Share process resources |
| **Fault Tolerance** | Crash doesn't affect other processes | Crash can bring down entire process |
| **Synchronization** | Not required between processes | Required for shared data access |
| **Use Case** | Independent applications | Parallel tasks within application |
| **Examples** | Browser, text editor, compiler | UI thread, worker thread, I/O thread |

## Multithreading Models

Multithreading models define the relationship between user-level threads (managed by libraries) and kernel-level threads (managed by the OS).

### Many-to-One Model (User-Level Threads)

Multiple user-level threads (ULTs) map to a single kernel-level thread (KLT).

**Characteristics:**
- ULTs managed entirely by user-level thread library
- OS kernel unaware of ULTs
- Thread management (creation, scheduling, synchronization) in user space
- Fast thread operations (no kernel involvement)

**Advantages:**
- Low overhead for thread operations
- Flexible scheduling policies
- Portable across operating systems
- High degree of control for programmer

**Disadvantages:**
- Cannot exploit multi-core processors (all ULTs share one KLT)
- Blocking system call blocks entire process
- No true parallelism
- Poor scalability

**Use Cases:**
- I/O-bound applications with many threads
- Fine-grained parallelism scenarios
- Legacy systems

**Examples:**
- Green threads (older Java implementations)
- User-level threading libraries

### One-to-One Model (Kernel-Level Threads)

Each user-level thread corresponds to a separate kernel-level thread.

**Characteristics:**
- Each ULT has its own KLT
- OS kernel manages all threads
- True parallelism across multiple cores
- System calls by one thread don't block others

**Advantages:**
- True parallelism on multi-core systems
- Better concurrency
- Blocking call doesn't block entire process
- Well-suited for compute-bound tasks

**Disadvantages:**
- Higher overhead (kernel involvement for all operations)
- Thread creation is expensive
- Limited scalability (kernel thread limit)
- Context switching overhead

**Use Cases:**
- Compute-bound applications
- Applications requiring parallelism across cores
- Modern general-purpose systems

**Examples:**
- Windows threads
- Linux threads (NPTL - Native POSIX Thread Library)
- Modern threading libraries

### Many-to-Many Model (Hybrid)

Multiple user-level threads map to smaller or equal number of kernel-level threads.

**Characteristics:**
- Combines advantages of both models
- Typically one KLT per processor core
- ULTs managed by user-level libraries
- KLTs managed by operating system
- Dynamic mapping between ULTs and KLTs

**Advantages:**
- Balances control and performance
- True parallelism with low overhead
- Can create many ULTs without kernel thread limit
- Flexible scheduling
- Blocking call doesn't block all threads

**Disadvantages:**
- Complex implementation
- Requires coordination between user and kernel schedulers
- Potential scheduling conflicts

**Use Cases:**
- Applications with variable thread counts
- Systems requiring both performance and flexibility
- Server applications with many concurrent tasks

**Examples:**
- Solaris (older versions)
- Some modern runtime systems (Go, Erlang)

### Model Selection

The choice of multithreading model depends on:
- Application characteristics (I/O-bound vs. CPU-bound)
- Target platform capabilities
- Performance requirements
- Scalability needs
- Development complexity constraints

Modern systems often use the one-to-one model due to improvements in kernel efficiency and the prevalence of multi-core processors. Some runtime environments implement many-to-many models in user space for specialized workloads.

## Scheduling

Scheduling determines the order in which processes and threads execute on the CPU, balancing fairness, responsiveness, and resource utilization.

### Context Switch

A context switch is the process by which an operating system saves the state of a running process/thread and restores the state of another to share a single CPU among multiple execution units.

**Context Switch Process:**

1. **Interrupt Handling:**
   - Timer interrupt (time quantum expires)
   - Hardware interrupt (I/O completion)
   - Software interrupt (system call)

2. **Save Current Context:**
   - CPU switches from user mode to kernel mode
   - Interrupt service routine (ISR) executes
   - Current process/thread context saved to PCB/TCB:
     - Program counter
     - Register values
     - CPU state information

3. **Choose New Process/Thread:**
   - Scheduler selects next process/thread from ready queue
   - Selection based on scheduling algorithm (Round Robin, Priority, etc.)
   - Considers priority and other criteria

4. **Load New Context:**
   - Saved state of selected process/thread loaded from PCB/TCB
   - Program counter, registers, and CPU state restored
   - CPU switches back to user mode

5. **Resume Execution:**
   - CPU resumes execution of new process/thread
   - Execution continues from where it was last interrupted

**Context Switch Overhead:**

- Direct costs: Saving/loading registers, updating data structures
- Indirect costs: Cache misses, TLB flushes, pipeline stalls
- Time varies from microseconds to milliseconds

Efficient context switching is performance-critical, affecting system responsiveness and resource utilization. Operating systems minimize this overhead through optimization techniques.

### Scheduling Algorithms

Scheduling algorithms determine which process or thread runs next, each with distinct characteristics suited to different scenarios.

#### First-Come, First-Served (FCFS)

**Overview:**
The simplest scheduling algorithm where processes execute in the order they arrive in the ready queue.

**Characteristics:**
- Non-preemptive
- FIFO queue implementation
- Simple to implement

**Advantages:**
- Fair in arrival order
- No starvation
- Low overhead

**Disadvantages:**

- High variance in response time
- Convoy effect (short processes wait for long ones)
- Poor for interactive systems

**Application Scenario:**
Batch processing systems where arrival order is significant and execution times are unpredictable.

#### Shortest Job Next (SJN) / Shortest Job First (SJF)

**Overview:**
Schedules processes based on expected burst times, with shortest job executed first.

**Characteristics:**
- Can be preemptive (SRTF - Shortest Remaining Time First) or non-preemptive
- Requires knowledge of burst times
- Optimal for minimizing average waiting time

**Advantages:**
- Minimizes average waiting time
- Optimal when burst times known

**Disadvantages:**
- Burst times often unknown in advance
- Can cause starvation for long processes
- Impractical for most interactive systems

**Application Scenario:**
Environments where job lengths are known (batch systems) or can be accurately estimated.

#### Round Robin (RR)

**Overview:**
Each process receives a fixed time quantum (time slice). When the time slice expires, the process moves to the end of the ready queue.

**Characteristics:**
- Preemptive
- Time quantum typically 10-100ms
- Circular queue of ready processes

**Advantages:**
- Fair CPU time allocation
- Good response time for interactive systems
- No starvation
- Prevents process monopolization

**Disadvantages:**
- Performance depends on time quantum size
- Higher context switch overhead
- Not optimal for batch processing

**Application Scenario:**
Time-sharing systems, interactive environments, and ensuring fair CPU allocation. Ideal for preventing any single process from monopolizing CPU.

#### Priority Scheduling

**Overview:**
Each process assigned a priority level; highest priority process executes first.

**Characteristics:**
- Can be preemptive or non-preemptive
- Priorities can be static or dynamic
- May use priority queues

**Advantages:**
- Important tasks execute promptly
- Flexible (can implement various policies)
- Good for real-time systems

**Disadvantages:**
- Can cause starvation for low-priority processes
- Priority inversion possible
- Requires careful priority assignment

**Solutions to Starvation:**
- Aging: Gradually increase priority of waiting processes
- Dynamic priority adjustment

**Application Scenario:**
Real-time systems and environments where critical tasks must execute promptly. Effective when processes have varying importance levels.

#### Multilevel Queue Scheduling

**Overview:**
Processes categorized into multiple queues based on priority or other attributes. Each queue can use its own scheduling algorithm.

**Characteristics:**
- Multiple queues with different priorities
- Processes assigned to queues based on attributes
- Each queue has its own scheduling algorithm
- Fixed priority between queues

**Advantages:**
- Different process types managed separately
- Flexible (different algorithms per queue)
- Can prioritize certain process types

**Disadvantages:**
- Processes cannot move between queues
- Potential starvation for low-priority queues
- Complex configuration

**Application Scenario:**
Scenarios where different process classes need separate management (e.g., system processes, interactive processes, batch processes).

#### Multilevel Feedback Queue Scheduling

**Overview:**
Similar to multilevel queue scheduling, but processes can move between queues based on their behavior and characteristics.

**Characteristics:**
- Multiple queues with different priorities
- Processes can change queues dynamically
- Typically uses Round Robin within queues
- Aging mechanism to prevent starvation

**Advantages:**
- Adapts to changing workload
- Prevents starvation through aging
- Rewards short jobs
- Flexible and responsive

**Disadvantages:**
- Complex implementation
- Requires tuning of parameters
- Higher overhead

**Application Scenario:**
Dynamic environments with varying workload characteristics. Common in modern general-purpose operating systems (Linux, Windows).

### Scheduling Goals

Different systems optimize for different metrics:

| Goal | Description | Important For |
|------|-------------|---------------|
| **CPU Utilization** | Keep CPU busy | All systems |
| **Throughput** | Processes completed per unit time | Batch systems |
| **Turnaround Time** | Time from submission to completion | Batch systems |
| **Waiting Time** | Time spent in ready queue | Interactive systems |
| **Response Time** | Time from request to first response | Interactive systems |
| **Fairness** | All processes get fair CPU time | General-purpose systems |
| **Predictability** | Consistent performance | Real-time systems |

## Inter-Process Communication

Inter-process communication (IPC) encompasses mechanisms for processes to communicate and share data. Common IPC methods include pipes, message queues, shared memory, sockets, and remote procedure calls.

### IPC Methods Overview

| Method | Description | Use Case |
|--------|-------------|----------|
| **Pipes** | One-way communication between related processes | Parent-child communication |
| **Named Pipes (FIFOs)** | Named file system entry for unrelated processes | Unrelated process communication |
| **Message Queues** | Structured asynchronous message passing | Reliable inter-process data exchange |
| **Shared Memory** | Common memory region accessible to processes | High-speed data sharing |
| **Sockets** | Network-based communication | Local or network communication |
| **Signals** | Asynchronous event notification | Process control and notification |
| **Semaphores** | Synchronization primitive | Resource access control |
| **File-based IPC** | Communication through files | Simple data sharing and persistence |
| **RPC** | Remote procedure call mechanism | Distributed systems, client-server |

### Message Queues

Message queues provide structured, asynchronous message passing between processes with reliable delivery.

**Characteristics:**
- Messages stored in kernel queue
- FIFO or priority-based ordering
- Asynchronous communication
- Persistent until read

**POSIX Message Queue Example:**

```c
#include <mqueue.h>

#define QUEUE_NAME "/my_message_queue"
#define MAX_MSG_SIZE 100

int main() {
    mqd_t mq;
    struct mq_attr attr;
    char message[MAX_MSG_SIZE];
    
    // Define message queue attributes
    attr.mq_flags = 0;
    attr.mq_maxmsg = 10;
    attr.mq_msgsize = MAX_MSG_SIZE;
    
    // Create or open the message queue
    mq = mq_open(QUEUE_NAME, O_CREAT | O_RDWR, 0666, &attr);
    if (mq == (mqd_t)-1) {
        perror("mq_open");
        exit(1);
    }
    
    // Send a message
    strcpy(message, "Hello from Process 1!");
    if (mq_send(mq, message, strlen(message), 0) == -1) {
        perror("mq_send");
        exit(1);
    }
    printf("Message sent: %s\n", message);
    
    // Receive a message
    unsigned int prio;
    ssize_t msg_len = mq_receive(mq, message, MAX_MSG_SIZE, &prio);
    if (msg_len == -1) {
        perror("mq_receive");
        exit(1);
    }
    message[msg_len] = '\0';
    printf("Received message: %s\n", message);
    
    // Close and optionally unlink the queue
    mq_close(mq);
    // mq_unlink(QUEUE_NAME);  // Remove queue
    
    return 0;
}
```

### Shared Memory

Shared memory allows multiple processes to access a common memory region, providing the fastest IPC method.

**Characteristics:**
- Fastest IPC method (no data copying)
- Requires synchronization (semaphores, mutexes)
- Processes map same physical memory
- Direct memory access

**POSIX Shared Memory Example:**

```c
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>

#define SHARED_MEMORY_NAME "/my_shared_memory"
#define SHARED_MEMORY_SIZE 4096

int main() {
    int shm_fd;
    void* shared_memory;
    char* shared_message = "Hello from Process 1!";
    
    // Create or open the shared memory object
    shm_fd = shm_open(SHARED_MEMORY_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(1);
    }
    
    // Set the size of the shared memory
    if (ftruncate(shm_fd, SHARED_MEMORY_SIZE) == -1) {
        perror("ftruncate");
        exit(1);
    }
    
    // Map the shared memory into process address space
    shared_memory = mmap(0, SHARED_MEMORY_SIZE, 
                         PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shared_memory == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
    
    // Write to shared memory
    strcpy(shared_memory, shared_message);
    printf("Message written: %s\n", (char*)shared_memory);
    
    // Unmap and close
    munmap(shared_memory, SHARED_MEMORY_SIZE);
    close(shm_fd);
    
    // Optionally remove the shared memory object
    // shm_unlink(SHARED_MEMORY_NAME);
    
    return 0;
}
```

### Remote Procedure Call (RPC)

RPC allows programs to execute procedures on remote systems as if they were local function calls.

**gRPC Example Overview:**

1. **Define Service (.proto file):**
```protobuf
syntax = "proto3";

service Calculator {
    rpc CalculateSquare (Number) returns (Result);
}

message Number {
    int32 value = 1;
}

message Result {
    int32 value = 1;
}
```

2. **Generate Code:**
```bash
protoc -I=. --cpp_out=. calculator.proto
protoc -I=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` calculator.proto
```

3. **Implement Server:**
```cpp
class CalculatorServiceImpl final : public Calculator::Service {
public:
    ::grpc::Status CalculateSquare(::grpc::ServerContext* context, 
                                   const ::Number* request, 
                                   ::Result* response) override {
        response->set_value(request->value() * request->value());
        return ::grpc::Status::OK;
    }
};
```

4. **Implement Client:**
```cpp
int main() {
    auto channel = grpc::CreateChannel("localhost:50051", 
                                       grpc::InsecureChannelCredentials());
    auto stub = Calculator::NewStub(channel);
    
    Number number;
    number.set_value(5);
    Result result;
    
    grpc::ClientContext context;
    grpc::Status status = stub->CalculateSquare(&context, number, &result);
    
    if (status.ok()) {
        std::cout << "Square: " << result.value() << std::endl;
    }
    return 0;
}
```

## Signals and Interrupts

### Overview

Signals and interrupts are mechanisms for handling asynchronous events, but they serve different purposes and operate at different levels.

**Signal:**
- Software interrupt delivered to a process/thread
- Notifies process of specific events or conditions
- Generated within software
- Used for inter-process communication and event notification
- Examples: SIGINT (Ctrl+C), SIGTERM (termination), SIGCHLD (child process event)

**Interrupt:**
- Hardware signal sent to CPU
- Alerts CPU to events requiring immediate attention
- Generated by external hardware devices
- Used for handling external events and I/O operations
- Examples: Timer interrupt, keyboard interrupt, network card interrupt

**Key Differences:**

| Aspect | Signal | Interrupt |
|--------|--------|-----------|
| **Source** | Software (processes, OS) | Hardware (devices, timers) |
| **Purpose** | Software event notification, IPC | Hardware event handling |
| **Initiation** | Programmatic or manual | Hardware device timing/completion |
| **Handling** | Process signal handlers | OS interrupt service routines |
| **Level** | Process/application level | System/hardware level |

### Signal Handling

Operating systems provide mechanisms for processes to handle signals, defining how they respond to various events.

**Signal Generation Events:**

- User actions (Ctrl+C generates SIGINT)
- Hardware exceptions (division by zero, invalid memory access)
- I/O events (data arrival, socket activity)
- Timer and alarm signals
- Other processes (kill command)

**Signal Delivery:**
Signals are delivered to target processes based on the event type:
- User-generated signals directed to specific process
- Hardware exceptions delivered to offending process
- Broadcast signals to process groups

**Signal Handling Options:**

1. **Termination:** Process terminates (default for many signals)
2. **Ignore:** Process ignores the signal entirely
3. **Custom Handler:** Execute programmer-defined signal handler function
4. **Default Action:** Take predefined action (varies by signal type)

**Common Signals:**

| Signal | Number | Default Action | Description |
|--------|--------|----------------|-------------|
| SIGINT | 2 | Terminate | Interrupt (Ctrl+C) |
| SIGQUIT | 3 | Core dump | Quit (Ctrl+\) |
| SIGKILL | 9 | Terminate | Force kill (cannot be caught) |
| SIGSEGV | 11 | Core dump | Segmentation fault |
| SIGTERM | 15 | Terminate | Termination request |
| SIGCHLD | 17 | Ignore | Child process status change |
| SIGSTOP | 19 | Stop | Stop process (cannot be caught) |
| SIGCONT | 18 | Continue | Continue if stopped |

**Signal Features:**

- **Signal Queuing:** Signals can be queued if they arrive while handling another signal
- **Blocking Signals:** Processes can temporarily block signals to protect critical sections
- **Signal Masks:** Each process has a signal mask defining which signals are blocked
- **Reliable vs. Unrealizable Signals:** Modern systems use reliable signals that aren't lost

### Interrupt Handling

Operating systems handle interrupts through hardware and software cooperation to ensure timely response to external events.

**Interrupt Handling Process:**

1. **Interrupt Generation:**
   - Hardware devices generate interrupts (I/O controllers, timers)
   - Software can generate software interrupts (system calls, exceptions)

2. **Interrupt Request (IRQ):**
   - Device sends Interrupt Request to CPU
   - Each interrupt type has specific IRQ line
   - Priority assigned to different IRQ lines

3. **CPU Response:**
   - CPU suspends current execution
   - Enters kernel mode (supervisor mode)
   - Saves program counter and register state
   - Allows return to interrupted code later

4. **Interrupt Handling:**
   - CPU transfers control to Interrupt Service Routine (ISR)
   - Each interrupt type has predefined ISR
   - ISR identifies interrupt source
   - Processes event and performs necessary actions

5. **Context Switch (if needed):**
   - For timer interrupts or I/O completion
   - May switch to different process/thread
   - Saves current process state
   - Loads new process state

6. **Interrupt Acknowledgment:**
   - CPU acknowledges interrupt controller
   - Indicates interrupt processing complete
   - May send signal to device or clear flag

7. **Return from Interrupt:**
   - ISR completes execution
   - CPU restores previously saved state
   - Resumes interrupted program execution

**Interrupt Management:**

- **Interrupt Prioritization:** Higher-priority interrupts can preempt lower-priority ones
- **Masking/Unmasking:** OS can disable/enable specific interrupts
- **Nested Interrupts:** Higher-priority interrupts can interrupt ISRs
- **Interrupt Latency:** Time between interrupt occurrence and ISR execution

## Design Patterns

Multithreaded programming design patterns help structure and manage concurrent tasks efficiently, solving specific concurrency problems.

### Boss-Worker (Master-Slave)

**Description:**
One thread (boss) delegates tasks to a pool of worker threads. The boss divides work, distributes tasks, and collects results.

**Characteristics:**
- Boss thread manages work distribution
- Worker pool executes tasks
- Task queue between boss and workers
- Results collected by boss or written to shared location

**Use Cases:**
- Parallelizing independent tasks
- Web server request handling
- Task distribution in compute clusters
- Managing thread pool efficiently

**Advantages:**
- Efficient core utilization
- Scalable (add more workers)
- Boss can implement load balancing
- Clear separation of concerns

**Disadvantages:**
- Boss can become bottleneck
- Overhead of task distribution
- Worker synchronization needed

### Pipeline

**Description:**
A series of processing stages connected in linear sequence. Each stage processes data and passes it to the next stage.

**Characteristics:**
- Multiple stages in sequence
- Each stage performs specific operation
- Data flows through pipeline
- Stages can run concurrently

**Use Cases:**
- Stream processing
- Data transformation tasks
- Assembly-line style processing
- Compiler phases (lexing, parsing, code generation)
- Image/video processing

**Advantages:**
- Natural decomposition for sequential processing
- Good throughput with multiple items in pipeline
- Each stage can be optimized independently
- Parallelism across stages

**Disadvantages:**
- Slowest stage determines throughput
- Complex synchronization between stages
- Limited parallelism for single items

### Layered Design

**Description:**
System divided into multiple layers, each responsible for specific functionality aspect. Threads manage each layer.

**Characteristics:**
- Hierarchical organization
- Each layer provides services to layer above
- Threads coordinate between layers
- Clear abstraction boundaries

**Use Cases:**
- Network protocols (OSI model: data link, network, transport, application)
- Graphics rendering pipelines
- Operating system layers
- Multi-tier applications

**Advantages:**
- Clear separation of concerns
- Modularity and maintainability
- Each layer can be tested independently
- Facilitates distributed implementation

**Disadvantages:**
- Performance overhead from layer crossings
- Complexity in layer coordination
- Potential bottlenecks at layer boundaries

### Producer-Consumer

**Description:**
One or more producer threads create items/data, and one or more consumer threads process these items.

**Characteristics:**
- Shared buffer between producers and consumers
- Synchronization using semaphores or condition variables
- Producers add items to buffer
- Consumers remove items from buffer

**Use Cases:**
- Separating data generation from processing
- Event handling systems
- Logging systems
- I/O buffering

**Advantages:**
- Decouples production from consumption
- Producers and consumers work at their own pace
- Buffer smooths rate differences
- Natural parallelism

**Disadvantages:**
- Buffer size management
- Synchronization overhead
- Potential deadlock if not designed carefully

### Reader-Writer

**Description:**
Multiple threads read shared resource simultaneously (readers), while ensuring exclusive access for single thread during writes (writer).

**Characteristics:**
- Multiple concurrent readers allowed
- Single exclusive writer
- Readers and writers mutually exclusive
- Synchronization using read-write locks

**Use Cases:**
- Read-heavy workloads
- Databases with frequent queries
- Configuration data
- Caching systems

**Advantages:**
- Maximizes concurrency for readers
- Better performance than exclusive locks for read-heavy workloads
- Clear semantics

**Disadvantages:**
- Writer starvation possible
- More complex than simple locks
- Fairness considerations

### Thread Pool

**Description:**
Pool of pre-created worker threads execute tasks from a queue, avoiding overhead of thread creation/destruction.

**Characteristics:**
- Fixed or dynamic number of worker threads
- Task queue feeding workers
- Threads reused for multiple tasks
- Manager coordinates pool

**Use Cases:**
- Web servers handling requests
- Parallel computing frameworks
- Short-lived frequent tasks
- Resource-constrained environments

**Advantages:**
- Eliminates thread creation overhead
- Limits concurrent threads (resource control)
- Better resource utilization
- Faster task execution start

**Disadvantages:**
- Pool size tuning required
- Potential thread starvation
- Task queue management overhead

## Performance

### Metrics

Thread performance metrics evaluate efficiency, effectiveness, and scalability of multithreaded applications.

**Key Metrics:**

| Metric | Description | Importance |
|--------|-------------|------------|
| **Throughput** | Tasks completed per unit time | System capacity |
| **Latency** | Time for single task completion | Responsiveness |
| **Concurrency Level** | Number of threads running concurrently | Resource utilization |
| **CPU Utilization** | Percentage of time CPU executes threads | Efficiency |
| **Scalability** | Performance improvement with additional cores | Parallel efficiency |
| **Contention** | Thread competition for resources | Bottleneck identification |
| **Lock Contention** | Frequency/duration of lock waiting | Synchronization overhead |
| **Context Switching** | Frequency of context switches | Overhead |
| **Cache Efficiency** | Cache hit rate and locality | Memory performance |
| **Response Time Variability** | Consistency of response times | Predictability |

**Additional Considerations:**

- **Speedup:** Performance improvement with N threads vs. 1 thread
- **Efficiency:** Speedup / N (ideal is 1.0)
- **Amdahl's Law:** Theoretical maximum speedup limited by serial portion
- **Resource Utilization:** Memory, network, disk usage
- **Contention Resolution Time:** Time to resolve resource conflicts

### Programming Model Comparison

| Aspect | Multithreading | Multiprocessing | Event-Driven |
|--------|---------------|-----------------|--------------|
| **Execution Units** | Multiple threads in process | Multiple independent processes | Single/few threads with event loop |
| **Memory** | Shared address space | Separate address spaces | Shared within thread |
| **Communication** | Direct memory access | IPC (pipes, sockets, shared memory) | Callbacks, event queue |
| **Overhead** | Low (lightweight) | High (heavy-weight) | Very low |
| **Isolation** | Weak | Strong | N/A |
| **Fault Tolerance** | Crash affects entire process | Crashes isolated | Depends on implementation |
| **Synchronization** | Required (locks, semaphores) | Optional (if using shared memory) | Minimal (single thread) |
| **Scalability** | Good (limited by Amdahl's Law) | Excellent (process isolation) | Excellent (for I/O-bound) |
| **Best For** | Concurrent tasks, shared data | Independent tasks, CPU-bound | I/O-bound, many connections |
| **Examples** | Web server threads, parallel algorithms | Chrome browser tabs, worker pools | Node.js, nginx, GUI event loops |

**When to Use:**

- **Multithreading:** Shared data, moderate concurrency, responsive UIs
- **Multiprocessing:** CPU-intensive tasks, strong isolation needed, true parallelism
- **Event-Driven:** High concurrency I/O operations, network services, low latency

## References

**Course Materials:**
- CS 6200: Introduction to Operating Systems - Georgia Tech OMSCS

**Textbooks:**

- Arpaci-Dusseau and Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*
