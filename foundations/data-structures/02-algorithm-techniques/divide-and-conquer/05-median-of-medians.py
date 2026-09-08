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

def find_median_of_small_group(arr, left, right):
    """
    Find the median of a small array segment by sorting it.
    Used for groups of 5 elements in the median-of-medians algorithm.

    Args:
        arr: The array
        left: Start index (inclusive)
        right: End index (inclusive)

    Returns:
        The median value of arr[left:right+1]
    """
    # Extract the segment and sort it
    segment = sorted(arr[left:right+1])
    # Return the middle element (median)
    return segment[len(segment) // 2]


def median_of_medians(arr, left, right, k):
    """
    Find the kth smallest element in arr[left:right+1] using the median-of-medians algorithm.
    Guarantees O(n) worst-case time by choosing a good pivot deterministically.

    Args:
        arr: Array to search
        left: Start index (inclusive)
        right: End index (inclusive)
        k: Find the kth smallest element (1-indexed)

    Returns:
        The kth smallest element in arr[left:right+1]
    """
    n = right - left + 1

    # Base case: if array is small enough, just sort and return kth element
    if n <= 5:
        segment = sorted(arr[left:right+1])
        return segment[k-1]

    # Step 1: Divide array into groups of 5 and find median of each group
    medians = []
    for i in range(left, right + 1, 5):
        # Get the end of this group (either i+4 or right, whichever is smaller)
        group_right = min(i + 4, right)
        # Find median of this group and add to medians list
        median = find_median_of_small_group(arr, i, group_right)
        medians.append(median)

    # Step 2: Recursively find the median of medians to use as pivot
    # This is the key insight: the median of medians is a good pivot
    num_medians = len(medians)
    if num_medians == 1:
        pivot = medians[0]
    else:
        # Recursively find median of the medians array
        pivot = median_of_medians(medians, 0, num_medians - 1, (num_medians + 1) // 2)

    # Step 3: Partition the array into three groups
    lows = []   # Elements < pivot
    mids = []   # Elements == pivot
    highs = []  # Elements > pivot

    for i in range(left, right + 1):
        if arr[i] < pivot:
            lows.append(arr[i])
        elif arr[i] == pivot:
            mids.append(arr[i])
        else:
            highs.append(arr[i])

    # Step 4: Determine which partition contains the kth smallest element
    low_size = len(lows)
    mid_size = len(mids)

    if k <= low_size:
        # kth smallest is in the lows partition
        return median_of_medians(lows, 0, low_size - 1, k)
    elif k <= low_size + mid_size:
        # kth smallest is the pivot itself
        return pivot
    else:
        # kth smallest is in the highs partition
        # Adjust k by subtracting elements we've eliminated
        new_k = k - low_size - mid_size
        return median_of_medians(highs, 0, len(highs) - 1, new_k)


def find_kth_smallest(arr, k):
    """
    Public interface for finding the kth smallest element using median-of-medians.

    Args:
        arr: Array of integers
        k: Find the kth smallest element (1-indexed, k=1 means smallest)

    Returns:
        The kth smallest element, or None if k is out of bounds

    Time complexity: O(n) worst-case
    Space complexity: O(n) for auxiliary arrays in partition step
    """
    if k < 1 or k > len(arr):
        return None

    # Create a copy to avoid modifying the original array
    arr_copy = arr.copy()
    return median_of_medians(arr_copy, 0, len(arr_copy) - 1, k)


if __name__ == "__main__":
    # Test case 1: Find 2nd smallest
    arr1 = [3, 2, 1, 5, 6, 4]
    k1 = 2
    result1 = find_kth_smallest(arr1, k1)
    print(f"Test 1 - Find {k1}nd smallest:\n"
          f"  Array: {arr1}\n"
          f"  Result: {result1}\n"
          f"  Expected: 2 (sorted: [1, 2, 3, 4, 5, 6])\n")

    # Test case 2: Find median (middle element)
    arr2 = [12, 3, 5, 7, 19, 26, 11, 8, 14]
    k2 = 5  # Middle element of 9 elements
    result2 = find_kth_smallest(arr2, k2)
    print(f"Test 2 - Find {k2}th smallest (median):\n"
          f"  Array: {arr2}\n"
          f"  Result: {result2}\n"
          f"  Expected: 11 (sorted: [3, 5, 7, 8, 11, 12, 14, 19, 26])\n")

    # Test case 3: Find smallest element (k=1)
    arr3 = [7, 10, 4, 3, 20, 15]
    k3 = 1
    result3 = find_kth_smallest(arr3, k3)
    print(f"Test 3 - Find {k3}st smallest (minimum):\n"
          f"  Array: {arr3}\n"
          f"  Result: {result3}\n"
          f"  Expected: 3\n")

    # Test case 4: Find largest element (k=n)
    arr4 = [7, 10, 4, 3, 20, 15]
    k4 = len(arr4)
    result4 = find_kth_smallest(arr4, k4)
    print(f"Test 4 - Find {k4}th smallest (maximum):\n"
          f"  Array: {arr4}\n"
          f"  Result: {result4}\n"
          f"  Expected: 20\n")

    # Test case 5: Larger array with duplicates
    arr5 = [9, 7, 5, 5, 3, 3, 1, 8, 6, 4, 2]
    k5 = 6
    result5 = find_kth_smallest(arr5, k5)
    print(f"Test 5 - Array with duplicates:\n"
          f"  Array: {arr5}\n"
          f"  k: {k5}\n"
          f"  Result: {result5}\n"
          f"  Expected: 5 (sorted: [1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9])\n")

    # Test case 6: Invalid k (out of bounds)
    arr6 = [5, 2, 8]
    k6 = 10
    result6 = find_kth_smallest(arr6, k6)
    print(f"Test 6 - Invalid k:\n"
          f"  Array: {arr6}\n"
          f"  k: {k6}\n"
          f"  Result: {result6}\n"
          f"  Expected: None")
