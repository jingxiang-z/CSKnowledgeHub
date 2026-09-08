# 01 Operating System Introduction

## Table of Contents

1. [Overview](#overview)
2. [Core Functions](#core-functions)
3. [OS Components](#os-components)
4. [Types of Operating Systems](#types-of-operating-systems)
5. [OS Architectures](#os-architectures)
6. [Privilege Levels](#privilege-levels)
7. [OS Design Goals](#os-design-goals)
8. [Traditional OS Structures](#traditional-os-structures)
9. [Modern OS Approaches](#modern-os-approaches)
   - [SPIN](#spin)
   - [Exokernel](#exokernel)
   - [L3 Microkernel](#l3-microkernel)

## Overview

An **operating system (OS)** is system software that manages computer hardware and software resources and provides common services for computer programs. The OS acts as an intermediary between users/applications and the computer hardware.

### Primary Roles

- **Resource Manager**: Allocates and manages CPU, memory, storage, and I/O devices
- **Abstraction Layer**: Provides high-level abstractions that hide hardware complexity
- **Protection**: Enforces security policies and isolates processes
- **Interface Provider**: Offers user interfaces (GUI/CLI) and programming interfaces (system calls)

## Core Functions

| Function | Description |
|----------|-------------|
| **Process Management** | Creating, scheduling, and terminating processes; handling synchronization |
| **Memory Management** | Allocating memory, implementing virtual memory, managing page tables |
| **File System Management** | Organizing data storage, managing directories, enforcing access control |
| **Device Management** | Controlling I/O devices through device drivers |
| **Security & Protection** | User authentication, access control, resource isolation |
| **Networking** | Managing network protocols and communication |

## OS Components

### Kernel

The **kernel** is the core component of an operating system that has complete control over system resources.

**Key Responsibilities:**
- Process and thread scheduling
- Memory allocation and management
- Device driver interface and management
- System call handling
- Interrupt and exception handling

The kernel runs in privileged mode with direct hardware access.

### System Libraries

Collections of pre-compiled functions that provide standard interfaces for application developers. Examples include:
- Standard C library (libc)
- POSIX libraries
- System-specific APIs (Win32 API, Cocoa)

### Device Drivers

Software modules that enable the OS to communicate with hardware devices. Device drivers:
- Are hardware-specific
- Usually run in kernel mode
- Translate generic I/O commands to device-specific operations
- Handle interrupts from devices

### File System

Manages data organization and storage on persistent media. Common file systems:
- **Linux**: ext4, XFS, Btrfs
- **Windows**: NTFS, FAT32, ReFS
- **macOS**: APFS, HFS+

### User Interface

Provides mechanisms for user interaction:
- **CLI (Command-Line Interface)**: bash, zsh, cmd.exe, PowerShell
- **GUI (Graphical User Interface)**: Desktop environments like Windows Explorer, GNOME, KDE

## Types of Operating Systems

### Desktop Operating Systems
Designed for personal computers and workstations.
- **Examples**: Windows, macOS, Ubuntu, Fedora
- **Characteristics**: User-friendly interfaces, broad application support, multitasking

### Server Operating Systems
Optimized for managing server hardware and network services.
- **Examples**: Windows Server, Red Hat Enterprise Linux, Ubuntu Server
- **Characteristics**: High reliability, multi-user support, service management

### Mobile Operating Systems
Built for smartphones and tablets.
- **Examples**: Android, iOS, HarmonyOS
- **Characteristics**: Touch interfaces, power efficiency, app sandboxing

### Embedded Operating Systems
Used in specialized devices with specific functions.
- **Examples**: Embedded Linux, FreeRTOS, VxWorks
- **Characteristics**: Resource-constrained, real-time capabilities, minimal footprint

### Real-Time Operating Systems (RTOS)
Designed for time-critical applications with strict timing constraints.
- **Examples**: VxWorks, QNX, FreeRTOS
- **Characteristics**: Deterministic scheduling, guaranteed response times, priority-based scheduling

**Key Distinction**: RTOS guarantees response within specific time constraints (hard deadlines), while general-purpose OS optimizes for average throughput.

## OS Architectures

Operating system architecture defines how the OS is structured and how components interact.

### Architecture Comparison

| Architecture | Structure | Performance | Modularity | Fault Tolerance | Examples |
|--------------|-----------|-------------|------------|-----------------|----------|
| **Monolithic** | Single large kernel | High | Low | Low | Linux, BSD |
| **Microkernel** | Minimal kernel + user servers | Lower | High | High | QNX, Mach, L4 |
| **Hybrid** | Core in kernel + services in user space | Medium-High | Medium | Medium | Windows NT+, macOS |
| **Exokernel** | Minimal authorization layer | Very High | Very High | High | Research systems |

### Monolithic Kernel

All operating system services run in a single address space in kernel mode.

**Architecture:**
```
┌─────────────────────────────────────┐
│         User Applications           │
├─────────────────────────────────────┤
│      System Call Interface          │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │   Monolithic Kernel           │  │
│  │  - Process Management         │  │
│  │  - Memory Management          │  │
│  │  - File System                │  │
│  │  - Device Drivers             │  │
│  │  - Network Stack              │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│           Hardware                  │
└─────────────────────────────────────┘
```

**Advantages:**
- High performance due to direct component communication
- Efficient resource sharing
- No overhead from context switching between components

**Disadvantages:**
- Poor modularity and maintainability
- Single point of failure (one bug can crash entire system)
- Difficult to extend or modify
- Large trusted computing base

**Examples**: Linux, traditional Unix systems, early Windows versions

### Microkernel

Minimal kernel with most OS services running as separate user-space processes.

**Architecture:**
```
┌─────────────────────────────────────┐
│      User Applications              │
├─────────────────────────────────────┤
│  File System │ Device  │ Network    │ (User Space Servers)
│    Server    │ Drivers │  Stack     │
├─────────────────────────────────────┤
│      ┌─────────────────┐            │
│      │  Microkernel    │            │
│      │  - IPC          │            │
│      │  - Scheduling   │            │
│      │  - Basic Memory │            │
│      └─────────────────┘            │
├─────────────────────────────────────┤
│           Hardware                  │
└─────────────────────────────────────┘
```

**Core Services (in kernel):**
- Inter-Process Communication (IPC)
- Basic scheduling
- Low-level memory management
- Hardware abstraction

**Advantages:**
- High modularity and maintainability
- Better fault isolation (server crash doesn't affect kernel)
- Easier to extend and debug
- Smaller trusted computing base
- Better security

**Disadvantages:**
- Performance overhead from IPC
- Frequent context switches between user and kernel space
- More complex IPC mechanisms

**Examples**: QNX, Mach, L4 family, MINIX 3

### Hybrid Kernel

Combines elements of monolithic and microkernel architectures.

**Design:**
- Core essential services in kernel space (performance)
- Some services in user space (modularity)
- Pragmatic balance between approaches

**Advantages:**
- Better performance than pure microkernel
- More modular than pure monolithic
- Practical compromise for commercial systems

**Disadvantages:**
- More complex design
- Still has larger kernel than microkernel
- Trade-offs may not satisfy purists

**Examples**: Windows NT and later, macOS (XNU kernel), DragonFly BSD

### Exokernel

Minimal kernel that separates resource protection from management.

**Philosophy:**
- Kernel only handles resource authorization
- Library Operating Systems (LibOS) manage resources
- Applications have direct (but controlled) hardware access

This is primarily a research architecture. See detailed analysis in [Modern OS Approaches](#modern-os-approaches).

## Privilege Levels

Modern CPUs implement multiple privilege levels to protect system integrity. Most operating systems use two primary levels:

### Kernel Mode (Supervisor Mode, Privileged Mode, Ring 0)

| Aspect | Description |
|--------|-------------|
| **Privilege Level** | Highest privilege level |
| **Hardware Access** | Direct, unrestricted access to all hardware |
| **Memory Access** | Can access all memory regions |
| **Instructions** | Can execute all CPU instructions including privileged ones |
| **Code Running** | Kernel, device drivers |
| **Crash Impact** | System crash (kernel panic, blue screen) |

### User Mode (Unprivileged Mode, Ring 3)

| Aspect | Description |
|--------|-------------|
| **Privilege Level** | Lowest privilege level |
| **Hardware Access** | Restricted; must use system calls |
| **Memory Access** | Only user-space memory regions |
| **Instructions** | Cannot execute privileged instructions |
| **Code Running** | User applications, libraries |
| **Crash Impact** | Process termination only |

### Mode Transitions

**User Mode → Kernel Mode** occurs via:
- System calls (explicit requests for OS services)
- Hardware interrupts (timer, I/O completion)
- Exceptions (page faults, divide by zero, protection violations)

**Kernel Mode → User Mode** occurs via:
- Return from system call
- Return from interrupt handler
- Context switch to user process

### Architecture Diagram

```
┌────────────────────────────────────┐
│       User Applications            │  Ring 3 (User Mode)
│  (Web Browser, Text Editor, etc.)  │  - Limited access
├────────────────────────────────────┤  - Protected memory
│      System Call Interface         │
├────────────────────────────────────┤
│        Operating System            │  Ring 0 (Kernel Mode)
│   (Kernel, Device Drivers)         │  - Full hardware access
├────────────────────────────────────┤  - All instructions
│          Hardware                  │
└────────────────────────────────────┘
```

### Protection Mechanism

When a user program attempts to execute a privileged instruction:
1. CPU generates a protection fault (exception)
2. Control transfers to kernel exception handler
3. Kernel typically terminates the offending process
4. System remains stable despite malicious or buggy user code

This separation is fundamental to modern OS security and stability.

## OS Design Goals

Operating system designers balance multiple objectives:

### 1. Protection

**Objectives:**
- Protect hardware from user errors
- Protect users and processes from each other
- Protect the OS from user programs
- Protect users from their own mistakes

**Mechanisms:**
- Memory protection (MMU, page tables)
- Access control lists (ACLs)
- Capability systems
- Process isolation

### 2. Performance

**Objectives:**
- Minimize overhead for system services
- Efficient resource utilization
- Fast system calls and context switches

**Metrics:**
- Throughput (operations per second)
- Response time
- Turnaround time
- CPU utilization

### 3. Flexibility and Extensibility

**Objectives:**
- Adapt to different application needs
- Support new hardware without kernel recompilation
- Allow customization

**Approaches:**
- Loadable kernel modules
- Plugin architectures
- Microkernel designs

### 4. Scalability

**Objectives:**
- Performance scales with additional hardware
- Support multi-core and multi-processor systems
- Handle increasing workloads

**Challenges:**
- Lock contention
- Cache coherence
- Load balancing

### 5. Reliability

**Objectives:**
- System remains operational despite component failures
- Predictable behavior
- Graceful degradation

**Techniques:**
- Fault tolerance mechanisms
- Error detection and correction
- Redundancy
- Checkpoint and recovery

### 6. Responsiveness

**Objectives:**
- React quickly to external events
- Low latency for interactive applications
- Meet real-time constraints (for RTOS)

**Important for:**
- Interactive applications (games, multimedia)
- Control systems
- Human-computer interaction

### Trade-offs

These goals often conflict:

- **Performance vs. Security**: Fast systems may bypass security checks; secure systems add overhead
- **Flexibility vs. Simplicity**: Extensible systems are more complex to implement and maintain
- **Portability vs. Optimization**: Generic code sacrifices hardware-specific optimizations

Good OS design requires understanding these trade-offs and making appropriate choices for the target use case.

## Traditional OS Structures

### Comparison of Classical Approaches

| Structure | Protection | Performance | Extensibility | Characteristics |
|-----------|------------|-------------|---------------|-----------------|
| **Monolithic** | High | High | Low | All OS services in single address space; minimal border crossings |
| **DOS-like** | Low | High | High | No separation between application and OS; not suitable for general-purpose use |
| **Microkernel** | High | Potentially Low | High | Minimal kernel with IPC; services as separate servers |

### Monolithic Structure

Applications run in separate address spaces (protected from each other), and the OS runs in its own address space (protected from applications). When an application needs a service (e.g., file I/O), it switches to the OS address space to execute the necessary code.

**Performance**: Good, because all service components reside in a single address space, reducing communication overhead.

**Limitation**: "One size fits all" model limits customization for specific application needs.

### Microkernel Challenges

While microkernel designs achieve strong protection and extensibility, they face a significant performance challenge: **border crossings**.

Since services are separate server processes, an application request may require:
1. Kernel-mediated IPC between application and multiple servers
2. Frequent address space switching
3. Explicit costs (switching time) and implicit costs (cache/TLB locality loss)

This motivated research into alternative approaches that could achieve all three goals: protection, performance, and extensibility.

## Modern OS Approaches

In the 1990s, researchers focused on achieving protection, performance, and extensibility simultaneously. Three influential systems emerged:

### Quick Comparison

| System | Key Innovation | Protection Method | Performance Strategy |
|--------|----------------|-------------------|----------------------|
| **SPIN** | Language-enforced protection | Modula-3 type safety | Co-location in same address space |
| **Exokernel** | Separate authorization from management | Secure bindings with encrypted keys | Direct hardware access after binding |
| **L3** | Processor-specific microkernel | Hardware address spaces | Optimized IPC (123 cycles) |

## SPIN

**Philosophy**: Use programming language features for protection instead of hardware mechanisms.

### Core Ideas

**Language-Enforced Protection:**
- Written in Modula-3, a strongly-typed, memory-safe language
- **Logical protection domains** instead of hardware address spaces
- Type safety enforced by compiler, not MMU

**Co-location for Performance:**
- Kernel and extensions reside in the same hardware address space
- Extension access = simple procedure call (no address space switch)
- Minimal border crossing overhead

**Capabilities as Pointers:**
- Access to resources via language-supported pointers
- Modula-3 pointers are type-specific and non-forgeable
- Compiler enforces safety

### Mechanisms for Extensibility

| Mechanism | Purpose |
|-----------|---------|
| **create** | Instantiate a logical protection domain, initialize contents, export entry points |
| **resolve** | Dynamically link two protection domains; once resolved, accessing methods happens at memory speed |
| **combine** | Aggregate multiple logical protection domains into a single domain |

### Event-Based Communication

SPIN handles external events (interrupts, exceptions, system calls) using an event-based model:
- Services register event handlers with the SPIN event dispatcher
- Supports one-to-one, one-to-many, and many-to-one mappings
- Example: Multiple network interface events (Ethernet, ATM) can map to a single IP handler

### Core Services

SPIN provides only interface definitions (mechanisms), not implementations (policies):

**CPU Scheduling:**
- Global scheduler allocates time at macro level to extensions
- Uses **strand** abstraction (maps to extension's thread concept)

**Memory Management:**
- Interface functions for allocating/deallocating physical page frames and virtual pages
- Event handlers for page faults and access faults

### Advantages

- High performance (minimal border crossings)
- Highly extensible (dynamic binding of implementations)
- Safe despite co-location (language enforcement)

### Disadvantages

- Requires type-safe language (limits language choice)
- Potential runtime overhead from language features
- Extensions must be written in Modula-3

## Exokernel

**Philosophy**: Separate resource authorization from resource management.

### Architecture

```
┌─────────────────────────────────────┐
│   Application   │   Application     │
├─────────────────┼───────────────────┤
│    LibOS A      │     LibOS B       │ (Implement OS abstractions)
│ (e.g., Unix)    │  (e.g., Plan 9)   │
├─────────────────┴───────────────────┤
│          Exokernel                  │ (Only authorization)
│  - Secure bindings                  │
│  - Resource allocation              │
├─────────────────────────────────────┤
│          Hardware                   │
└─────────────────────────────────────┘
```

### Core Concepts

**Minimal Kernel:**
- Exokernel only handles secure resource authorization
- No OS abstractions (processes, files, etc.) in kernel
- Supports mechanisms for allocating resources but no abstractions

**Library Operating Systems (LibOS):**
- Implement OS abstractions in user space
- Determine usage semantics of allocated resources
- Exokernel is unaware of user-level processes within a LibOS

**Secure Bindings:**

When a LibOS requests a hardware resource:
1. Exokernel validates the request (e.g., TLB entry, physical page)
2. Exokernel creates a secure binding and provides an **encrypted key** (capability)
3. Key is non-forgeable and non-transferable
4. LibOS presents key when accessing the resource
5. After binding establishment, resource access is very fast (hardware speed)

**Downloaded Code:**
- LibOS can inject code into kernel (e.g., packet filters, garbage collection)
- Code runs on behalf of specific LibOS
- Avoids border crossings for performance-critical operations
- Trade-off: Potentially compromises protection compared to language-enforced safety

### Resource Management

**CPU Scheduling:**
- Uses a linear vector of time slots
- Each LibOS registers its allocated time slots
- During its quantum, LibOS has complete control of processor
- Timer interrupt transfers control back to Exokernel
- Context saving time is bounded; exceeding it results in penalty

**Memory Management:**

Page fault handling flow:
1. Exokernel fields the trap and identifies the running LibOS
2. Passes fault to appropriate LibOS (upcall)
3. LibOS handles fault and establishes virtual-to-physical mapping
4. LibOS presents mapping and encrypted key for TLB entry to Exokernel
5. Exokernel validates key and installs mapping into hardware TLB

**Software TLB (STLB):**
- Maintained for each LibOS
- Holds guaranteed memory mappings
- Used during context switching to mitigate locality loss when hardware TLB is flushed

**Resource Revocation:**
- Exokernel maintains a scoreboard of resource allocations
- Uses **revoke** call (upcall) with **repossession vector** specifying which resources are being reclaimed
- LibOS performs corrective action (e.g., saving data to disk)
- LibOS can pre-seed Exokernel with **autosave options** to minimize workload during revocation

### Data Structures

**PE (Process Environment) Structure:**
- Maintained for each LibOS
- Holds handler entry points for different discontinuities:
  - Exceptions
  - External interrupts
  - System calls

**Software TLB:**
- Per-LibOS structure
- Holds guaranteed mappings to mitigate performance loss during context switches

### Advantages

- Maximum flexibility (LibOS controls all policies)
- High performance (direct hardware access after authorization)
- Multiple OS personalities can coexist
- Application-specific optimizations possible

### Disadvantages

- Complex LibOS implementation
- Security concerns with downloaded code
- No shared abstractions between LibOSs
- Primarily research-oriented

## L3 Microkernel

**Philosophy**: Microkernels can be fast if implemented carefully and processor-specifically.

### Debunking Microkernel Performance Myths

L3 systematically disproved misconceptions about microkernel performance (derived from Mach's poor performance):

#### Myth 1: Border Crossing is Inherently Expensive

**L3's Response:**
- Achieved user-to-kernel border crossing in **123 processor cycles**
- Near theoretical minimum of **107 cycles** on the hardware
- In contrast, Mach took ~900 cycles on the same hardware

**Conclusion**: Mach's slowness was due to design priorities (portability leading to code bloat and cache pollution), not the microkernel structure itself.

#### Myth 2: Address Space Switching is Expensive

**L3's Strategy:**
- Use hardware features to manage protection domains efficiently
- On architectures without Address Space Tagged TLBs (Intel 486/Pentium):
  - Use **segment registers** (x86, PowerPC) to carve linear virtual address space
  - Create multiple small, co-resident protection domains
  - Avoid TLB flushing when switching between small domains

**Conclusions:**
- **Small protection domains**: Efficient context switching is achievable
- **Large protection domains**: Explicit switching cost is insignificant compared to unavoidable implicit costs (memory effects, cache pollution) that affect all OS structures

#### Myth 3: IPC is Slow in Microkernels

**L3's Response:**
- Efficient implementation makes thread switch time competitive with SPIN and Exokernel
- Processor-specific optimization is key

### Design Principles

**1. Minimal Abstractions:**

L3 provides only fundamental abstractions required by all subsystems:
- Address spaces
- Threads
- Inter-Process Communication (IPC)
- Unique IDs (UID)

All other OS services (file systems, network protocols, scheduling policies) are implemented as processes/servers above the microkernel.

**2. Processor-Specific Implementation:**

L3 advocates that for maximum efficiency, microkernel implementation must be processor-specific:
- Exploit unique hardware capabilities (segment registers, fast system call instructions)
- Non-portable by design
- Performance over portability for the kernel itself
- High-level services above kernel remain processor-independent

**3. Small Protection Domains:**

Use hardware features to efficiently manage multiple small protection domains:
- Pack domains into same address space using segments
- Avoid TLB flush overhead
- Efficient context switching

### Impact

L3 demonstrated that a microkernel structure can achieve:
- **Protection**: Using distinct address spaces and privileged mode
- **Extensibility**: Services implemented as separate processes
- **High Performance**: Through efficient, processor-specific implementation

This challenged previous assumptions that microkernels were inherently slow and validated the microkernel approach for high-performance systems.

### Examples in Practice

The L4 microkernel family (descended from L3) is used in various systems:
- seL4 (formally verified microkernel)
- OKL4 (mobile devices)
- Fiasco.OC and L4Re (real-time systems)

## Summary

Operating systems manage computer resources and provide abstractions that make systems usable and secure. Key concepts include:

**Fundamental Concepts:**
- OS roles: resource management, abstraction, protection, interface
- Kernel and user mode separation for security and stability
- System calls as the interface between applications and kernel

**Architectural Approaches:**
- Monolithic: High performance, low modularity
- Microkernel: High modularity, potential performance overhead
- Hybrid: Practical balance for commercial systems

**Design Trade-offs:**
- Performance vs. security
- Flexibility vs. simplicity
- Portability vs. optimization

**Modern Innovations:**
- SPIN: Language-enforced protection for safe extensibility
- Exokernel: Separate authorization from management for maximum flexibility
- L3: Processor-specific optimization proves microkernels can be fast

Understanding these foundational concepts is essential for studying advanced operating system topics including process management, memory management, thread management, and device management.

## References

**Course Materials:**
- CS 6200: Introduction to Operating Systems - Georgia Tech OMSCS
- CS 6210: Advanced Operating Systems - Georgia Tech OMSCS

**Foundational Papers:**
- Bershad et al., "SPIN - An Extensible Microkernel for Application-Specific Operating System Services," ACM SOSP 1995
- Engler et al., "Exokernel: An Operating System Architecture for Application-Level Resource Management," ACM SOSP 1995
- Liedtke, J., "On μ-Kernel Construction," ACM SOSP 1995

**Textbooks:**
- Arpaci-Dusseau and Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*
