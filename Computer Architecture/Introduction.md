# Introduction

## Computer Architecture

### Components

1. **Central Processing Unit (CPU)**: The CPU is the brain of the computer, responsible for executing instructions.
   - **Arithmetic Logic Unit (ALU)**: Performs arithmetic and logical operations.
   - **Control Unit (CU)**: Directs the operation of the processor by decoding instructions and generating control signals.
   - **Registers**: Small, fast storage locations used for temporary data storage and manipulation.
   - **Cache**: A small, fast memory located close to the CPU to speed up access to frequently used data.
   
2. **Memory Hierarchy**:
   - **Registers**: The fastest and smallest type of memory, located within the CPU.
   - **Cache Memory**: Provides faster data access to the CPU by storing frequently accessed data. It is typically divided into levels (L1, L2, L3) with L1 being the fastest and smallest.
   - **Main Memory (RAM)**: Volatile memory used to store data and instructions currently being processed by the CPU.
   - **Secondary Storage**: Non-volatile storage used for long-term data storage, such as hard drives and SSDs.

3. **Input/Output (I/O) Devices**: Devices that facilitate interaction between the computer and the external environment.
   - **Input Devices**: Keyboards, mice, scanners.
   - **Output Devices**: Monitors, printers, speakers.
   - **Storage Devices**: Hard drives, SSDs, USB drives.
   
4. **Bus Systems**: Communication pathways that transfer data between different components of a computer.
   - **Data Bus**: Carries data between the CPU, memory, and I/O devices.
   - **Address Bus**: Carries the addresses of data (but not the data itself) to be accessed.
   - **Control Bus**: Carries control signals from the control unit to other components.

### Workflow

1. **Fetch**:
   - The CPU uses the program counter (PC) to fetch the next instruction from main memory.
   - The instruction is transferred via the address and data buses.

2. **Decode**:
   - The fetched instruction is decoded by the control unit to determine the required operation and operands.

3. **Execute**:
   - The ALU performs the required arithmetic or logical operation.
   - The control unit generates the necessary control signals for data movement.

4. **Memory Access**:
   - If the instruction involves memory access (e.g., load/store), the data is read from or written to memory.
   - This step involves interaction between the CPU, main memory, and possibly the cache.

5. **Write Back**:
   - The result of the execution is written back to the appropriate register or memory location.

## Instruction Set Architecture

### Components

1. **Instructions**:
   - **Operation Codes (Opcodes)**: The portion of a machine language instruction that specifies the operation to be performed.
   - **Instruction Types**:
     - **Arithmetic and Logical Instructions**: Perform mathematical calculations and logical operations (e.g., ADD, SUB, AND, OR).
     - **Data Transfer Instructions**: Move data between memory and registers or between registers (e.g., LOAD, STORE, MOV).
     - **Control Flow Instructions**: Change the sequence of instruction execution (e.g., JUMP, CALL, RETURN, BRANCH).
     - **Special Instructions**: Specific to the architecture, such as system calls and no-operation (NOP).

2. **Data Types**:
   - Defines the types of data the ISA can handle, such as integer, floating-point, character, and more complex types like vectors and matrices.

3. **Registers**:
   - **General Purpose Registers (GPRs)**: Used for a wide variety of operations.
   - **Special Purpose Registers**: Used for specific functions like the Program Counter (PC), Stack Pointer (SP), and Status Register.

4. **Addressing Modes**:
   - Methods to specify operands for instructions.
   - **Immediate**: Operand is a constant within the instruction itself.
   - **Direct**: Address of the operand is specified in the instruction.
   - **Indirect**: Address of the operand is held in a register or memory location.
   - **Register**: Operand is located in a register.
   - **Indexed**: Effective address is computed by adding an index to a base address.

5. **Memory Architecture**:
   - Defines the memory model, including address space, data alignment, and the relationship between main memory and cache.

6. **Interrupt and Exception Handling**:
   - Mechanisms for handling unexpected events or conditions, such as hardware interrupts or software exceptions.

7. **External I/O**:
   - Methods for the processor to communicate with external devices, often involving specific instructions for input and output operations.

### Types

1. **CISC (Complex Instruction Set Computing)**:
   - Characterized by a large number of complex instructions.
   - Example: x86 architecture.
   - Pros: Can perform complex operations with fewer instructions, potentially reducing the number of instructions per program.
   - Cons: Complex instruction decoding and execution, which can limit clock speed and increase power consumption.

2. **RISC (Reduced Instruction Set Computing)**:
   - Emphasizes a small, highly optimized set of instructions.
   - Example: ARM, MIPS architecture.
   - Pros: Simplifies instruction decoding, allowing for higher clock speeds and more efficient pipelining.
   - Cons: May require more instructions to perform complex tasks, placing greater demands on the compiler.

3. **VLIW (Very Long Instruction Word)**:
   - Encodes multiple operations in a single, long instruction word.
   - Example: Itanium architecture.
   - Pros: Can exploit instruction-level parallelism explicitly, simplifying the hardware.
   - Cons: Increased complexity in the compiler and potential inefficiency in handling variable instruction latencies.

4. **EPIC (Explicitly Parallel Instruction Computing)**:
   - Similar to VLIW but with additional features to manage parallelism and dependencies.
   - Example: Intel Itanium.

### Assembly Language

Here is a simple MIPS assembly program that adds two numbers and prints the result.

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

### Explanation

