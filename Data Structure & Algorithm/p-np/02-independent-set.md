# Independent Set

## Problem Statement

In a graph G=(V, E), an independent set is a subset of vertices S such that no two vertices in S are connected by an edge.

The **decision version** asks: given G and integer k, does G contain an independent set of size ≥ k?

## Reduction

We show Independent Set is NP-complete by proving (1) it is in NP, and (2) 3-SAT reduces to it in polynomial time.

### NP Membership

Given a candidate set S ⊆ V, we verify two conditions: (1) check that |S| ≥ k by counting vertices in S, which takes O(n) time; (2) check that no two vertices in S share an edge by examining every pair, which takes O(|S|²) ≤ O(n²) time. Both checks run in polynomial time, so Independent Set is in NP.

### Input Transformation

The input for 3-SAT consists of n variables x₁, x₂, ..., xₙ and m clauses C₁, C₂, ..., Cₘ, each containing at most 3 literals, joined by AND.

Construct graph G = (V, E) as follows:

- **Vertices**: For each literal in clause Cⱼ, create one vertex. Since each clause has at most 3 literals and there are m clauses, |V| ≤ 3m.
- **Clause edges**: For each clause Cⱼ, add an edge between every pair of vertices within that clause. This prevents the independent set from selecting more than one literal per clause.
- **Variable edges**: For each variable xᵢ, add an edge between every vertex representing xᵢ and every vertex representing ¬xᵢ. This prevents the independent set from selecting a literal and its negation simultaneously.

Set the target independent set size to **k = m**. The question becomes: does G have an IS of size ≥ m?

**Time complexity**: Creating vertices is O(m). Clause edges add at most 3 edges per clause → O(m). Consistency edges connect occurrences of xᵢ to occurrences of ¬xᵢ across all clauses; in the worst case this is O(m²). Overall: **O(m²)**.

### Output Transformation

If Independent Set outputs an IS S of size ≥ m, iterate over every vertex in S, read the literal it represents, and set that variable accordingly; set any uncovered variable arbitrarily. This scan takes **O(|S|) = O(m)** time.

### Correctness

**Forward direction (3-SAT → IS):**

Suppose the 3-SAT instance has a satisfying assignment. Since every clause is satisfied, at least one literal per clause is true. Pick exactly one true literal from each clause; let S be the set of their corresponding vertices. Then:

1. |S| = m = k.
2. S contains no two vertices from the same clause, so no clause edge exists within S.
3. S cannot contain both a vertex for xᵢ and a vertex for ¬xᵢ, because the assignment sets each variable to a single value — so no variable edge exists within S.

Therefore S is a valid independent set of size k.

**Backward direction (IS → 3-SAT):**

Suppose G has an independent set S of size ≥ m. Since clause edges connect every pair of vertices within the same clause, S contains **at most one vertex per clause** — so |S| ≤ m. Combined with |S| ≥ m, we get |S| = m, and S contains **exactly one vertex per clause**. Then:

1. S contains exactly one vertex per clause (shown above).
2. Since variable edges connect xᵢ-vertices to ¬xᵢ-vertices, S cannot contain both — so the literals in S are mutually consistent.
3. Assign each variable xᵢ to true if a vertex for xᵢ appears in S, to false if a vertex for ¬xᵢ appears in S, and arbitrarily otherwise.
4. Every clause has exactly one vertex in S, and that literal is set to true by the assignment, so every clause is satisfied.

Therefore the 3-SAT instance is satisfiable.
