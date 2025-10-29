# CPU Fundamentals

## Table of Contents
1. [Introduction](#introduction)
2. [Computer Architecture Components](#computer-architecture-components)
3. [Instruction Set Architecture](#instruction-set-architecture)
4. [Assembly Language](#assembly-language)
5. [Performance Metrics](#performance-metrics)
6. [Power Consumption](#power-consumption)
7. [Fabrication Cost](#fabrication-cost)
8. [References](#references)

## Introduction

Computer architecture is the science and art of designing computers that are well-suited for their purpose by improving performance and capabilities. This requires a deep understanding of technological trends, performance metrics, and fundamental trade-offs involving power and cost.

### Basic Execution Workflow

The CPU executes instructions through a series of stages known as the instruction cycle:

1. **Fetch**: The CPU uses the program counter (PC) to fetch the next instruction from main memory. The instruction is transferred via the address and data buses.

2. **Decode**: The fetched instruction is decoded by the control unit to determine the required operation and operands.

3. **Execute**: The ALU performs the required arithmetic or logical operation. The control unit generates the necessary control signals for data movement.

4. **Memory Access**: If the instruction involves memory access (e.g., load/store), the data is read from or written to memory. This step involves interaction between the CPU, main memory, and possibly the cache.

5. **Write Back**: The result of the execution is written back to the appropriate register or memory location.

## Computer Architecture Components

A computer system consists of several key components that work together to execute programs:

### 1. Central Processing Unit (CPU)

The CPU is the brain of the computer, responsible for executing instructions.

**Sub-components:**

- **Arithmetic Logic Unit (ALU)**: Performs arithmetic and logical operations (addition, subtraction, AND, OR, etc.).

- **Control Unit (CU)**: Directs the operation of the processor by decoding instructions and generating control signals.

- **Registers**: Small, fast storage locations used for temporary data storage and manipulation. Types include:
  - **General Purpose Registers (GPRs)**: Used for a wide variety of operations.
  - **Special Purpose Registers**: Used for specific functions like the Program Counter (PC), Stack Pointer (SP), and Status Register.

- **Cache**: A small, fast memory located close to the CPU to speed up access to frequently used data. Typically divided into levels (L1, L2, L3) with L1 being the fastest and smallest.

### 2. Memory Hierarchy

A multi-level system designed to balance speed, capacity, and cost:

- **Registers**: The fastest and smallest type of memory, located within the CPU.

- **Cache Memory**: Provides faster data access to the CPU by storing frequently accessed data. It is typically divided into levels:
  - **L1 Cache**: Fastest and smallest, closest to the CPU cores
  - **L2 Cache**: Larger and slightly slower than L1
  - **L3 Cache**: Largest and slowest cache level, often shared among cores

- **Main Memory (RAM)**: Volatile memory used to store data and instructions currently being processed by the CPU.

- **Secondary Storage**: Non-volatile storage used for long-term data storage, such as hard drives and SSDs.

### 3. Input/Output (I/O) Devices

Devices that facilitate interaction between the computer and the external environment:

- **Input Devices**: Keyboards, mice, scanners
- **Output Devices**: Monitors, printers, speakers
- **Storage Devices**: Hard drives, SSDs, USB drives

### 4. Bus Systems

Communication pathways that transfer data between different components:

- **Data Bus**: Carries data between the CPU, memory, and I/O devices.
- **Address Bus**: Carries the addresses of data (but not the data itself) to be accessed.
- **Control Bus**: Carries control signals from the control unit to other components.

## Instruction Set Architecture

The **Instruction Set Architecture (ISA)** is the abstract interface between hardware and software. It defines what instructions a processor can execute and how they are encoded, forming a contract between hardware designers and software developers.

### ISA Components

#### 1. Instructions

- **Operation Codes (Opcodes)**: The portion of a machine language instruction that specifies the operation to be performed.

- **Instruction Types**:
  - **Arithmetic and Logical Instructions**: Perform mathematical calculations and logical operations (e.g., ADD, SUB, AND, OR)
  - **Data Transfer Instructions**: Move data between memory and registers or between registers (e.g., LOAD, STORE, MOV)
  - **Control Flow Instructions**: Change the sequence of instruction execution (e.g., JUMP, CALL, RETURN, BRANCH)
  - **Special Instructions**: Specific to the architecture, such as system calls and no-operation (NOP)

#### 2. Data Types

Defines the types of data the ISA can handle, such as integer, floating-point, character, and more complex types like vectors and matrices.

#### 3. Registers

- **General Purpose Registers (GPRs)**: Used for a wide variety of operations
- **Special Purpose Registers**: Used for specific functions like the Program Counter (PC), Stack Pointer (SP), and Status Register

#### 4. Addressing Modes

Methods to specify operands for instructions:

- **Immediate**: Operand is a constant within the instruction itself
- **Direct**: Address of the operand is specified in the instruction
- **Indirect**: Address of the operand is held in a register or memory location
- **Register**: Operand is located in a register
- **Indexed**: Effective address is computed by adding an index to a base address

#### 5. Memory Architecture

Defines the memory model, including address space, data alignment, and the relationship between main memory and cache.

#### 6. Interrupt and Exception Handling

Mechanisms for handling unexpected events or conditions, such as hardware interrupts or software exceptions.

#### 7. External I/O

Methods for the processor to communicate with external devices, often involving specific instructions for input and output operations.

### ISA Types

Different architectural philosophies lead to different ISA designs:

#### 1. CISC (Complex Instruction Set Computing)

- **Characteristics**: Large number of complex instructions that can perform multiple operations
- **Example**: x86 architecture
- **Pros**:
  - Can perform complex operations with fewer instructions
  - Potentially reduces the number of instructions per program
  - Reduces memory bandwidth for instruction fetches
- **Cons**:
  - Complex instruction decoding and execution
  - Can limit clock speed and increase power consumption
  - Variable instruction length complicates pipelining

#### 2. RISC (Reduced Instruction Set Computing)

- **Characteristics**: Small, highly optimized set of simple instructions
- **Example**: ARM, MIPS architecture
- **Pros**:
  - Simplifies instruction decoding
  - Allows for higher clock speeds
  - More efficient pipelining
  - Fixed instruction length
- **Cons**:
  - May require more instructions to perform complex tasks
  - Places greater demands on the compiler
  - Higher memory bandwidth requirements

#### 3. VLIW (Very Long Instruction Word)

- **Characteristics**: Encodes multiple operations in a single, long instruction word
- **Example**: Itanium architecture, DSP processors
- **Pros**:
  - Can exploit instruction-level parallelism explicitly
  - Simplifies the hardware
  - Compiler has global view for optimization
- **Cons**:
  - Increased complexity in the compiler
  - Code bloat due to NOPs
  - Potential inefficiency in handling variable instruction latencies

#### 4. EPIC (Explicitly Parallel Instruction Computing)

- **Characteristics**: Similar to VLIW but with additional features to manage parallelism and dependencies
- **Example**: Intel Itanium
- **Features**: Predication, speculation, explicit parallelism hints

## Assembly Language

Assembly language is a low-level programming language that provides a human-readable representation of machine code. Each assembly language instruction typically corresponds to a single machine instruction.

### MIPS Assembly Example

Here is a simple MIPS assembly program that adds two numbers and prints the result:

```assembly
.data
    num1:   .word 5          # Define a word (32-bit integer) with value 5
    num2:   .word 10         # Define a word with value 10
    result: .word 0          # Define a word to store the result

.text
    .globl main              # Declare the main function globally
main:
    lw    $t0, num1          # Load the value of num1 into register $t0
    lw    $t1, num2          # Load the value of num2 into register $t1
    add   $t2, $t0, $t1      # Add the values in $t0 and $t1, store result in $t2
    sw    $t2, result        # Store the result from $t2 into memory location result

    li    $v0, 1             # Load the system call code for print integer into $v0
    lw    $a0, result        # Load the result into $a0 (argument for print integer)
    syscall                  # Make the system call to print the integer

    li    $v0, 10            # Load the system call code for exit into $v0
    syscall                  # Make the system call to exit the program
```

### Program Structure

#### Data Section
```assembly
.data
    num1:   .word 5
    num2:   .word 10
    result: .word 0
```
- **.data**: Directive indicating the beginning of the data segment, where variables and constants are defined
- **num1, num2**: Labels for 32-bit integers with initial values
- **result**: Label for storing the computation result, initialized to 0

#### Text Section
```assembly
.text
    .globl main
main:
```
- **.text**: Directive indicating the beginning of the code segment
- **.globl main**: Makes the `main` label globally accessible as the entry point
- **main**: Label marking the start of executable instructions

#### Instructions

**Data Movement:**
```assembly
    lw    $t0, num1          # Load word from memory to register
    sw    $t2, result        # Store word from register to memory
```
- **lw** (load word): Loads a 32-bit value from memory into a register
- **sw** (store word): Stores a 32-bit value from a register into memory

**Arithmetic:**
```assembly
    add   $t2, $t0, $t1      # Add two registers, store in third
```
- **add**: Adds the values in two source registers and stores the result in a destination register

**System Calls:**
```assembly
    li    $v0, 1             # Load immediate value 1 (print integer code)
    lw    $a0, result        # Load argument for system call
    syscall                  # Execute system call
```
- **li** (load immediate): Loads a constant value into a register
- **syscall**: Makes a system call; type determined by value in `$v0`
  - Code 1: Print integer (argument in `$a0`)
  - Code 10: Exit program

## Performance Metrics

Understanding and measuring performance is fundamental to computer architecture. Performance can be evaluated through various metrics and laws.

### Speed Metrics

- **Throughput**: The amount of work or data processed by a system in a given amount of time
- **Latency**: The time it takes to complete a single task or operation from start to finish

**Speedup**: A measure comparing the performance of two systems:

$$
Speedup = \frac{Speed(X)}{Speed(Y)} = \frac{Throughput(X)}{Throughput(Y)} = \frac{Latency(Y)}{Latency(X)}
$$

- **Speedup < 1**: Performance has degraded
- **Speedup > 1**: Performance has improved

### Benchmarks

Benchmarks are standard tasks for measuring processor performance. A benchmark is a suite of programs that represent common tasks:

- **Real Applications**: Most realistic, most difficult to set up, used for real machine comparisons
- **Kernels**: Most time-consuming part of an application, still difficult to set up, used for prototypes
- **Synthetic**: Similar to kernels but simpler to compile, used for design studies
- **Peak Performance**: Used for marketing

### The Iron Law of Performance

The Iron Law provides a fundamental framework for understanding factors that influence processor performance:

$$
Execution\ Time = Instruction\ Count \times Cycles\ Per\ Instruction \times Clock\ Cycle\ Time
$$

**Components:**

- **Instruction Count (IC)**: The total number of instructions executed by a program (influenced by algorithm and compiler)
- **Cycles Per Instruction (CPI)**: The average number of clock cycles each instruction takes to execute (influenced by processor architecture)
- **Clock Cycle Time (T)**: The duration of a single clock cycle, inversely proportional to clock frequency (influenced by hardware implementation)

**Implications**: Computer architects primarily influence CPI and clock cycle time through processor and instruction set design. The compiler and algorithm affect the instruction count.

### Amdahl's Law

Amdahl's Law is used to find the maximum improvement possible in a system when only part of the system is improved:

$$
S = \frac{1}{1-P+\frac{P}{N}}
$$

Where:
- **S** is the theoretical maximum speedup
- **P** is the proportion of the program that can be parallelized
- **N** is the number of processors or cores

**Key Principles:**

1. **Make the Common Case Fast**: Small improvements to frequently used parts yield better overall results than large improvements to rarely used parts
2. **Diminishing Returns**: Successive improvements yield progressively smaller gains
3. **Serial Bottleneck**: If only 90% of a program can be parallelized, maximum speedup is 10× regardless of number of cores

**Example**: If 80% of a program can be parallelized (P=0.8) with 4 cores (N=4):
$$
S = \frac{1}{0.2 + \frac{0.8}{4}} = \frac{1}{0.4} = 2.5
$$
The maximum speedup is 2.5×, not 4×, due to the 20% serial portion.

### Lhadma's Law

A corollary to Amdahl's Law: **While trying to make the common case fast, do not make the uncommon case worse.**

This reminds architects to consider the impact of optimizations on all code paths, not just the frequently executed ones.

## Power Consumption

Power consumption is a critical design constraint in modern processors, composed of two main components:

### Dynamic Power

Dynamic power is the power consumed by a processor due to the charging and discharging of capacitors during the switching of transistors. It occurs only when the processor is actively performing computations.

$$
P_{dynamic} = \alpha C V^2 f
$$

**Factors:**

- **Clock Frequency (f)**: Higher frequencies increase dynamic power because more switching events occur per unit time
- **Supply Voltage (V)**: Power consumption increases quadratically with voltage. Reducing voltage significantly decreases dynamic power
- **Capacitance (C)**: Larger or more complex circuits have higher capacitance, increasing dynamic power
- **Activity Factor (α)**: The fraction of transistors switching per clock cycle. More active transistors lead to higher power consumption

### Static Power

Static power, also known as leakage power, is the power consumed by a processor even when it is not actively switching. It is due to leakage currents that flow through the transistors when they are in the off state.

**Factors:**

- **Supply Voltage (V)**: Lower voltages can increase static power due to increased leakage
- **Temperature**: Higher temperatures exacerbate leakage currents, increasing static power consumption
- **Transistor Size**: As transistor sizes decrease with advanced fabrication technologies, leakage currents become more significant

### Power Trade-offs

There is a fundamental trade-off between dynamic and static power: lowering the supply voltage reduces dynamic power but can lead to increased leakage currents and higher static power consumption. Finding the optimal voltage point is crucial for energy-efficient design.

**Modern Techniques:**
- **Dynamic Voltage and Frequency Scaling (DVFS)**: Adjusting voltage and frequency based on workload
- **Clock Gating**: Disabling clock signals to idle units
- **Power Gating**: Completely shutting off power to unused circuit blocks
- **Multiple Voltage Domains**: Different parts of the chip operating at different voltages

## Fabrication Cost

Fabrication cost includes the cost of manufacturing and the cost of defective parts. Understanding these costs is crucial for economic chip design.

### Key Factors

**Die Size**: The larger the die, the higher the percentage of defective parts. Larger dies have a higher probability of containing a manufacturing defect.

**Fabrication Yield**: The ratio of working chips to total chips on a wafer:

$$
Fabrication\ Yield = \frac{Number\ of\ Working\ Chips}{Number\ of\ Chips\ on\ Wafer}
$$

**Defect Density**: The number of defects per unit area of the silicon wafer. Lower defect density improves yield.

### Moore's Law Impact

**Moore's Law** states that the number of transistors on a chip doubles approximately every 18-24 months. This trend provides two key benefits:

1. **Cost Reduction**: The same processor can be manufactured on a smaller die, reducing cost
2. **Performance Improvement**: A better processor can be built in the same die area, improving performance

**Technology Scaling Benefits:**
- Smaller transistors switch faster
- More transistors fit in the same area
- Lower power per transistor (historically)
- Reduced manufacturing cost per transistor

**Modern Challenges:**
- Physical limits approaching (quantum effects, heat dissipation)
- Increasing mask and development costs
- Diminishing returns in power reduction
- Shift towards architectural innovation rather than pure scaling

## References

This document synthesizes fundamental concepts in computer architecture from:

- **Georgia Institute of Technology** - OMSCS CS 6200 and CS 6210 graduate courses
- **Columbia University** - Graduate Computer Science courses
- Patterson, D. A., & Hennessy, J. L. (2017). *Computer Organization and Design: The Hardware/Software Interface* (5th ed.). Morgan Kaufmann
- Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach* (6th ed.). Morgan Kaufmann
