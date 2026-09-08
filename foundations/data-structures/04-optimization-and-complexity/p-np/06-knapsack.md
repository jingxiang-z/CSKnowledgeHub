# Knapsack (0/1, decision)

## Problem Statement

You are given \(n\) items. Item \(i\) has **weight** \(w_i > 0\) and **value** \(v_i > 0\). You also have a **capacity** \(W\) and a **value target** \(V\). Each item may be chosen **at most once** (0/1 knapsack).

The **decision version** asks: does there exist a subset \(S \subseteq \{1,\ldots,n\}\) such that \(\sum_{i \in S} w_i \le W\) and \(\sum_{i \in S} v_i \ge V\)?

## Reduction

We show 0/1 Knapsack is NP-complete by proving (1) it is in NP, and (2) Subset Sum reduces to it in polynomial time (as in `00-p-np.md`: Subset Sum → Knapsack).

### NP Membership

Given a candidate subset \(S\), compute \(\sum_{i \in S} w_i\) and \(\sum_{i \in S} v_i\), then check \(\le W\) and \(\ge V\). There are \(O(|S|) \le O(n)\) additions; each runs in time polynomial in the bit lengths of the inputs. So Knapsack is in NP.

### Input Transformation

Given a Subset Sum instance — integers \(a_1,\ldots,a_n\) and target \(t\) — build a Knapsack instance:

- For each item \(i\), set **\(w_i = a_i\)** and **\(v_i = a_i\)** (value equals weight).
- Set **capacity** \(W = t\) and **value target** \(V = t\).

**Time complexity**: Copy \(n\) weights/values and two scalars — **\(O(n)\)**.

### Output Transformation

If Knapsack answers YES, return YES for Subset Sum (the same subset \(S\) works). If Knapsack answers NO, return NO. Forwarding the decision is **\(O(1)\)**; listing \(S\) is **\(O(n)\)**.

### Correctness

With \(v_i = w_i = a_i\), every subset satisfies **total value = total weight**.

**Forward direction (Subset Sum → Knapsack):**

If \(\sum_{i \in S} a_i = t\), then \(\sum_{i \in S} w_i = t \le W\) and \(\sum_{i \in S} v_i = t \ge V\). So Knapsack answers YES.

**Backward direction (Knapsack → Subset Sum):**

If some \(S\) satisfies \(\sum_{i \in S} w_i \le W\) and \(\sum_{i \in S} v_i \ge V\) with \(W = V = t\) and \(w_i = v_i = a_i\), then \(\sum_{i \in S} a_i \le t\) and \(\sum_{i \in S} a_i \ge t\). Hence \(\sum_{i \in S} a_i = t\). So Subset Sum answers YES.

## Conclusion

Knapsack is in NP (polynomial-time verifier above), and Subset Sum — NP-complete — reduces to it in polynomial time. Therefore **the 0/1 Knapsack decision problem is NP-complete**.
