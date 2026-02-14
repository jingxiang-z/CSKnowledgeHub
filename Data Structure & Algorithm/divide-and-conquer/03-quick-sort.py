"""
Quick Sort - Divide and Conquer

PROBLEM DESCRIPTION
===================
Given an unsorted array of integers, sort the array in ascending order.

Example: arr = [38, 27, 43, 3, 9, 82, 10]  →  Output: [3, 9, 10, 27, 38, 43, 82]


ALGORITHM DESCRIPTION
=====================
- **Base case**: When the length of the array is smaller than or equal to one, the array is already sorted
- **Divide**: Choose a pivot element and partition the array so that:
  - Elements smaller than or equal to the pivot are moved to the left subarray
  - Elements greater than the pivot are moved to the right subarray
  - The pivot is placed in its final sorted position
- **Conquer**: Recursively sort the left subarray and right subarray
- **Combine**: No combine step needed! After partitioning and recursive sorting, the array is already in sorted order
- **Return value**: The sorted array


CORRECTNESS JUSTIFICATION
==========================
- After partitioning, the pivot is in its final sorted position, with all elements in the left subarray ≤ pivot and all elements in the right subarray > pivot
- The partition operation maintains the invariant that elements are correctly positioned relative to the pivot
- Recursively sorting the left and right subarrays ensures each subarray becomes sorted
- Since the pivot is already in its correct position and separates smaller elements (left) from larger elements (right),
  no merging is needed—the array is sorted once all recursive calls complete


RUNTIME ANALYSIS
================
Best/Average Case Recurrence: T(n) = 2T(n/2) + O(n)
Worst Case Recurrence: T(n) = T(n-1) + O(n)

**Average/Best Case: O(n log n)**
- Occurs when the pivot divides the array into roughly equal halves
- Two balanced subproblems per level
- O(n) work per level for the PARTITION operation (comparing and swapping elements)
- O(log n) levels in the recursion tree (halving the problem size each time)
- Total: O(n log n) time

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

    Note: Always uses arr[right] as pivot, which causes O(n²) worst case
          on already sorted or reverse sorted arrays.
    """
    # Choose the last element as pivot
    pivot = arr[right]

    # i tracks the boundary between elements < pivot and elements >= pivot
    # Elements at [left, i] are < pivot
    # Elements at [i+1, j-1] are >= pivot
    i = left - 1

    # Scan through the array and move elements smaller than pivot to the left
    for j in range(left, right):
        if arr[j] < pivot:
            # Found an element smaller than pivot, move it to the "less than" section
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Place pivot in its final sorted position (between smaller and larger elements)
    arr[i+1], arr[right] = arr[right], arr[i+1]

    # Return the final position of the pivot
    return i + 1

def quick_sort_helper(arr, left, right):
    """
    Helper function that recursively sorts arr[left:right+1] in-place.

    Args:
        arr: Array to sort
        left: Start index (inclusive)
        right: End index (inclusive)
    """
    # Base case: array segment has 0 or 1 element
    if left >= right:
        return

    # Divide: partition the array and get the pivot's final position
    pivot_index = partition(arr, left, right)

    # Conquer: recursively sort the left and right subarrays
    # Note: pivot is already in its correct position, so we exclude it
    quick_sort_helper(arr, left, pivot_index - 1)
    quick_sort_helper(arr, pivot_index + 1, right)


def quick_sort(arr):
    """
    Sorts an array in-place using quick sort algorithm.

    Args:
        arr: Array of integers to sort

    Time complexity:
        - Average case: O(n log n)
        - Worst case: O(n²) when array is already sorted or reverse sorted
    Space complexity: O(log n) average for recursion stack, O(n) worst case
    """
    # Base case: empty or single-element arrays are already sorted
    if len(arr) <= 1:
        return

    # Sort the entire array using helper function
    left, right = 0, len(arr) - 1
    quick_sort_helper(arr, left, right)




if __name__ == "__main__":
    # Test case 1: Standard unsorted array
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    quick_sort(arr1)
    print(f"Test 1 - Standard unsorted array:\n"
          f"  Result: {arr1}\n"
          f"  Expected: [3, 9, 10, 27, 38, 43, 82]\n")

    # Test case 2: Already sorted array (worst case for this implementation)
    arr2 = [1, 2, 3, 4, 5]
    quick_sort(arr2)
    print(f"Test 2 - Already sorted array (worst case):\n"
          f"  Result: {arr2}\n"
          f"  Expected: [1, 2, 3, 4, 5]\n")

    # Test case 3: Array with duplicates
    arr3 = [5, 2, 8, 2, 9, 1, 5, 5]
    quick_sort(arr3)
    print(f"Test 3 - Array with duplicates:\n"
          f"  Result: {arr3}\n"
          f"  Expected: [1, 2, 2, 5, 5, 5, 8, 9]")