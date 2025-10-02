## Processor Design

### Workflow

1. **Define the ISA**:
   - Determine the set of instructions, data types, addressing modes, and architectural features.

2. **Design the Data Path**:
   - Create the components necessary to execute instructions, such as ALUs, registers, multiplexers, and buses.

3. **Design the Control Unit**:
   - Develop the logic to generate control signals based on the decoded instructions.

4. **Implement Pipelining**:
   - Divide the instruction execution into stages and design mechanisms to handle pipeline hazards.

5. **Design the Memory Hierarchy**:
   - Plan the organization of registers, cache levels, and main memory for efficient data access.

6. **Simulate and Verify**:
   - Use simulation tools to verify the functionality and performance of the design. Debug and optimize as necessary.

7. **Physical Design**:
   - Translate the logical design into a physical layout for fabrication. This includes placement, routing, and timing analysis.

8. **Fabrication and Testing**:
   - Manufacture the processor and perform extensive testing to ensure it meets design specifications and performance targets.

### Types

1. **Single-Cycle Processors**:
   - Each instruction is executed in a single clock cycle.
   - Simple design but may have a long clock cycle to accommodate the slowest instruction.

2. **Multi-Cycle Processors**:
   - Instructions are broken down into multiple stages, with each stage executed in a separate clock cycle.
   - Allows for a shorter clock cycle but increases the complexity of the control unit.

3. **Pipelined Processors**:
   - Instructions are divided into stages, and multiple instructions are overlapped in execution.
   - Improves throughput but requires handling pipeline hazards.

4. **Superscalar Processors**:
   - Capable of executing multiple instructions simultaneously by having multiple execution units.
   - Requires sophisticated instruction scheduling and hazard detection.

5. **Out-of-Order Processors**:
   - Instructions are executed out of order to optimize resource usage and improve performance.
   - Relies on complex hardware for instruction reordering and dependency checking.

## Pipelining

Pipelining in processor design is a technique used to increase the instruction throughput (the number of instructions that can be executed in a unit of time) of a CPU. It does this by dividing the execution process into several stages, with each stage handling a different part of the instruction.

### Stages

1. **Fetch (IF)**: Retrieve the instruction from memory.
2. **Decode (ID)**: Decode the instruction to understand what actions are needed.
3. **Execute (EX)**: Perform the arithmetic or logic operation.
4. **Memory Access (MEM)**: Access memory if the instruction involves a memory read or write.
5. **Write Back (WB)**: Write the result of the instruction back to the register file.

### Hazards

- **Structural Hazards**: Occur when hardware resources are insufficient to handle the current instruction load.
- **Data Hazards:** Occur when instructions depend on the results of previous instructions that have not yet completed.
  - **Read After Write (RAW)**: An instruction needs to read a register that a previous instruction is writing to.
  - **Write After Read (WAR)**: An instruction needs to write to a register that a previous instruction is reading from.
  - **Write After Write (WAW)**: An instruction needs to write to a register that a previous instruction is also writing to.
- **Control Hazards**: Occur due to the pipeline’s inability to accurately predict changes in the instruction flow, such as branches and jumps.

### Hazards Handling

1. **Pipeline Stalls**: Temporarily halting the pipeline to resolve hazards.
2. **Forwarding (Bypassing)**: Passing the result of a previous instruction directly to a subsequent instruction that needs it.
3. **Branch Prediction**: Predicting the outcome of branches to minimize control hazards.
4. **Out-of-Order Execution**: Allowing instructions to be executed out of order when there are no dependencies, improving efficiency.

## Branches

### Types

- **Conditional Branches**: Instructions that transfer control based on the evaluation of a condition (e.g., `if-else` statements).
- **Unconditional Branches**: Instructions that transfer control unconditionally (e.g., `goto`, `jump`).
- **Function Calls**: Instructions that transfer control to a subroutine and expect a return (e.g., `call` in assembly language).
- **Returns**: Instructions that transfer control back from a subroutine to the calling function.

### Branch Prediction

If a branch is not taken the PC just advances to the next instruction. If the branch is taken the immediate value is added to the PC to advance to the new destination. It is not known until the end of the ALU stage whether the branch is taken or not. It is better to make a prediction, then the processor is at least right some of the time.

1. **Static Branch Prediction**: Makes a prediction based on fixed rules.
   - **Predict Always Taken**: Assumes branches will always be taken.
   - **Predict Always Not Taken**: Assumes branches will never be taken.
   - **Backward Taken, Forward Not Taken (BTFNT)**: Assumes backward branches (loops) are taken, and forward branches (conditionals) are not taken.
