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

def merge_sort(arr):
    """
    Sorts an array in-place using merge sort algorithm.

    Args:
        arr: Array of integers to sort

    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    # Base case: empty or single-element arrays are already sorted
    if len(arr) <= 1:
        return

    # Sort the entire array using helper function
    left, right = 0, len(arr)
    merge_sort_helper(arr, left, right)


def merge_sort_helper(arr, left, right):
    """
    Helper function that recursively sorts arr[left:right] in-place.

    Args:
        arr: Array to sort
        left: Start index (inclusive)
        right: End index (exclusive)
    """
    # Base case: array segment has 0 or 1 element
    if right - left <= 1:
        return

    # Divide: find the midpoint
    mid = left + (right - left) // 2

    # Conquer: recursively sort both halves
    merge_sort_helper(arr, left, mid)
    merge_sort_helper(arr, mid, right)

    # Combine: merge the two sorted halves
    merge(arr, left, mid, right)


def merge(arr, left, mid, right):
    """
    Merges two sorted subarrays arr[left:mid] and arr[mid:right] into one sorted array.

    Args:
        arr: Array containing both sorted subarrays
        left: Start index of first subarray (inclusive)
        mid: End index of first subarray (exclusive), start of second subarray
        right: End index of second subarray (exclusive)
    """
    # Initialize pointers for left and right subarrays
    l, r = left, mid
    res = []

    # Merge elements from both subarrays in sorted order
    while l < mid and r < right:
        if arr[l] < arr[r]:
            res.append(arr[l])
            l += 1
        else:
            res.append(arr[r])
            r += 1

    # Append remaining elements from left subarray (if any)
    res.extend(arr[l:mid])

    # Append remaining elements from right subarray (if any)
    res.extend(arr[r:right])

    # Copy merged result back to original array
    arr[left:right] = res




if __name__ == "__main__":
    # Test case 1: Standard unsorted array
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    merge_sort(arr1)
    print(f"Test 1 - Standard unsorted array:\n"
          f"  Result: {arr1}\n"
          f"  Expected: [3, 9, 10, 27, 38, 43, 82]\n")

    # Test case 2: Already sorted array
    arr2 = [1, 2, 3, 4, 5]
    merge_sort(arr2)
    print(f"Test 2 - Already sorted array:\n"
          f"  Result: {arr2}\n"
          f"  Expected: [1, 2, 3, 4, 5]\n")

    # Test case 3: Reverse sorted array with duplicates
    arr3 = [9, 7, 5, 5, 3, 3, 1]
    merge_sort(arr3)
    print(f"Test 3 - Reverse sorted with duplicates:\n"
          f"  Result: {arr3}\n"
          f"  Expected: [1, 3, 3, 5, 5, 7, 9]")