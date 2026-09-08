# Clique

## Problem Statement

In a graph G = (V, E), a clique is a subset S which each pair of the vertices are connected by an edge

Dicision version: given graph G and integer k, does G contain a clique of size >= k

## Reduction

### NP Membership

Given a candidate set S ⊆ V, verify two conditions: (1) check that |S| ≥ k by counting vertices in S — O(|S|) ≤ O(n); (2) check that every pair of vertices in S shares an edge — O(|S|²) ≤ O(n²). Both checks run in polynomial time, so Clique is in NP.

### Input Transformation

Given a graph G = (V, E) as input to the independent set problem and an integer k

Construct the complement graph G̅ = (V, Ē) where Ē = { (u, v) : u ≠ v and (u, v) ∉ E }. Pass (G̅, k) as the Clique instance.

**Time complexity**: Enumerating all C(n,2) pairs and checking membership in E takes **O(n²)** time.

### Output Transformation

If Clique returns a set S̄ ⊆ V of size ≥ k in G̅, return S̄ as-is — it is the independent set in G. No translation needed because the vertex sets of G and G̅ are identical. **O(1)**.

### Correctness

**Forward direction (IS → Clique):**

Suppose G has an independent set S of size ≥ k. Take any two distinct vertices u, v ∈ S. Because S is an independent set, (u, v) ∉ E. By the complement construction, (u, v) ∈ Ē. Since u and v were arbitrary, every pair of vertices in S is connected in G̅ — so S is a clique of size ≥ k in G̅.

**Backward direction (Clique → IS):**

Suppose G̅ has a clique S̄ of size ≥ k. Take any two distinct vertices u, v ∈ S̄. Because S̄ is a clique in G̅, (u, v) ∈ Ē. By the complement construction, (u, v) ∉ E. Since u and v were arbitrary, no two vertices in S̄ share an edge in G — so S̄ is an independent set of size ≥ k in G.

## Conclusion

Clique is in NP (polynomial-time verifier above), and Independent Set — already shown NP-complete — reduces to it in polynomial time (O(n²) complement construction). Therefore **Clique is NP-complete**.