2. **Dynamic Branch Prediction**: Uses historical data and runtime information to make predictions.
   - **One-Level (Single-Level) Predictors**: Use a single history table to record the outcomes of recent branches.
     - **1-bit predictor:** A 1-bit predictor is a simple dynamic branch prediction technique that uses a single bit to record whether the last occurrence of a branch was taken or not, predicting the same outcome for the next occurrence.
     - **2-bit predictor:** A 2-bit predictor is a dynamic branch prediction method that uses a 2-bit state machine to track the behavior of a branch over multiple executions, allowing it to be more accurate by requiring two consecutive mispredictions before changing its prediction
   - **Two-Level Predictors:** Two-Level Predictors are advanced branch prediction mechanisms that use two levels of history information to make more accurate predictions about branch behavior.
     - **Global History Register (GHR) or Local History Register (LHR)**:
       - **GHR**: Records the outcomes of the most recent branches globally, providing a global history.
       - **LHR**: Records the outcomes of branches for a specific branch instruction, providing a local history.
     - **Pattern History Table (PHT) or Multiple Pattern History Tables (MPHT)**:
       - **PHT**: A table of counters indexed by the history registers (GHR or LHR).
       - **MPHT**: Multiple tables, where each table is associated with a different history pattern.
   - **Hybrid Predictors**: Combine multiple prediction strategies to improve accuracy.
     - **Tournament Predictor:** A tournament predictor is an advanced branch prediction mechanism that combines multiple branch predictors and dynamically selects the most accurate one for each branch using a meta-predictor to enhance overall prediction accuracy.
     - **Hierarchical Predictor:** A hierarchical predictor combines a highly accurate primary predictor with a secondary, less accurate predictor, updating the primary predictor only when the secondary predictor is incorrect, to improve overall branch prediction accuracy efficiently.

### Branch Prediction Mechanisms

- **Branch History Table (BHT)**:
  - **Description**: A table that keeps track of the outcomes of recent branches using simple predictors like 1-bit or 2-bit counters.
  - **Function**: Used to predict the direction of a branch (taken or not taken).
  - **Structure**: Each entry in the BHT corresponds to a specific branch or a set of branches, indexed typically by the least significant bits (LSB) of the branch address (Program Counter, PC).
- **Pattern History Table (PHT)**:
  - **Description**: A table of counters indexed by a history of branch outcomes, used in two-level predictors.
  - **Function**: Stores the patterns of branch history to improve prediction accuracy.
  - **Structure**: Entries are often 2-bit saturating counters indexed by a combination of global or local history registers.
- **Global History Register (GHR)**:
  - **Description**: A shift register that keeps a global history of the outcomes of recent branches (taken or not taken).
  - **Function**: Provides a history pattern used to index into the PHT.
  - **Structure**: Typically a bit vector where each bit represents the outcome of a recent branch (1 for taken, 0 for not taken).
- **Local History Register (LHR)**:
  - **Description**: Registers that keep track of the outcomes of branches for specific branch instructions.
  - **Function**: Used in local history predictors to capture the behavior of individual branches.
  - **Structure**: Each branch instruction has its own LHR, which is a bit vector similar to the GHR but specific to that branch.
- **Branch Target Buffer (BTB)**:
  - **Description**: A cache that stores the target addresses of recently executed branches.
  - **Function**: Provides the target address for branches predicted to be taken, reducing the need to recompute branch targets.
  - **Structure**: Entries are indexed by the branch address (PC) and include the target address and possibly other information such as the branch type and prediction history.
- **Return Address Stack (RAS)**:
  - **Description**: A stack structure used to predict the return address for function calls.
  - **Function**: Helps in predicting the return address of function calls to avoid pipeline stalls.
  - **Structure**: A stack that stores the return addresses of recently executed function calls, with push and pop operations corresponding to call and return instructions.
- **Meta-Predictor**:
  - **Description**: A predictor used in tournament predictors to choose between multiple branch predictors.
  - **Function**: Selects the most accurate predictor for a given branch based on past performance.
  - **Structure**: Typically a table of counters or another data structure that tracks the performance of different predictors.

### Predication

**Predication** is a technique used in computer architecture to eliminate or reduce the need for conditional branches, thereby improving the flow of instructions in the pipeline and enhancing overall performance. Instead of using traditional branching, predication converts conditional code into a series of instructions that are conditionally executed based on a predicate.

1. **Predicate Registers**:
   - Special registers, known as predicate registers, are used to store boolean values (`true` or `false`).
   - These values determine whether a particular instruction should be executed.
2. **Conditional Execution**:
   - Each instruction in the predicated code is associated with a predicate.
   - The instruction is executed only if the predicate evaluates to `true`.
   - If the predicate is `false`, the instruction is effectively a no-op (no operation).

## Instruction Level Parallelism

