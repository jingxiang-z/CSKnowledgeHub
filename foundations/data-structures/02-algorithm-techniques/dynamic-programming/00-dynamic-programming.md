# Dynamic Programming

## Introduction

Dynamic Programming (DP) is a fundamental algorithm design paradigm that solves complex problems by breaking them down into simpler overlapping subproblems and storing their solutions to avoid redundant computation. The key insight is that many problems have overlapping subproblems that are solved multiple times, and DP exploits this overlap by computing each subproblem only once and storing the result.

**Core Principles:**
1. **Define Subproblems**: Identify how to break the problem into smaller, related subproblems
2. **Store Solutions**: Use a table to store solutions to subproblems (no recursion or memoization in pure DP)
3. **Build Bottom-Up**: Solve smaller subproblems first, using their solutions to build up to the final answer
4. **Extract Result**: Retrieve the final answer from the computed table

## Key Characteristics

### Optimal Substructure
- The optimal solution to the problem can be constructed from optimal solutions of its subproblems
- This property is necessary but not sufficient for dynamic programming
- Enables building solutions incrementally from smaller subproblems

### Overlapping Subproblems
- The same subproblems are solved multiple times during naive recursive computation
- DP eliminates this redundancy by storing solutions to subproblems
- Each unique subproblem is computed exactly once and reused as needed

### Bottom-Up Construction
- Solutions are built iteratively from smaller subproblems to larger ones
- Table entries are filled in a specific order that ensures dependencies are satisfied
- No recursion is used in the implementation (distinguishes DP from memoization)

## Essential Components of a DP Solution

A complete dynamic programming solution consists of three required sections. These components form the standard format for presenting and evaluating DP solutions in academic and professional contexts.

### (a) Subproblem Definition

The subproblem definition articulates what each table entry represents in plain language.

**Requirements:**
- Always build on a subset of the input (e.g., `A[1..i]`)
- Conceptually defined against "previous" subproblems, not the entire input
- Expressed using words: "T(i,j) is the ..."
- Should use terminology from the problem statement without redefining meanings
- May or may not require inclusion of the last element

**Inclusion Constraint:**
- Phrases like "which includes A[i]", "ending at A[i]", or "which includes i" mean element `A[i]` must be used in the subproblem output
- This is distinct from the range of indices `[1..i]` considered for the subproblem

### (b) Recurrence Relation

The recurrence relation provides a mathematical definition of how table entries relate to each other.

**Requirements:**
1. **Mathematical notation only** - no programming constructs, no pseudocode
2. **Single mathematical definition** - the table gets one definition for all entries
3. **Recursive to smaller subproblems** - each entry defined using previously computed entries
4. **Well-defined references** - any referenced entry must have a definition
5. **No self-reference** - cannot define `T(i)` using `T(i)` itself
6. **Include base cases** - with their applicable bounds clearly specified
7. **Provide bounds for all variables** - scoped to where they are used
8. **Focus on table definitions** - not on the final return value

**Important Notes:**
- Bounds convey directionality of table fill
  - `0 ≤ i ≤ n` suggests left-to-right fill order
  - `n ≥ i ≥ 0` suggests right-to-left fill order (for suffix-based approaches)
- Each table entry can be defined only once (no contradictions)
- All referenced entries must be well-defined before use
- Helper indices can be added to access ranges of previous entries

**Common Pitfalls to Avoid:**

❌ **Self-referential definition:**
```
T(i) = max{T(i), T(i-1)+1}  // WRONG: T(i) on both sides
```

✅ **Correct definition:**
```
T(i) = max{T(j)+1}, 0 ≤ j < i  // Uses helper index j
```

❌ **Pseudocode constructs:**
```
for i = 1 to n: T(i) = T(i-1) + 1  // WRONG: for loop
if i ≥ 1: T(i) = ...              // WRONG: if statement (control flow)
```

✅ **Conditional mathematical notation:**
```
T(i) = T(i-1) + 1,     if A[i] > A[i-1]
     = 1,              otherwise

where 1 ≤ i ≤ n
```

❌ **Overlapping base cases and recurrence:**
```
Base: T(i) = 0, 0 ≤ i ≤ n
Recurrence: T(i) = T(i-1)+1, 1 ≤ i ≤ n  // WRONG: T(1)..T(n) defined twice
```

