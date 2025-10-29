# CPU Processor Design

## Table of Contents
1. [Introduction](#introduction)
2. [Processor Design Types](#processor-design-types)
3. [Pipelining](#pipelining)
4. [Branch Prediction](#branch-prediction)
5. [Instruction-Level Parallelism](#instruction-level-parallelism)
6. [Out-of-Order Execution](#out-of-order-execution)
7. [Compiler Optimizations](#compiler-optimizations)
8. [Processor Architectures](#processor-architectures)
9. [Multi-Core Systems](#multi-core-systems)
10. [References](#references)

## Introduction

Modern processor design focuses on exploiting parallelism at multiple levels to maximize performance. The central strategy involves increasing Instruction-Level Parallelism (ILP) through sophisticated hardware mechanisms and intelligent compiler optimizations, all while managing the constraints of power consumption and complexity.

### Processor Design Workflow

The typical workflow for designing a processor includes:

1. **Define the ISA**: Determine the set of instructions, data types, addressing modes, and architectural features

2. **Design the Data Path**: Create the components necessary to execute instructions, such as ALUs, registers, multiplexers, and buses

3. **Design the Control Unit**: Develop the logic to generate control signals based on decoded instructions

4. **Implement Pipelining**: Divide instruction execution into stages and design mechanisms to handle pipeline hazards

5. **Design the Memory Hierarchy**: Plan the organization of registers, cache levels, and main memory for efficient data access

6. **Simulate and Verify**: Use simulation tools to verify functionality and performance. Debug and optimize as necessary

7. **Physical Design**: Translate the logical design into a physical layout for fabrication. This includes placement, routing, and timing analysis

8. **Fabrication and Testing**: Manufacture the processor and perform extensive testing to ensure it meets design specifications

## Processor Design Types

Different processor designs represent trade-offs between complexity, performance, and power consumption.

### 1. Single-Cycle Processors

- **Characteristics**: Each instruction is executed in a single clock cycle
- **Advantages**: Simple design, easy to understand
- **Disadvantages**: Long clock cycle to accommodate the slowest instruction, poor resource utilization

### 2. Multi-Cycle Processors

- **Characteristics**: Instructions are broken down into multiple stages, with each stage executed in a separate clock cycle
- **Advantages**: Shorter clock cycle, better resource sharing
- **Disadvantages**: Increased complexity in control unit, still sequential execution

### 3. Pipelined Processors

- **Characteristics**: Instructions are divided into stages, and multiple instructions are overlapped in execution
- **Advantages**: Significantly improved throughput, better resource utilization
- **Disadvantages**: Requires handling pipeline hazards, increased complexity

### 4. Superscalar Processors

- **Characteristics**: Capable of executing multiple instructions simultaneously by having multiple execution units
- **Types**:
  - **In-Order Superscalar**: Issues multiple instructions per cycle but maintains program order
  - **Out-of-Order (OOO) Superscalar**: Dynamically reorders instructions for optimal resource usage
- **Advantages**: High performance on general-purpose code
- **Disadvantages**: Very complex hardware, high power consumption

### 5. VLIW Processors

- **Characteristics**: Compiler statically schedules multiple operations into long instruction words
- **Advantages**: Simpler hardware, energy efficient
- **Disadvantages**: Heavily compiler-dependent, code bloat, poor performance on irregular code

## Pipelining

Pipelining is a fundamental technique that increases instruction throughput by overlapping the execution of multiple instructions. A basic pipeline divides instruction execution into discrete stages.

### Pipeline Stages

A classic five-stage RISC pipeline includes:

1. **Fetch (IF)**: Retrieve the instruction from memory using the Program Counter
2. **Decode (ID)**: Decode the instruction and read source operands from the register file
3. **Execute (EX)**: Perform the arithmetic or logic operation using the ALU
4. **Memory Access (MEM)**: Access memory if the instruction involves a load or store
5. **Write Back (WB)**: Write the result back to the register file

**Pipeline Diagram:**
```
Time →
Cycle:  1    2    3    4    5    6    7
Inst1: [IF] [ID] [EX] [MEM] [WB]
Inst2:      [IF] [ID] [EX] [MEM] [WB]
Inst3:           [IF] [ID] [EX] [MEM] [WB]
Inst4:                [IF] [ID] [EX] [MEM]
Inst5:                     [IF] [ID] [EX]
```

### Pipeline Hazards

Dependencies between instructions can cause hazards that prevent the pipeline from operating at full capacity.

#### Data Hazards

Occur when instructions depend on the results of previous instructions:

- **Read After Write (RAW)**: A true dependency where an instruction needs to read a value that a previous instruction writes
  ```
  ADD R1, R2, R3   # R1 = R2 + R3
  SUB R4, R1, R5   # Needs R1 from previous instruction (RAW hazard)
  ```

- **Write After Read (WAR)**: A false (name) dependency where an instruction writes to a register that a previous instruction reads
  ```
  ADD R1, R2, R3   # Reads R2
  SUB R2, R4, R5   # Writes R2 (WAR hazard in out-of-order execution)
  ```

- **Write After Write (WAW)**: A false (name) dependency where two instructions write to the same register
  ```
  ADD R1, R2, R3   # Writes R1
  SUB R1, R4, R5   # Also writes R1 (WAW hazard in out-of-order execution)
  ```

#### Structural Hazards

Occur when hardware resources are insufficient to handle the current instruction load (e.g., a single memory port shared between instruction fetch and data access).

#### Control Hazards

Occur due to the pipeline's inability to accurately predict changes in instruction flow, such as branches and jumps.

### Hazard Resolution Techniques

#### 1. Pipeline Stalls (Bubbles)

Temporarily halt the pipeline to resolve hazards by inserting NOPs:
```
ADD R1, R2, R3
NOP              # Stall
NOP              # Stall
SUB R4, R1, R5   # Now R1 is ready
```
- **Impact**: Reduces throughput, increases CPI

#### 2. Forwarding (Bypassing)

Pass the result of a previous instruction directly to a subsequent instruction without waiting for writeback:
```
Cycle:  1    2    3    4    5
ADD:   [IF] [ID] [EX] [MEM] [WB]
                  ↓ (forward from EX)
SUB:             [IF] [ID] [EX] [MEM] [WB]
```
- **Benefit**: Eliminates many stalls
- **Limitation**: Cannot eliminate all hazards (e.g., load-use hazard still requires one stall)

#### 3. Compiler Reordering

The compiler can reorder independent instructions to avoid hazards:
```
# Original (has hazard):
LW  R1, 0(R2)
ADD R3, R1, R4   # Stall needed

# Reordered (no hazard):
LW  R1, 0(R2)
SUB R5, R6, R7   # Independent instruction fills the delay slot
ADD R3, R1, R4   # Now R1 is ready
```

#### 4. Branch Prediction

Predict branch outcomes to avoid stalling the pipeline (covered in detail below).

### Pipeline Depth Optimization

The optimal number of pipeline stages balances:
- **Deeper pipelines**: Shorter cycle time (higher clock frequency) but more hazards and higher misprediction penalties
- **Shallower pipelines**: Fewer hazards and lower penalties but longer cycle time

**Typical configurations:**
- **Performance-only optimization**: 30-40 stages
- **Power-aware optimization**: 10-15 stages (modern standard)

## Branch Prediction

Branches account for approximately 20% of instructions and are a major impediment to pipeline performance. Accurate prediction is critical, especially in deep pipelines where the misprediction penalty can be 15-20 cycles.

### Branch Types

- **Conditional Branches**: Transfer control based on condition evaluation (e.g., if-else statements)
- **Unconditional Branches**: Always transfer control (e.g., goto, jump)
- **Function Calls**: Transfer control to a subroutine with expected return
- **Returns**: Transfer control back from a subroutine

### Branch Resolution

When a branch is not taken, the PC simply advances to the next instruction. If taken, an immediate value is added to the PC. The branch outcome is typically not known until the ALU stage, causing potential pipeline stalls.

### Static Branch Prediction

Makes predictions based on fixed rules, requiring no hardware state:

| Technique | Description | Pros | Cons |
|-----------|-------------|------|------|
| **Predict Always Taken** | Assumes branches always taken | Simple | Poor for forward branches |
| **Predict Always Not-Taken** | Assumes branches never taken | Simple, 88% accurate on average | High penalty on taken branches (60%) |
| **BTFNT** | Backward Taken, Forward Not Taken | Good for loops | Requires knowing branch direction |

### Dynamic Branch Prediction

Uses historical data and runtime information to make predictions.

#### Branch Prediction Hardware Structures

**Branch History Table (BHT):**
- Table that tracks recent branch outcomes
- Indexed by lower bits of PC
- Each entry contains a prediction counter

**Branch Target Buffer (BTB):**
- Cache storing target PC for taken branches
- Indexed by branch PC
- Enables zero-cycle taken branches if prediction correct
- **Structure**: Each entry contains:
  - Tag (branch PC)
  - Target PC
  - Prediction bits (from BHT)

**Pattern History Table (PHT):**
- Table of counters indexed by branch history
- Used in two-level predictors
- Each entry is typically a 2-bit saturating counter

#### 1-Bit Predictor

- **Mechanism**: Single bit storing the last outcome (0=not taken, 1=taken)
- **Pros**: Simple, works well for highly biased branches
- **Cons**: Suffers two mispredictions for every anomalous outcome (e.g., loop exit causes two mispredictions)

#### 2-Bit Saturating Counter

A more resilient predictor using four states:

```
State Machine:
   00 (Strong Not-Taken)  ←→  01 (Weak Not-Taken)
          ↓                           ↓
   11 (Strong Taken)      ←→  10 (Weak Taken)

Predict "taken" for states 10 and 11
Predict "not taken" for states 00 and 01
```

- **Pros**: More resilient to anomalies; requires two consecutive wrong outcomes to change strong prediction
- **Cons**: Slightly more hardware than 1-bit

#### Two-Level Predictors

Use history of recent branch outcomes to select a prediction counter, capturing patterns.

**Global History Register (GHR):**
- N-bit shift register recording outcomes of last N branches globally
- Updated on every branch: `GHR = (GHR << 1) | branch_outcome`

**Local History Register (LHR):**
- Separate history for each branch instruction
- Captures local branch behavior patterns

**Correlation Example:**
```c
if (a == 2) { ... }  // Branch 1
if (b == 2) { ... }  // Branch 2
if (a != b) { ... }  // Branch 3: outcome correlated with branches 1 & 2
```

An N-bit history predictor can learn patterns of length N+1 (e.g., 3-bit history can detect "NNT, NNT, NNT..." pattern).

**Cost**: Grows exponentially with history length (N bits requires 2^N counters per entry).

#### Tournament Predictors

Combine multiple predictors and use a meta-predictor to choose the best one:

- **GShare**: Global history predictor (good for correlated branches)
- **PShare**: Private/local history predictor (good for loop branches)
- **Meta-predictor**: 2-bit counter tracking which predictor is more accurate for each branch

**Advantages**: Adapts to different branch behaviors, achieving higher accuracy (95%+)

#### Return Address Stack (RAS)

A dedicated small hardware stack for predicting function returns:

- **Push**: On function call, push return address
- **Pop**: On return instruction, pop predicted target
- **Accuracy**: Very high for function calls/returns
- **Challenge**: Must identify return instructions before decode

### Predication

An alternative to branch prediction for hard-to-predict short branches:

**Mechanism**: Execute instructions from both paths, then commit only the correct path's results based on a predicate bit.

**Example:**
```c
// Original:
if (cond)
    x = a + b;
else
    x = a - b;

// Predicated:
p1 = (cond)
x = (p1) ? a + b : a - b;  // Both computed, one selected
```

**Conditional Instructions**: `MOVC` (move if condition true)

**Pros:**
- Eliminates misprediction penalties for short, unpredictable branches
- Increases scheduling flexibility

**Cons:**
- Executes more instructions (both paths)
- Requires more registers
- Less efficient for large blocks or highly biased branches
- Needs compiler and hardware support

## Instruction-Level Parallelism

**Instruction-Level Parallelism (ILP)** measures how many instructions in a program can be executed simultaneously. Exploiting ILP is central to modern high-performance processors.

### Key Concepts

#### Dependencies

**True Dependency (RAW)**: Real data dependency limiting parallel execution
```
ADD R1, R2, R3
SUB R4, R1, R5   # Must wait for R1
```

**Name Dependencies**: No real data dependency, can be resolved by renaming
- **WAR**: Write After Read
- **WAW**: Write After Write

**Control Dependency**: Execution order dictated by branches

#### Techniques to Exploit ILP

1. **Pipelining**: Overlap instruction stages
2. **Superscalar Execution**: Multiple execution units for concurrent instruction execution
3. **Out-of-Order Execution**: Execute instructions as soon as operands are available
4. **Register Renaming**: Eliminate name dependencies by mapping to physical registers
5. **Branch Prediction**: Reduce control dependencies
6. **Speculative Execution**: Execute instructions before certainty, rollback if wrong

### Calculating ILP

**Steps:**
1. Rename registers to remove false dependencies
2. "Execute" the program to determine when instructions can actually run
3. ILP = Number of instructions / Number of cycles required

**Example:**
```
Original:
ADD R1, R2, R3    # Cycle 1
ADD R1, R1, R4    # Cycle 2 (depends on previous)
SUB R5, R6, R7    # Cycle 1 (independent!)
MUL R8, R5, R9    # Cycle 2 (depends on SUB)

After renaming and analysis:
Instructions: 4
Cycles: 2
ILP = 4/2 = 2.0
```

## Out-of-Order Execution

Out-of-order (OOO) execution allows independent instructions to proceed while dependent ones wait, maximizing resource utilization.

### Register Renaming

Eliminates false dependencies (WAR, WAW) by mapping architectural registers to a larger set of physical registers.

**Register Allocation Table (RAT)**: Tracks the mapping from architectural to physical registers, allowing multiple "versions" of each architectural register.

**Example:**
```
Original:                   After Renaming:
ADD R1, R2, R3             ADD P10, P2, P3
SUB R4, R1, R5  (RAW)      SUB P11, P10, P5
ADD R1, R6, R7  (WAW)      ADD P12, P6, P7   # No conflict now!
MUL R8, R1, R9             MUL P13, P12, P9
```

### Tomasulo's Algorithm

A classic hardware algorithm for dynamic scheduling and OOO execution, developed by IBM in 1967 for the IBM 360/91.

#### Components

**Reservation Stations (RS):**
- Buffers holding instructions waiting for operands
- Each functional unit (ALU, load/store, multiply) has dedicated RSs
- Store instruction details: operation, source operands (or tags), destination tag

**Common Data Bus (CDB):**
- Broadcast bus where results are sent
- All RSs snoop the CDB for needed results
- Enables data forwarding without going through register file

**Register Allocation Table (RAT):**
- Maps each architectural register to either:
  - A physical register value (if ready)
  - An RS tag (if value is being computed)

#### Execution Stages

**1. Issue:**
- Fetch and decode instruction
- Check for available RS
- If available:
  - Allocate RS
  - Check operand status in RAT:
    - If ready: copy value to RS
    - If not ready: copy producing RS tag to RS
  - Update RAT to point to this RS for the destination

**2. Dispatch (Execute):**
- When all operands are available in an RS
- Dispatch instruction to functional unit
- Execute the operation

**3. Write Result (Broadcast):**
- Broadcast result on CDB with RS tag
- Update waiting RSs that are listening for this tag
- Update register file
- Free the RS

**Example:**
```
Instructions:
1. MUL R1, R2, R3
2. ADD R4, R1, R5
3. SUB R6, R7, R8

Cycle 1: MUL issued to RS1, RAT[R1] = RS1
Cycle 2: ADD issued to RS2, needs R1 (tag=RS1), RAT[R4] = RS2
         SUB issued to RS3 (independent), RAT[R6] = RS3
Cycle 3: SUB completes, broadcasts on CDB
Cycle 7: MUL completes, broadcasts on CDB → RS2 captures R1
Cycle 8: ADD executes now that R1 is ready
```

### Reorder Buffer (ROB)

Modern OOO processors add a ROB to Tomasulo's algorithm to enable precise exceptions and easy recovery from branch mispredictions.

**Function:**
- Instructions allocated in-order at Issue stage
- Results written to ROB out-of-order as they complete
- Instructions committed in-order from ROB head
- Only at commit are results written to architectural register file

**ROB Entry Contains:**
- Instruction type
- Destination register
- Result value (when ready)
- Exception status

**Benefits:**

1. **Precise Exceptions**: Exception handled only when faulting instruction reaches ROB head
2. **Speculative Execution**: Wrong-path instructions can be discarded by flushing ROB
3. **Architectural State Preservation**: Architectural registers always reflect committed state

**Execution Flow:**
- **Issue**: In-order, allocate ROB entry
- **Execute/Writeback**: Out-of-order, write to ROB
- **Commit**: In-order, update architectural state

### Memory Ordering

OOO execution extends to memory operations through the Load/Store Queue (LSQ).

**Load/Store Queue (LSQ):**
- Holds pending load and store instructions in program order
- Tracks memory addresses to detect dependencies

**Operations:**

**Store-to-Load Forwarding:**
- If a load matches a pending store address in the LSQ
- Data forwarded directly from store entry to load
- Bypasses memory, satisfies RAW dependency

**Speculative Load Execution:**
- Aggressive designs allow loads to execute before all prior store addresses are known
- If a dependency is later discovered (address collision)
- Recovery triggered: re-execute the load and all dependent instructions

**LSQ Process:**
1. **Issue**: Load/store allocated in LSQ with address calculation
2. **Dependency Checking**: Check for address matches in LSQ
3. **Execution**: Load from memory/cache or forward from store queue
4. **Commit**: Stores commit in-order, writing to memory

## Compiler Optimizations

Compilers play a vital role in exposing ILP for hardware to exploit.

### 1. Instruction Scheduling

Reorder instructions to separate dependent instructions and fill pipeline stalls:

```c
// Original (poor scheduling):
LW  R1, 0(R2)
ADD R3, R1, R4    # Stall: waiting for R1

// Optimized (good scheduling):
LW  R1, 0(R2)
SUB R5, R6, R7    # Independent instruction fills delay slot
ADD R3, R1, R4    # R1 now ready
```

May require changing register destinations or address offsets to maintain correctness.

### 2. Loop Unrolling

Replicate the loop body to perform multiple iterations' work in a single iteration:

```c
// Original:
for (i = 0; i < 100; i++)
    a[i] = a[i] + b[i];

// Unrolled by 4:
for (i = 0; i < 100; i += 4) {
    a[i]   = a[i]   + b[i];
    a[i+1] = a[i+1] + b[i+1];
    a[i+2] = a[i+2] + b[i+2];
    a[i+3] = a[i+3] + b[i+3];
}
```

**Benefits:**
- Reduces loop overhead (fewer branches and counter updates)
- Increases instruction pool for scheduling
- Exposes more ILP

**Drawbacks:**
- Code bloat
- Requires handling remainder iterations

### 3. Function Inlining

Replace function call with the function body:

```c
// Original:
int square(int x) { return x * x; }
int result = square(5);

// Inlined:
int result = 5 * 5;
```

**Benefits:**
- Eliminates call/return overhead
- Enables better cross-procedural optimization
- More instructions available for scheduling

**Drawbacks:**
- Significant code bloat if applied to large functions
- Increased instruction cache pressure

### 4. Tree Height Reduction

Restructure associative operations to reduce critical path length:

```c
// Original (height = 3):
result = a + b + c + d;
// Computed as: ((a + b) + c) + d

// Optimized (height = 2):
result = (a + b) + (c + d);
// Two additions can execute in parallel
```

**Benefits:**
- Shortens dependency chains
- Exposes more parallelism

**Requirements:**
- Associative operations (addition, multiplication)
- Floating-point requires relaxed IEEE compliance

## Processor Architectures

Different architectures balance hardware complexity and compiler dependency to achieve high IPC (Instructions Per Cycle).

### Comparison

| Architecture | Hardware Complexity | Compiler Dependency | Performance | Power Efficiency |
|--------------|---------------------|---------------------|-------------|------------------|
| **In-Order Superscalar** | Low-Medium | High | Moderate | High |
| **OOO Superscalar** | Very High | Low | Very High | Low |
| **VLIW** | Low | Very High | High (regular code) | Very High |

### Out-of-Order Superscalar

**Key Features:**
- Dynamic scheduling (Tomasulo's algorithm)
- Register renaming
- Reorder Buffer (ROB)
- Multiple issue per cycle

**Advantages:**
- High performance on general-purpose, irregular code
- Hides instruction latencies
- Adapts to runtime behavior

**Disadvantages:**
- Very complex and expensive hardware (reservation stations, large instruction windows)
- High power consumption
- Diminishing returns at high issue widths

**Examples**: Intel Core, AMD Ryzen, Apple M-series

### In-Order Superscalar

**Key Features:**
- Multiple issue per cycle
- Maintains program order
- Simpler than OOO
- Relies on compiler scheduling

**Advantages:**
- Lower power consumption
- Simpler hardware
- Lower cost

**Disadvantages:**
- Performance limited by first stalled instruction (RAW dependency)
- Heavily compiler-dependent
- Poor performance on irregular code

**Examples**: Early ARM processors, some embedded processors

### VLIW (Very Long Instruction Word)

**Key Features:**
- Compiler statically bundles multiple operations into one long instruction
- No hardware dependency checking
- No dynamic scheduling
- Explicit parallelism

**Instruction Format:**
```
[ OP1 | OP2 | OP3 | OP4 ]  ← Single VLIW instruction
  ALU   MEM   ALU   Branch
```

**Advantages:**
- Simple, low-cost hardware
- Energy-efficient
- Excellent performance on regular code (loops, arrays, DSP)
- Compiler has global view for optimization

**Disadvantages:**
- Heavily compiler-dependent
- Code bloat (NOPs when parallelism unavailable)
- Poor performance on irregular code
- Variable latencies (cache misses) hurt performance
- Binary compatibility issues

**Examples**: TI DSPs, Intel Itanium (EPIC variant), some VLIW GPUs

### EPIC (Explicitly Parallel Instruction Computing)

An evolution of VLIW with additional features:
- **Predication**: Conditional execution support
- **Speculation**: Explicit speculative load instructions
- **Rotating Register Files**: Hardware support for loop unrolling

**Example**: Intel Itanium (commercially unsuccessful despite technical sophistication)

## Multi-Core Systems

To continue scaling performance beyond single-core limits, modern processors integrate multiple cores on a single chip.

### Architectural Models (Flynn's Taxonomy)

Most multi-core processors are **MIMD** (Multiple Instruction, Multiple Data), where each core can execute different instructions on different data.

#### Shared Memory Architectures

All cores share a single physical address space.

**Uniform Memory Access (UMA):**
- All cores have equal latency to all memory locations
- Simple programming model
- **Limitation**: Does not scale beyond ~16 cores due to memory bandwidth contention
- **Example**: Typical desktop/laptop multi-core CPUs

**Non-Uniform Memory Access (NUMA):**
- Memory physically distributed among cores/sockets
- Each core has faster access to its "local" memory
- Remote memory access is slower
- **Advantage**: Better scalability (hundreds of cores)
- **Requirement**: OS awareness to place data near the using core
- **Example**: Multi-socket server systems

#### Distributed Memory (Message Passing)

Each core has private memory; communication via explicit messages over a network.
- **Advantage**: Highly scalable (thousands of nodes)
- **Disadvantage**: Explicit data distribution and communication management
- **Example**: HPC clusters, supercomputers

### Multi-Core Benefits

1. **Thread-Level Parallelism**: Different cores execute different threads
2. **Power Efficiency**: Multiple slower cores can be more power-efficient than one fast core
3. **Thermal Distribution**: Spread heat across chip
4. **Fault Tolerance**: Core isolation improves reliability

### Multi-Core Challenges

1. **Programming Complexity**: Parallel programming is difficult
2. **Amdahl's Law**: Serial portions limit speedup
3. **Cache Coherence**: Maintaining consistent view of memory (covered in [03-Memory-Systems.md](03-Memory-Systems.md))
4. **Synchronization Overhead**: Locks and barriers add overhead
5. **Power Budget**: Total chip power divided among cores

### Key Design Decisions

**Homogeneous vs. Heterogeneous:**
- **Homogeneous**: All cores identical (easier programming, flexible)
- **Heterogeneous**: Different core types (e.g., big.LITTLE, performance + efficiency cores)

**Number of Cores vs. Core Complexity:**
- **Few complex cores**: Better single-thread performance
- **Many simple cores**: Higher throughput for parallel workloads

**Cache Hierarchy:**
- **Private L1/L2**: Low latency, no coherence overhead
- **Shared L3**: Reduced capacity misses, enables core communication

## References

This document synthesizes processor design principles from:

- **Georgia Institute of Technology** - OMSCS CS 6200 and CS 6210 graduate courses
- **Columbia University** - Graduate Computer Science courses
- Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach* (6th ed.). Morgan Kaufmann
- Smith, J. E., & Sohi, G. S. (1995). "The Microarchitecture of Superscalar Processors." *Proceedings of the IEEE*, 83(12), 1609-1624
- Tomasulo, R. M. (1967). "An Efficient Algorithm for Exploiting Multiple Arithmetic Units." *IBM Journal of Research and Development*, 11(1), 25-33

For related topics, see:
- [01-Fundamentals.md](01-Fundamentals.md) - Basic architecture and ISA concepts
- [03-Memory-Systems.md](03-Memory-Systems.md) - Cache design and memory hierarchy
- [05-GPU-Architecture.md](05-GPU-Architecture.md) - GPU design and SIMT execution