#### Data Section
```assembly
.data
    num1:   .word 5
    num2:   .word 10
    result: .word 0
```
- **.data**: This directive indicates the beginning of the data segment, where variables and constants are defined.
- **num1**: A label for a word (32-bit integer) with an initial value of 5.
- **num2**: A label for a word with an initial value of 10.
- **result**: A label for a word that will store the result of the addition, initialized to 0.

#### Text Section
```assembly
.text
    .globl main
main:
```
- **.text**: This directive indicates the beginning of the code segment, where the instructions are located.
- **.globl main**: This directive makes the `main` label globally accessible, indicating that it is the entry point of the program.
- **main**: The label for the main function, marking the start of the executable instructions.

#### Instructions
```assembly
    lw    $t0, num1
    lw    $t1, num2
    add   $t2, $t0, $t1
    sw    $t2, result
```
- **lw $t0, num1**: `lw` stands for "load word". This instruction loads the 32-bit value from the memory location labeled `num1` into register `$t0`.
- **lw $t1, num2**: Loads the 32-bit value from the memory location labeled `num2` into register `$t1`.
- **add $t2, $t0, $t1**: Adds the values in registers `$t0` and `$t1` and stores the result in register `$t2`.
- **sw $t2, result**: `sw` stands for "store word". This instruction stores the 32-bit value from register `$t2` into the memory location labeled `result`.

#### System Calls
```assembly
    li    $v0, 1
    lw    $a0, result
    syscall
```
- **li $v0, 1**: `li` stands for "load immediate". This instruction loads the immediate value `1` into register `$v0`. In the context of MIPS system calls, `1` is the code for printing an integer.
- **lw $a0, result**: Loads the value from the memory location labeled `result` into register `$a0`, which is used as an argument for the print integer system call.
- **syscall**: This instruction makes a system call. The type of system call is determined by the value in `$v0`. Since `$v0` contains `1`, the system call will print the integer in `$a0`.

```assembly
    li    $v0, 10
    syscall
```
- **li $v0, 10**: Loads the immediate value `10` into register `$v0`. In the context of MIPS system calls, `10` is the code for exiting the program.
- **syscall**: Makes the system call to exit the program.

## Performance

### Speed

- Throughput is the amount of work or data processed by a system in a given amount of time.
- Latency is the time it takes to complete a single task or operation from start to finish

- Speedup: N = Speed(X) / Speed(Y) = Throughput(X) / Throughput(Y) = Latency(Y) / Latency(X)
  - Speedup < 1 : The performance has gotten worse with the newer version. The degradation is because of worse performance. 
  - Speedup > 1: The performance has gotten better with the newer version. The improvement is through shorter execution time or with Higher Throughput.
- Benchmarks: Benchmarks are standard tasks for measuring processor performance. A benchmark is a suite of programs that represent common tasks.
  - Real Applications: ­ most realistic, most difficult to set up ­ used for real machine comparisons. 
  - Kernels: ­ most time consuming part of an application, is still difficult to set up, ­ used for prototypes. 
  - Synthetic:­ similar to kernels, but simpler to compile, used for design studies Peak performance, ­used for marketing.
- Iron Law of performance: The Iron Law of Processor Performance provides a fundamental framework for understanding the factors that influence a processor's performance
  - **Instruction Count (IC)**: The total number of instructions executed by a program
  - **Cycles Per Instruction (CPI)**: The average number of clock cycles each instruction takes to execute.
  - **Clock Cycle Time (T)**: The duration of a single clock cycle, inversely proportional to the clock frequency (f).

$$
Execution Time=Instruction Count×Cycles Per Instruction×Clock Cycle Time
$$

- Amdahl's Law: Amdahl's Law is used to find the maximum improvement possible in a system when only part of the system is improved
  - $S$ is the theoretical maximum speedup.
  - $P$ is the proportion of the program that can be parallelized.
  - $N$ is the number of processors or cores.

$$
S=\frac{1}{1-P+\frac{P}{N}}
$$

- Lhadma’s Law: While trying to make the common case fast, do not make the uncommon case worse.

### Power Consumption

- **Dynamic Power:** Dynamic power is the power consumed by a processor due to the charging and discharging of capacitors during the switching of transistors. It occurs only when the processor is actively performing computations.
  - **Clock Frequency (f)**: Higher frequencies increase dynamic power because more switching events occur per unit time.
  - **Supply Voltage (V)**: Power consumption increases quadratically with voltage. Reducing the voltage significantly decreases dynamic power.
  - **Capacitance (C)**: Larger or more complex circuits have higher capacitance, increasing dynamic power.
  - **Activity Factor (α)**: More active transistors lead to higher power consumption.

$$
P_{dynamic} = \alpha C V^2 f
$$

- **Static Power:** Static power, also known as leakage power, is the power consumed by a processor even when it is not actively switching. It is due to leakage currents that flow through the transistors when they are in the off state.

  - **Supply Voltage (V)**: lower voltages increased static power.

  - **Temperature**: Higher temperatures can exacerbate leakage currents, increasing static power consumption.

  - **Transistor Size**: As transistor sizes decrease with advanced fabrication technologies, leakage currents become more significant.


- **Trade-offs:** lowering the supply voltage reduces dynamic power, it can lead to increased leakage currents and higher static power consumption

### Fabrication Cost

Fabrication Cost include the cost of manufacturing and the cost of defective parts. The larger the die the higher the percentage of defective parts. 

Fabrication Yield = number of working chips / number of chips on the wafer