✅ **Mutually exclusive bounds:**
```
Base: T(0) = 0
Recurrence: T(i) = T(i-1)+1, 1 ≤ i ≤ n
```

### (c) Implementation Analysis

This section analyzes the computational complexity and efficiency of the dynamic programming solution based on the recurrence relation.

#### (c.1) Number of Subproblems

State the total number of distinct subproblems (table entries) in Big-O notation.

**Examples:**
- One-dimensional table from `-1` to `n`: **O(n)**
- Two-dimensional table `T(i,j)` where `1 ≤ i ≤ n, 1 ≤ j ≤ m`: **O(n·m)**
- Three-dimensional table: **O(n·m·k)**

#### (c.2) Runtime to Fill the Table

State the worst-case time complexity to compute all table entries in Big-O notation.

**Calculation approach:**
- Identify the cost to compute one table entry
- Multiply by the number of table entries
- Simplify to Big-O notation

#### (c.3) Extracting the Final Answer

Describe how and where the final result is extracted from the completed table.

**Common patterns:**
- `T(n)` - last entry
- `T(n,m)` - bottom-right entry
- `max{T(n,*)}` or `max{T(*,*)}` - maximum value in row/table
- `sum{T(*,*)}` - sum of entries

#### (c.4) Runtime to Extract the Answer

State the time complexity to extract and return the final answer in Big-O notation.

## Problem-Solving Workflow

### Step 1: Identify the Problem Pattern
- **Sequence problems**: LIS, LCS, Maximum Subarray
- **Optimization problems**: Knapsack, Matrix Chain Multiplication
- **Counting problems**: Number of ways to reach a state
- **Interval problems**: Breaking strings/arrays into optimal intervals

### Step 2: Define the Subproblem
1. Identify what each table entry represents in plain language
2. Build on prefixes/suffixes of the input (e.g., `A[1..i]`)
3. Determine if the last element must be included
4. Use terminology from the problem statement

### Step 3: Derive the Recurrence Relation
1. Determine base case(s) - smallest directly solvable subproblems
2. Express `T(i)` or `T(i,j)` in terms of smaller subproblems
3. Handle all conditional cases
4. Specify bounds for all variables
5. Ensure no table entry is defined multiple times

### Step 4: Analyze Complexity
1. Count the number of subproblems
2. Determine cost per entry
3. Calculate total fill time
4. Identify extraction method and cost

### Step 5: Implement (If Required)
1. Initialize table with appropriate dimensions
2. Fill base cases
3. Iterate in correct order (respecting dependencies)
4. Apply recurrence relation
5. Extract final answer

## Common DP Patterns

### Linear Sequence DP
- One-dimensional table `T(i)` based on prefix `A[1..i]`
- Examples: Fibonacci, Maximum Subarray, Longest Increasing Subsequence

### Two Sequences DP
- Two-dimensional table `T(i,j)` based on prefixes of two inputs
- Examples: Longest Common Subsequence, Edit Distance

### Bounded Knapsack DP
- Table `T(i,w)` tracking items and capacity constraints
- Examples: 0/1 Knapsack, Subset Sum

### Interval DP
- Table `T(i,j)` representing solutions over intervals `[i,j]`
- Examples: Matrix Chain Multiplication, Palindrome Partitioning

## Common Pitfalls to Avoid

1. **Starting with code** - Always define subproblems and recurrence mathematically first
2. **Self-referential definitions** - `T(i)` cannot appear on both sides of the equation
3. **Pseudocode in recurrence** - No `for` loops, `if` statements as control flow
4. **Multiple table assignments** - Each entry can only be defined once
5. **Undefined references** - Ensure all referenced entries (like `T(i-2)`) have definitions
6. **Missing or overlapping bounds** - Base cases and recurrence must have mutually exclusive ranges
7. **Incomplete variable bounds** - All variables must have specified ranges

## Notation Conventions

- **Table indexing:** `T[i]` or `T(i)` (be consistent)
- **Conditions:** `if`, `otherwise`, `s.t.` (such that), `where`
- **Logical operators:** `and`, `or`, `||`, `&&`, `!`
- **Special values:** `∞` (infinity) for impossible states
- **Empty set:** `{}` or `∅`
- **Base cases:** Must be non-recursive with hard-coded values
- **Multiple tables:** Rare but valid; each needs its own definition
