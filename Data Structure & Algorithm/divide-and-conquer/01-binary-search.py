"""
Binary Search

PROBLEM DESCRIPTION
===================
Given a sorted array of integers and a target value, find the index of the target
in the array. Return -1 if the target is not found.

Example: arr = [1, 3, 5, 7, 9, 11, 13, 15]\, target = 7  →  Output: 3


ALGORITHM DESCRIPTION
=====================
- **Base case**: If left > right, the search range is empty, return -1
- **Divide**: Calculate the midpoint mid = left + (right - left) / 2 to split the search range
- **Conquer**: Compare target with arr[mid]: if equal, return mid; if target < arr[mid], recursively search the left subproblem [left, mid-1]; if target > arr[mid], recursively search the right subproblem [mid+1, right]
- **Combine**: No combine step needed—the result from the single recursive call is returned directly
- **Return value**: Either the index where target is found, or -1 if not found


CORRECTNESS JUSTIFICATION
==========================
- The sorted property allows us to eliminate half the search space with certainty
  at each step (if target < arr[mid], it cannot be in the right half)
- The search range shrinks by half each time, guaranteeing we reach the base case
- When left > right, we've exhausted all possible locations where target could be,
  correctly concluding it doesn't exist


RUNTIME ANALYSIS
================
Recurrence: T(n) = T(n/2) + O(1)

- Only one subproblem per level (search either left OR right, not both)
- O(1) work per level (comparison and arithmetic)
- log n levels until we reach a single element
- Total: O(log n) time

Space: O(log n) for recursive version (recursion stack depth), O(1) for iterative version
"""