**Instruction-Level Parallelism (ILP)** is a measure of how many of the instructions in a computer program can be executed simultaneously. The concept of ILP is central to modern high-performance processors, which aim to maximize the parallel execution of instructions to improve performance.

### Key Concepts in ILP

1. **Parallel Execution**:
   - **True (Data) Dependency**: When one instruction depends on the result of a previous instruction. This limits parallel execution.
   - **Name Dependency**: Occurs when instructions use the same register or memory location, but there's no actual data dependency. These can be resolved by renaming techniques.
   - **Control Dependency**: Arises from the execution order dictated by control instructions like branches.
2. **Techniques to Exploit ILP**:
   - **Pipelining**: Breaks down instruction execution into stages (fetch, decode, execute, etc.) so multiple instructions can be processed concurrently at different stages.
   - **Superscalar Execution**: Uses multiple execution units to execute more than one instruction per clock cycle.
   - **Out-of-Order Execution**: Instructions are executed as soon as their operands are available, rather than strictly in the order they appear in the program.
   - **Register Renaming**: Solves name dependencies by providing unique identifiers to each instance of a register.
   - **Branch Prediction**: Reduces control dependencies by predicting the outcomes of branches and pre-fetching instructions accordingly.
   - **Speculative Execution**: Executes instructions before the certainty of their execution is known, rolling back if the speculation was incorrect.

### Steps

1. Rename registers as they are used, keeping track of which registers are still free for assignment. 
2. “Execute” the program to make sure the false dependencies are removed and determine when the instructions are executed. 
3. Then it is the number of instructions / the number of cycles required to execute the instructions.

## Instruction Scheduling

### Tomasulo's Algorithm

1. **Instruction Issue**:
   - Instructions are fetched and decoded. If there is an available reservation station for the required functional unit, the instruction is issued and the operands are checked.
   - If an operand is not available, a tag representing the producing instruction is stored instead.
2. **Execution**:
   - Once all operands are available (either immediately or after being produced by earlier instructions), the instruction can be executed.
   - The execution units execute instructions independently and in parallel, as soon as their operands are ready.
3. **Write Result**:
   - After execution, the result is broadcast on the Common Data Bus (CDB) to all reservation stations and the register file.
   - Reservation stations waiting for this result can now proceed with their execution.

### Issue

1. **Instruction Fetch and Decode**:
   - The instruction is fetched from the instruction queue and decoded to understand its type (e.g., ADD, SUB, MUL) and the operands involved.
2. **Check for Available Reservation Station**:
   - The algorithm checks if there is an available reservation station corresponding to the functional unit required for the instruction (e.g., ALU, load/store unit).
   - If no reservation station is available, the instruction cannot be issued and must wait in the instruction queue.
3. **Register Renaming and Operand Status Check**:
   - The algorithm renames the destination and source registers to avoid false dependencies (WAR, WAW) using a technique called register renaming.
   - It checks the status of the source operands:
     - If the operand is ready (i.e., it has been computed and stored in a register), it is copied to the reservation station.
     - If the operand is not ready (i.e., it is still being computed by a previous instruction), a tag representing the producing instruction is copied to the reservation station.
4. **Placing the Instruction in the Reservation Station**:
   - The instruction is placed into an appropriate reservation station along with its operands (or tags for pending operands).
   - The reservation station entry includes:
     - The operation to be performed.
     - Source operands (or their tags if not yet available).
     - The destination register tag.

### Execution

1. **Instruction Execution**:
   - The dispatched instructions are executed by the corresponding functional units.
   - Each functional unit performs the operation specified by the instruction (e.g., addition, multiplication, memory access).
2. **Handling Execution Latency**:
   - Different instructions have different execution latencies. Some operations (like integer addition) may complete in a single cycle, while others (like floating-point multiplication) may take multiple cycles.
   - The functional unit keeps track of the progress and ensures the instruction completes its execution.
3. **Result Generation**:
   - Once the execution is complete, the result of the operation is produced.
   - This result will be used to update the reservation stations, register files, and any other dependent instructions.
4. **Readiness for Write-Back**:
   - After the result is generated, it is prepared to be broadcast on the Common Data Bus (CDB) in the write-back stage.
   - The instruction execution completes when the result is ready to be communicated to other parts of the processor.

### Write Results

1. **Result Broadcasting**:
   - The results of executed instructions are broadcast on the Common Data Bus (CDB).
   - This broadcast allows multiple units to receive the results simultaneously.
2. **Update Reservation Stations**:
   - Reservation stations listening to the CDB update their entries with the received results.
   - Instructions waiting for these results can now proceed to the execution stage if they were stalled.
3. **Update Register File**:
   - The physical register file is updated with the results.
   - Register renaming tables are also updated to reflect the new values.
