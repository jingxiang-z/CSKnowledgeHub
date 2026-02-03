"""
Median of Medians - Divide and Conquer

PROBLEM DESCRIPTION
===================
Given an unsorted array of integers and an integer k, find the kth smallest element
in the array in guaranteed O(n) worst-case time. The Median of Medians algorithm
(also known as BFPRT) achieves this by selecting a good pivot deterministically,
unlike QuickSelect which can degrade to O(n²) with poor pivot choices.

Example: arr = [3, 2, 1, 5, 6, 4], k = 2  →  Output: 2 (the 2nd smallest element)


ALGORITHM DESCRIPTION
=====================
- **Base case**: If the array has only 1 element, return that element
- **Divide**: Split the array into groups of 5 elements, sort each group, and collect the median of each group to form a medians array
- **Find pivot**: Recursively call fast_select on the medians array to find the median of medians, which serves as a good pivot
- **Partition**: Partition the array into three groups: elements less than pivot (lows), equal to pivot (mids), and greater than pivot (highs)
- **Conquer**: Based on k and the sizes of lows and mids, recursively search in either lows or highs, or return the pivot if k falls in the mids range
- **Return value**: The kth smallest element


CORRECTNESS JUSTIFICATION
==========================
- Dividing into groups of 5 and finding their medians ensures the median-of-medians is a good pivot that eliminates at least 30% of elements per iteration
- After partitioning, we know exactly which group contains the kth smallest: if k ≤ lowSize, it's in lows; if k > lowSize + midSize, it's in highs (adjusted); otherwise it's the pivot itself
- This deterministic pivot selection guarantees we never have the worst-case O(n²) scenario of regular QuickSelect, achieving O(n) worst-case time


RUNTIME ANALYSIS
================
Recurrence: T(n) = T(n/5) + T(7n/10) + O(n)

- T(n/5): Recursive call on medians array (n/5 medians from n/5 groups)
- T(7n/10): Recursive call on at most 70% of the array (guaranteed by median-of-medians)
- O(n): Work for grouping, finding medians, and partitioning
- Total: O(n) worst-case time

Space: O(log n) for recursion stack in average case, O(n) worst case for the auxiliary arrays
"""
