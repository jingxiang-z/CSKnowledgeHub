# Vertex Cover

## Problem Statement

In a graph G = (V, E), a vertex cover is a subset S ⊆ V such that for every edge (u, v) ∈ E, at least one of u or v is in S — every edge is "touched" by S.

The **decision version** asks: given G and integer k, does G contain a vertex cover of size ≤ k?

## Reduction

We show Vertex Cover is NP-complete by proving (1) it is in NP, and (2) Independent Set reduces to it in polynomial time.

### NP Membership

Given a candidate set S ⊆ V, verify two conditions: (1) check that |S| ≤ k by counting vertices in S — O(|S|) ≤ O(n); (2) for every edge (u, v) ∈ E, check that u ∈ S or v ∈ S — O(m) ≤ O(n²). Both checks run in polynomial time, so Vertex Cover is in NP.

### Input Transformation

Given an Independent Set instance (G = (V, E), k), pass **(G, n − k)** as the Vertex Cover instance — the same graph with target size n − k, where n = |V|.

**Time complexity**: The graph is reused unchanged; computing n − k takes **O(1)**.

### Output Transformation

If Vertex Cover returns a vertex cover C of size ≤ n − k in G, return S = V \ C as the independent set. Computing the set difference takes **O(n)**.

### Correctness

The proof relies on one key equivalence: **S ⊆ V is an independent set in G if and only if V \ S is a vertex cover in G.**

*Proof of equivalence*: Suppose S is an IS. For any edge (u, v) ∈ E, S contains at most one of u, v (since S has no edges), so the other endpoint must be in V \ S — every edge is covered. Conversely, suppose V \ S is a VC. For any two vertices u, v ∈ S, neither is in V \ S; if (u, v) ∈ E the cover would require u or v to be in V \ S — contradiction — so no such edge exists and S is an IS.

**Forward direction (IS → VC):**

Suppose G has an independent set S of size ≥ k. By the equivalence above, V \ S is a vertex cover of G. Its size is n − |S| ≤ n − k. So G has a vertex cover of size ≤ n − k.

**Backward direction (VC → IS):**

Suppose G has a vertex cover C of size ≤ n − k. By the equivalence above, V \ C is an independent set of G. Its size is n − |C| ≥ n − (n − k) = k. So G has an independent set of size ≥ k.

## Conclusion

Vertex Cover is in NP (polynomial-time verifier above), and Independent Set — already shown NP-complete — reduces to it in polynomial time (O(1) transformation). Therefore **Vertex Cover is NP-complete**.
