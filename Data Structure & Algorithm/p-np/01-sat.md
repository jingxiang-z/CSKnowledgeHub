# SAT

## Variables vs. Literals

A **variable** receives a truth assignment (TRUE/FALSE). A **literal** is a variable or its negation — the smallest unit in an expression.

In `(a v b v c) ^ (!a v !b)`: 3 variables (a, b, c), 5 literals (a, b, c, !a, !b).

Truth assignments belong to **variables**, not clauses or literals.

## CNF (Conjunctive Normal Form)

A CNF expression is **clauses joined by AND**, where each clause is **literals joined by OR**.

```
(a v !b) ^ (c v d) ^ (!e v a)
```

**A clause may:** contain any number of literals (including a literal and its negation like `a v !a`).

**A clause may NOT:** be empty, hardcode TRUE/FALSE, use operators other than OR, contain nested parentheses, or repeat a literal.

## SAT Complexity

Notation: **n** = number of variables, **m** = number of clauses.

| Operation | Runtime |
|---|---|
| Verify full assignment satisfies expression | O(nm) |
| Check if one clause is satisfied | O(n) |
| Add/remove a clause | O(1) |
| Remove a variable from a clause | O(n) |
| Access a variable's truth assignment | O(1) |

## Useful CNF Equivalencies

| Expression | Equivalent |
|---|---|
| `!!a` | `a` |
| `a -> b` | `!a v b` |
| `!(a ^ b)` | `!a v !b` |
| `!(a v b)` | `!a ^ !b` |

## SAT (Boolean Satisfiability Problem)

**Input:** A Boolean formula in CNF with n variables and m clauses.
**Output:** A truth assignment to the variables that satisfies all clauses, or NO if none exists.

SAT asks: *does there exist an assignment of TRUE/FALSE to the variables such that the entire CNF expression evaluates to TRUE?*

A CNF is satisfied when **every clause** has at least one TRUE literal. If even one clause has all FALSE literals, the assignment fails.

**Example:**
```
(a v !b) ^ (!a v c) ^ (b v c)
```
Assignment a=TRUE, b=TRUE, c=TRUE satisfies all three clauses → YES.
Assignment a=FALSE, b=TRUE, c=FALSE: clause 1 = (!b = FALSE, a = FALSE) → clause 1 fails → NO.

**Why SAT matters:** SAT was proven NP-Complete by the **Cook-Levin Theorem (1971/1973)** — it was the *first* problem shown to be NP-Complete. Every other NP-Complete problem is proven by reducing from SAT (directly or through a chain).

**SAT ∈ NP:** Given a candidate assignment, verify it by checking each clause in O(nm). Given an assignment to n variables and m clauses, each clause has at most n literals, so verification is O(nm).

## SAT → 3-SAT (NP-Completeness Proof)

3-SAT is a restricted version of SAT where each clause has **at most 3 literals**. We prove 3-SAT is NP-Complete by reducing from SAT.

### Part 1 — 3-SAT ∈ NP

Given an instance of 3-SAT with n variables and m clauses, and a candidate assignment to all n variables, verify the assignment by iterating through each clause and checking whether at least one literal is satisfied. Since each clause has at most 3 literals, each check is O(1), and there are m clauses, so verification runs in **O(m)** time. 3-SAT ∈ NP.

### Part 2 — Reduction: SAT → 3-SAT

**Input Transformation f:** Let c ∈ C be clauses in SAT input I, and c' ∈ C' be clauses in the 3-SAT input f(I). 3-SAT here requires at most 3 literals per clause. For each clause c ∈ C:

- **k ≤ 3:** Add c directly as c' to C'. It is already a valid 3-SAT clause.

- **k > 3** `(x1 v x2 v ... v xk)`: Introduce k−3 fresh variables y1, ..., yk-3. Replace with k−2 clauses:
  `(x1 v x2 v y1) ^ (!y1 v x3 v y2) ^ ... ^ (!yk-4 v xk-2 v yk-3) ^ (!yk-3 v xk-1 v xk)`

There are m clauses to transform, each containing at most n literals, giving a runtime of **O(mn)** which is polynomial.

**Output Transformation h:** The 3-SAT instance uses all original variables plus fresh auxiliary variables. Discard the auxiliary variable assignments and return the assignment to the original n variables as the solution to SAT. This runs in **O(n)** time.

**Correctness — 3-SAT has a solution IFF SAT has a solution:**

*(If SAT has a solution → 3-SAT has a solution):* Suppose SAT instance I has a satisfying assignment T. For k ≤ 3 clauses, c' is identical to c, so T satisfies them in f(I) directly. For a k > 3 clause, at least one original literal xi is TRUE under T. Assign yj = TRUE for all Yj before xi in the chain and FALSE after — this ensures every sub-clause contains at least one TRUE literal. Therefore T extended with these auxiliary assignments satisfies f(I).

*(If SAT has NO solution → 3-SAT has NO solution):* Suppose no assignment satisfies SAT instance I. For k ≤ 3 clauses, c' is identical to c so they are also unsatisfied in f(I). For a k > 3 clause, if all original literals x1, ..., xk are FALSE then y1 must be TRUE to satisfy `(x1 v x2 v y1)`, making !y1 FALSE in `(!y1 v x3 v y2)`, forcing y2 = TRUE, and so on. This chain propagates until the final sub-clause `(!yk-3 v xk-1 v xk)` has all literals FALSE. So without at least one original literal being TRUE, no assignment can satisfy all sub-clauses. Since no such assignment exists for SAT, no assignment satisfies f(I). Therefore 3-SAT has no solution.