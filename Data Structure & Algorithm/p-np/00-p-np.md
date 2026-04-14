# P and NP

## Overview

Complexity theory classifies problems by the resources needed to solve them. **P** and **NP** are the two most fundamental classes. The question **"Does P = NP?"** is the most famous unsolved problem in computer science.

- If **P = NP**: every problem whose solution can be verified quickly can also be *solved* quickly — cryptography as we know it would break.
- If **P ≠ NP** (widely believed): some problems are genuinely harder to solve than to verify.

## Complexity Classes

### P — Polynomial Time
Problems **solvable** by a deterministic algorithm in O(n^k) time. These are considered "efficiently solvable."

| Problem | Algorithm | Time |
|---|---|---|
| Sorting | Merge Sort | O(n log n) |
| Shortest Path | Dijkstra | O(E log V) |
| MST | Kruskal / Prim | O(E log V) |
| Max Flow | Edmonds-Karp | O(VE²) |

### NP — Nondeterministic Polynomial Time
Problems where a proposed solution (certificate) can be **verified** in polynomial time. NP is about *checking*, not necessarily *solving*.

| Problem | Certificate | Verification |
|---|---|---|
| 3-SAT | Variable assignment | Check all clauses — O(n) |
| Hamiltonian Path | Permutation of vertices | Check path validity — O(n) |
| Subset Sum | A subset | Check sum equals target — O(n) |
| TSP (decision) | A tour | Check tour cost ≤ k — O(n) |

Since any problem you can solve quickly you can also verify quickly: **P ⊆ NP**.

### NP-Hard
A problem H is NP-Hard if every problem in NP can be **polynomial-time reduced** to H — meaning H is at least as hard as any NP problem. H does not have to be in NP itself (it may not even be a decision problem).

### NP-Complete
A problem is NP-Complete if it is both **in NP** and **NP-Hard**. These are the hardest problems inside NP.

```
NP-Complete = NP ∩ NP-Hard
```

### Complexity Hierarchy

```
P ⊆ NP ⊆ PSPACE ⊆ EXP
```

*(Assuming P ≠ NP)*
```
         ┌─────────────────────────────┐
         │          NP-Hard            │
         │   ┌─────────────────────┐   │
         │   │         NP          │   │
         │   │  ┌──────────────┐   │   │
         │   │  │ NP-Complete  │   │   │
         │   │  └──────────────┘   │   │
         │   │  ┌─────┐            │   │
         │   │  │  P  │            │   │
         │   │  └─────┘            │   │
         │   └─────────────────────┘   │
         └─────────────────────────────┘
```

## NP-Completeness Proof — Full Structure

To prove unknown **Problem B** is NP-Complete you must do two things: show B ∈ NP, then show a known NP-Complete problem A reduces to B (A → B).

### Part 1 — Show B ∈ NP (Polynomial Verifier)

You are **not solving B**. You are showing that given an instance **I** and a candidate solution **S**, you can confirm S is valid in polynomial time with respect to |I|.

**What to write:**
- Describe in plain language what a candidate solution looks like.
- Walk through each check needed to confirm it is valid.
- Provide a Big-O runtime for those checks.

> **Critical:** If the problem has a goal, target, or budget (g, k, or b), your runtime must **not** depend on that value. Depending on it gives a *pseudo-polynomial* verifier, which is invalid.

**Example (3-SAT verifier):** Given a variable assignment, iterate through every clause and confirm at least one literal is satisfied. This takes O(n) where n is the number of clauses — no dependence on any target value.

### Part 2 — Reduction from Known A → Unknown B

The idea: if A (known NP-Complete) can be transformed into B, then B must be at least as hard as A. Treat B as a **black box** that returns YES/NO — do not design an algorithm for B.

The reduction has three required components:

#### a) Input Transformation (function f)
Show how to convert any instance **I** of A into an instance **f(I)** of B in polynomial time.
- Describe the mapping in detail.
- Provide a Big-O runtime.
- It must work for **any** valid instance of A — no arbitrary restrictions.
- Prefer minimal transformations; a very complex transformation usually means you picked the wrong source problem.

#### b) Output Transformation (function h)
Show how to convert B's solution **S** on input f(I) into a solution **h(S)** for the original instance I of A, in polynomial time.
- State this explicitly even if S is passed through unchanged.
- Provide a Big-O runtime.

#### c) Correctness — B has a solution IFF A has a solution

This is the heart of the proof. You must prove **both directions** of the biconditional. Choose exactly one of these four valid combinations:

| Option | Direction 1 | Direction 2 |
|---|---|---|
| **A** *(standard)* | B has solution → A has solution | A has solution → B has solution |
| **B** | B has solution → A has solution | B has NO solution → A has NO solution |
| **C** | A has NO solution → B has NO solution | A has solution → B has solution |
| **D** | A has NO solution → B has NO solution | B has NO solution → A has NO solution |

Option A (both positive directions) is the most common and usually the easiest.

**Common mistakes:**
- Proving a statement and its own contrapositive — they are logically identical, so you only proved one direction.
- Proving all four implications — correct but redundant (double the work).
- Mixing up which instance belongs to A vs B in your argument.

### Recommended Proof Layout

**Paragraph 1 — B ∈ NP:** Describe the verifier, walk through the checks, state Big-O runtime.

**Paragraph 2 — Input transformation f:** Describe how to build f(I) from I, state Big-O runtime.

**Paragraph 3 — Output transformation h:** Describe how to recover the A-solution from B's output, state Big-O runtime.

**Paragraphs 4–5 — IFF directions:** One paragraph per direction.

## Accepted Source Problems for Reductions

Pick the problem that **structurally resembles** B most closely — this minimises the transformation work.

| Problem | Core idea |
|---|---|
| **SAT** | Boolean formula: find an assignment satisfying all clauses |
| **3-SAT** | SAT where every clause has exactly 3 literals |
| **Clique** | Does the graph contain a complete subgraph of size k? |
| **Independent Set (IS)** | k vertices with no edges between them |
| **Vertex Cover (VC)** | k vertices that touch every edge in the graph |
| **Subset Sum (SSS)** | Subset of integers that sums to exactly target t |
| **Rudrata Path / (s,t)-Path / Cycle** | Hamiltonian path or cycle variants (directed graphs) |
| **ILP** | Integer solutions to a system of linear inequalities |
| **ZOE** | System of 0/1 equations |
| **3D Matching** | Perfect matching in a 3-partite hypergraph |
| **TSP** | Tour visiting all cities with total cost ≤ budget |

## Key NP-Complete Reduction Chain

SAT was the first NP-Complete problem (Cook 1971 / Levin 1973). Many others followed by reduction:

```
SAT → 3-SAT → Independent Set → Clique
                    ↓
              Vertex Cover
                    ↓
          Hamiltonian Path/Cycle → TSP

3-SAT → Subset Sum → Knapsack
```

- **3-SAT → IS**: construct a graph where each clause becomes a triangle; an independent set of size k corresponds to a satisfying assignment.
- **IS ↔ Clique**: S is an independent set in G iff S is a clique in the complement graph G̅.
- **IS ↔ Vertex Cover**: S is an independent set of size k iff V \ S is a vertex cover of size n − k.
