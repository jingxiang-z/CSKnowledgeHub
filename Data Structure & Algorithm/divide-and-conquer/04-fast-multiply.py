"""
Fast Integer Multiplication (Karatsuba) - Divide and Conquer

PROBLEM DESCRIPTION
===================
Given two large integers, multiply them efficiently. The standard grade-school
multiplication algorithm takes O(n²) time for n-digit numbers. Karatsuba's algorithm
uses divide and conquer to achieve better asymptotic complexity.

Example: 1234 * 5678 = 7006652


ALGORITHM DESCRIPTION
=====================
- **Base case**: If the numbers are small enough (single bit or small threshold), multiply directly
- **Divide**: Split each number at the midpoint into high and low bit halves: x = x_high*2^(n/2) + x_low, y = y_high*2^(n/2) + y_low
- **Conquer**: Recursively compute three products: p1 = x_high * y_high, p2 = x_low * y_low, p3 = (x_high + x_low) * (y_high + y_low)
- **Combine**: Compute result = p1*2^n + (p3 - p1 - p2)*2^(n/2) + p2 (using bit shifts for efficiency)
- **Return value**: The product of x and y


CORRECTNESS JUSTIFICATION
==========================
- Splitting numbers and recursively multiplying works because x*y = (x_high*2^(n/2) + x_low)*(y_high*2^(n/2) + y_low), which expands to the standard multiplication formula
- The Karatsuba trick uses (x_high + x_low)*(y_high + y_low) = x_high*y_high + x_high*y_low + x_low*y_high + x_low*y_low, which contains all four products we need
- We only need 3 multiplications because p3 - p1 - p2 gives us x_high*y_low + x_low*y_high, eliminating the need for two separate multiplications


RUNTIME ANALYSIS
================
Recurrence: T(n) = 3T(n/2) + O(n)

- Three recursive calls on half-sized numbers: 3T(n/2)
- O(n) work for splitting numbers and combining results (addition and shifting)
- Master Theorem: a = 3, b = 2, f(n) = O(n), so log_b(a) = log_2(3) ≈ 1.585
- Since f(n) = O(n^1) and 1 < 1.585, Case 1 applies
- Total: O(n^log_2(3)) ≈ O(n^1.585)

Comparison: Naive multiplication O(n²) requires 4 recursive calls, Karatsuba O(n^1.585) needs only 3

Space: O(log n) for recursion stack depth
"""
