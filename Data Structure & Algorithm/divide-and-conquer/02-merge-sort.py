"""
Merge Sort - Divide and Conquer

PROBLEM DESCRIPTION
===================
Given an unsorted array of integers, sort the array in ascending order.

Example: arr = [38, 27, 43, 3, 9, 82, 10]  →  Output: [3, 9, 10, 27, 38, 43, 82]


ALGORITHM DESCRIPTION
=====================
- **Base case**: If the array has 0 or 1 element, it is already sorted, return it as-is
- **Divide**: Split the array at the midpoint into left and right halves
- **Conquer**: Recursively call merge sort on both the left half and the right half
- **Combine**: Merge the two sorted halves by comparing elements from each using two pointers, building a new sorted array
- **Return value**: The merged, sorted array


CORRECTNESS JUSTIFICATION
==========================
- Dividing the problem into two independent subproblems (left and right halves) eventually reduces each to single elements, which are trivially sorted
- The merge operation correctly produces a sorted array from two sorted arrays by always selecting the smaller of the two front elements
- The base case (arrays of size ≤1 are already sorted) guarantees termination and correctness for the smallest subproblems


RUNTIME ANALYSIS
================
Recurrence: T(n) = 2T(n/2) + O(n)

- Two subproblems per level (left and right halves)
- O(n) work per level to merge the results
- O(log n) levels in the recursion tree (halving the problem size each time)
- Total: O(n log n) time

Space: O(n) for the temporary arrays used during merging
"""
