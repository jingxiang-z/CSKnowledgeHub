# Subset Sum

## Problem Statement

Given integers \(a_1, a_2, \ldots, a_n\) and a target \(t\), the **decision version** asks: is there a subset \(S \subseteq \{1,\ldots,n\}\) such that \(\sum_{i \in S} a_i = t\)?

## Reduction

We show Subset Sum is NP-complete by proving (1) it is in NP, and (2) 3-SAT reduces to it in polynomial time

### NP Membership

A certificate is a subset of indices \(S\) (or the multiset of chosen integers). Verify by summing the corresponding \(a_i\) and comparing to \(t\). There are at most \(n\) terms; each addition and the final comparison run in time polynomial in the **bit length** of the input (the size of the numbers), not in the numeric value of \(t\) alone. So Subset Sum is in NP.

### Input Transformation

Let the 3-SAT instance have variables \(x_1,\ldots,x_n\) and clauses \(C_1,\ldots,C_m\), each with at most three literals.

Pick an integer base \(B > 3\) (for example \(B = 10\), or any \(B \ge 4\) so that clause-column totals up to 3 do not carry into other digit positions). Think of each number as having **\(n + m\)** “digit positions” in base \(B\): positions \(1,\ldots,n\) correspond to variables, and positions \(n+1,\ldots,n+m\) correspond to clauses.

For each variable \(x_i\) (\(i = 1,\ldots,n\)), create two numbers:

- **\(T_i\)** (“\(x_i\) is true”): \(B^{i-1}\) plus \(B^{n+j-1}\) for every clause \(C_j\) in which the literal \(x_i\) appears.
- **\(F_i\)** (“\(x_i\) is false”): \(B^{i-1}\) plus \(B^{n+j-1}\) for every clause \(C_j\) in which the literal \(\neg x_i\) appears.

For each clause \(C_j\) (\(j = 1,\ldots,m\)), create two **slack** numbers that are **only** nonzero in clause position \(n+j\):

- **\(S_{j,1} = S_{j,2} = B^{n+j-1}\)** (two identical copies; both may be used in the subset sum).

Set the target

\[
t \;=\; \sum_{i=1}^{n} B^{i-1} \;+\; 3\sum_{j=1}^{m} B^{n+j-1}.
\]

The multiset of Subset Sum inputs is \(\{T_1,F_1,\ldots,T_n,F_n\} \cup \{S_{j,1},S_{j,2} : 1 \le j \le m\}\), with target \(t\).

**Time complexity**: For each literal occurrence we may add one power of \(B\) to a number; total work is \(O(n + m)\) additions of values whose bit length is \(O((n+m)\log B)\), i.e. **polynomial** in the size of the 3-SAT instance.

### Output Transformation

If Subset Sum answers YES, recover a satisfying assignment: for each \(i\), exactly one of \(T_i, F_i\) appears in the solution (see correctness below). Set \(x_i\) to true if \(T_i\) is chosen, false if \(F_i\) is chosen. This takes **\(O(n)\)**.

If Subset Sum answers NO, report that the 3-SAT instance is unsatisfiable.

### Correctness

**Key idea.** Variable digit \(i\) forces **exactly one** of \(T_i, F_i\) into any valid subset summing to \(t\), so every solution encodes a truth assignment. Clause digit \(n+j\) must sum to \(3\): literals chosen under that assignment contribute the number of true literals in \(C_j\) (0 to 3), and the two slack numbers for clause \(j\) contribute 0, 1, or 2. Together they can reach \(3\) **if and only if** at least one literal of \(C_j\) is true.

**Forward direction (3-SAT → Subset Sum):**

Suppose we have a satisfying assignment. For each \(i\), include \(T_i\) if \(x_i\) is true, else include \(F_i\). For each clause \(C_j\), let \(r_j \in \{1,2,3\}\) be the number of true literals in \(C_j\) under this assignment (at least 1). In digit \(n+j\), the chosen variable numbers contribute \(r_j\). Include \(3 - r_j\) of the two slack numbers \(S_{j,1}, S_{j,2}\) (possible since \(r_j \ge 1 \Rightarrow 3-r_j \in \{0,1,2\}\)). Then each variable digit \(i\) sums to \(1\) and each clause digit \(n+j\) sums to \(r_j + (3-r_j) = 3\), so the total equals \(t\).

**Backward direction (Subset Sum → 3-SAT):**

Suppose some subset sums to \(t\).

1. **Variable digits:** For fixed \(i\), only \(T_i\) and \(F_i\) have a nonzero coefficient on \(B^{i-1}\), and each has coefficient 1. The target has coefficient 1 in that digit, so **at most one** of \(T_i, F_i\) can be chosen — and to reach 1, **exactly one** is chosen. Define \(x_i\) true if \(T_i\) is chosen, false if \(F_i\) is chosen.

2. **Clause digits:** In digit \(n+j\), only numbers associated with clause \(j\) contribute: the literals of \(C_j\) (each at most 1) and the two slack copies (each 0 or 1). So the digit sum is in \(\{0,\ldots,3\}\) from literals plus \(\{0,1,2\}\) from slack, and the target digit is 3. If no literal of \(C_j\) is true under the assignment from step 1, literal contribution is 0 and slack can contribute at most 2 — impossible. Hence **at least one literal in \(C_j\) is true**, for every \(j\).

Therefore the 3-SAT instance is satisfiable.

## Conclusion

Subset Sum is in NP (polynomial-time verifier above), and 3-SAT — NP-complete — reduces to it in polynomial time. Therefore **Subset Sum is NP-complete**.
