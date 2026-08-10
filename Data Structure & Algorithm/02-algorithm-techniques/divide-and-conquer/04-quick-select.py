"""
Quick Select - Divide and Conquer

PROBLEM DESCRIPTION
===================
Given an unsorted array of integers, find the kth smallest element in the array.

Example: arr = [38, 27, 43, 3, 9, 82, 10], k = 3  →  Output: 10 (the 3rd smallest element)
Note: The array is NOT sorted; we only find and return the kth smallest element.


ALGORITHM DESCRIPTION
=====================
- **Base case**: If the subarray has only one element, return it as the kth smallest
- **Divide**: Choose a pivot element and partition the array so that:
  - Elements smaller than or equal to the pivot are moved to the left subarray
  - Elements greater than the pivot are moved to the right subarray
  - The pivot is placed in its final sorted position at index `pivot_index`
- **Conquer**: Compare pivot position with k to decide which subarray to search:
  - If `pivot_index == k-1`: Found it! Return the pivot element
  - If `pivot_index > k-1`: The kth smallest is in the left subarray, recursively search left for kth smallest
  - If `pivot_index < k-1`: The kth smallest is in the right subarray, recursively search right for (k - pivot_index - 1)th smallest
- **Combine**: No combine step needed - we only search ONE side
- **Return value**: The kth smallest element


CORRECTNESS JUSTIFICATION
==========================
- After partitioning, the pivot is in its final sorted position at index `pivot_index`, with exactly `pivot_index` elements smaller than it
- If `pivot_index == k-1`, then the pivot is the kth smallest element by definition (k-1 in 0-indexed array)
- The partition operation correctly places all elements ≤ pivot on the left and all elements > pivot on the right
- By comparing pivot position with k, we can determine which side contains the kth smallest element
- Recursively searching only the relevant side (left OR right, not both) ensures we find the kth smallest element


RUNTIME ANALYSIS
================
Best/Average Case Recurrence: T(n) = T(n/2) + O(n)
Worst Case Recurrence: T(n) = T(n-1) + O(n)

**Average/Best Case: O(n)** ← Key advantage over sorting!
- Occurs when the pivot divides the array into roughly equal halves
- Only ONE subproblem per level (recurse into left OR right, not both)
- O(n) work per level for the PARTITION operation (comparing and swapping elements)
- O(log n) levels in the recursion tree (halving the problem size each time)
- Work done: n + n/2 + n/4 + n/8 + ... = n(1 + 1/2 + 1/4 + ...) = 2n (geometric series)
- Total: **O(n) time**

**Comparison with Quick Sort:**
- Quick Sort: T(n) = 2T(n/2) + O(n) = O(n log n) [searches BOTH sides]
- Quick Select: T(n) = T(n/2) + O(n) = O(n) [searches ONE side only]

**Worst Case: O(n²)**
- Occurs when the pivot is consistently the smallest or largest element
- Happens with already sorted arrays and poor pivot selection (e.g., always choosing first/last element)
- Creates unbalanced partitions: one subarray has n-1 elements, the other has 0
- O(n) levels in the recursion tree (reducing problem size by only 1 each time)
- Total: O(n²) time

Space: O(log n) average case for recursion stack, O(n) worst case; partition itself is O(1) in-place

"""

def partition(arr, left, right):
    """
    Partitions the array segment arr[left:right+1] around a pivot.
    Uses Lomuto partition scheme with the last element as pivot.

    Args:
        arr: Array to partition
        left: Start index (inclusive)
        right: End index (inclusive)

    Returns:
        Final position of the pivot after partitioning
    """
    # Choose the last element as pivot
    pivot = arr[right]

    # i tracks the boundary between elements < pivot and elements >= pivot
    i = left - 1

    # Scan through the array and move elements smaller than pivot to the left
    for j in range(left, right):
        if arr[j] < pivot:
            # Found an element smaller than pivot, move it to the "less than" section
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Place pivot in its final sorted position
    arr[i+1], arr[right] = arr[right], arr[i+1]

    # Return the final position of the pivot
    return i + 1

def quick_select_helper(arr, left, right, k):
    """
    Helper function that finds the kth smallest element in arr[left:right+1].

    Args:
        arr: Array to search
        left: Start index (inclusive)
        right: End index (inclusive)
        k: Find the kth smallest element (1-indexed)

    Returns:
        The kth smallest element value
    """
    # Partition the array and get the pivot's final position
    pivot_index = partition(arr, left, right)

    # Compare pivot position with k to decide what to do
    # Note: k is 1-indexed, pivot_index is 0-indexed
    if k - 1 == pivot_index:
        # Found it! The pivot is the kth smallest element
        return arr[pivot_index]
    elif k - 1 < pivot_index:
        # kth smallest is in the left subarray
        return quick_select_helper(arr, left, pivot_index - 1, k)
    else:
        # kth smallest is in the right subarray
        # Adjust k by the number of elements on the left (including pivot)
        return quick_select_helper(arr, pivot_index + 1, right, k - pivot_index - 1)


def quick_select(arr, k):
    """
    Finds the kth smallest element in an unsorted array.

    Args:
        arr: Array of integers
        k: Find the kth smallest element (1-indexed, k=1 means smallest)

    Returns:
        The kth smallest element, or -1 if k is out of bounds

    Time complexity:
        - Average case: O(n)
        - Worst case: O(n²)
    Space complexity: O(log n) average for recursion stack
    """
    # Validate k is in valid range
    if k < 1 or k > len(arr):  # Fixed: added k < 1 check
        return -1

    # Find the kth smallest element using helper function
    left, right = 0, len(arr) - 1
    return quick_select_helper(arr, left, right, k)


if __name__ == "__main__":
    # Test case 1: Find 3rd smallest in unsorted array
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    k1 = 3
    result1 = quick_select(arr1.copy(), k1)
    print(f"Test 1 - Find {k1}rd smallest:\n"
          f"  Array: [38, 27, 43, 3, 9, 82, 10]\n"
          f"  Result: {result1}\n"
          f"  Expected: 10 (sorted: [3, 9, 10, 27, 38, 43, 82])\n")

    # Test case 2: Find smallest element (k=1)
    arr2 = [5, 2, 8, 1, 9]
    k2 = 1
    result2 = quick_select(arr2.copy(), k2)
    print(f"Test 2 - Find {k2}st smallest (minimum):\n"
          f"  Array: [5, 2, 8, 1, 9]\n"
          f"  Result: {result2}\n"
          f"  Expected: 1\n")

    # Test case 3: Find largest element (k=n)
    arr3 = [5, 2, 8, 1, 9]
    k3 = len(arr3)
    result3 = quick_select(arr3.copy(), k3)
    print(f"Test 3 - Find {k3}th smallest (maximum):\n"
          f"  Array: [5, 2, 8, 1, 9]\n"
          f"  Result: {result3}\n"
          f"  Expected: 9\n")

    # Test case 4: Invalid k (out of bounds)
    arr4 = [5, 2, 8]
    k4 = 10
    result4 = quick_select(arr4.copy(), k4)
    print(f"Test 4 - Invalid k (out of bounds):\n"
          f"  Array: [5, 2, 8]\n"
          f"  k: {k4}\n"
          f"  Result: {result4}\n"
          f"  Expected: -1")