4. **Instruction Completion**:
   - Instructions are marked as completed once their results are written back.
   - This completion frees up resources such as reservation stations and physical registers for new instructions.

### ReOrder Buffer

A **Reorder Buffer (ROB)** is a hardware structure used in modern out-of-order processors to ensure the correct execution of instructions and maintain precise exceptions. It allows instructions to be executed out-of-order while committing their results in the original program order, thereby preserving the logical flow of the program.

1. **Issue Stage**:
   - When an instruction is issued, an entry is allocated in the ROB, and the instruction's destination register is renamed to point to this entry.
2. **Execution Stage**:
   - The instruction is executed out-of-order as soon as its operands are available. Upon completion, the result is written to the ROB entry.
3. **Commit Stage**:
   - Instructions at the head of the ROB are checked for completion. If the instruction has finished execution and there are no exceptions, its result is committed to the architectural state (register file or memory).
4. **Exception Handling**:
   - If an exception or interrupt occurs, the ROB allows the processor to discard instructions that have not been committed and restore the state to the point of the exception.

- Fetch, Decode, Issue are all in order ­ this ensures dependencies are done in order 

- Execute and Write can be done out of order 

- Commit is done in­order

### Memory Ordering

- **Instruction Issue**:

  - Load and store instructions are issued to the LSQ and allocated an entry.

  - The LSQ records the instruction's address and status.

- **Address Calculation**:
  - The effective memory address for the load or store instruction is calculated, often involving the addition of a base address and an offset.

- **Dependency Checking**:

  - For Loads
    - Check the store queue for any pending stores to the same address.
    - If a match is found, the load instruction may have to wait until the store completes.
    - If the data is available from a previous store in the queue, it can be forwarded directly to the load instruction.

  - For Stores
    - Check for any pending loads from the same address to ensure that the correct data is loaded.
    - The store instruction may wait until previous loads and stores to the same address are resolved.

- **Execution**:

  - Load instructions read data from the memory hierarchy or the store queue.

  - Store instructions write data to the memory hierarchy or update the store queue.

- **Commitment**:

  - Instructions commit in program order to ensure correct memory ordering.

  - The LSQ ensures that speculative memory operations do not affect the final program state unless they are confirmed to be correct.

## Compiler Parallelism

### Tree Height Reduction

1. **Balancing the Tree**:
   - Transform the tree into a more balanced form where the height is minimized.
   - This often involves rearranging the computation order and possibly introducing additional temporary variables.
2. **Associative Operations**:
   - Tree height reduction takes advantage of the associative property of certain operations (e.g., addition and multiplication).
   - Associativity allows for the reordering of operations without changing the result, which is crucial for balancing the tree.

### Loop Unrolling

1. **Replicate Loop Body**: The loop body is replicated multiple times within a single iteration. For example, if the loop is unrolled by a factor of 4, the body of the loop is repeated 4 times.
2. **Adjust Loop Control**: The loop counter and condition are adjusted to account for the increased number of operations per iteration. This may involve reducing the number of iterations of the loop by a factor equal to the unroll factor.
3. **Handle Remainder Iterations**: If the number of iterations of the original loop is not a multiple of the unroll factor, additional code (often called a cleanup loop) is added to handle the remaining iterations that do not fit into the unrolled loop.

### Function Call Inlining

1. **Function Call Overhead**: Traditional function calls involve overhead due to the need to pass arguments, set up a stack frame, perform a jump to the function's code, and handle the return to the caller.
2. **Inlining**: Inlining replaces the function call with the body of the function, thereby eliminating the call overhead and allowing further optimizations within the calling function.
3. **Inlining Criteria**: Compilers typically decide to inline a function based on factors like the size of the function, the frequency of calls, and the complexity of the function.

## VLIW

**Very Long Instruction Word (VLIW)** is a computer architecture design that aims to improve performance by exploiting instruction-level parallelism (ILP) at the compiler level rather than relying on complex hardware mechanisms. In a VLIW architecture, multiple operations are packed into a single long instruction word, allowing the processor to execute them in parallel.

1. **Instruction Packing**:
   - In VLIW, each instruction word contains multiple operations that can be executed simultaneously. These operations are independent and can utilize different functional units in parallel.
2. **Compiler Responsibility**:
   - The compiler is responsible for analyzing the program's instruction stream, identifying independent operations, and packing them into VLIW instructions.
   - This shifts the complexity from hardware to the compiler, simplifying the processor design but requiring advanced compiler techniques.
3. **Parallel Execution**:
   - Each VLIW instruction can include multiple operations, such as arithmetic, memory access, and branching, which are executed in parallel by different functional units within the processor.

