"""
Binary Search

PROBLEM DESCRIPTION
===================
Given a sorted array of integers and a target value, find the index of the target
in the array. Return -1 if the target is not found.

Example: arr = [1, 3, 5, 7, 9, 11, 13, 15], target = 7  →  Output: 3


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

def binary_search(arr, target):
    """
    Standard binary search that returns the index of target, or -1 if not found.

    Args:
        arr: Sorted array of integers
        target: Value to search for

    Returns:
        Index of target in arr, or -1 if not found
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1

    return -1


def lower_bound(arr, target):
    """
    Find the first position where an element >= target exists (or could be inserted).

    Args:
        arr: Sorted array of integers
        target: Value to search for

    Returns:
        Index of first element >= target, or len(arr) if all elements < target
    """
    # Initialize search boundaries (note: right = len(arr), not len(arr) - 1)
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        # Keep mid in search space by setting right = mid (not mid - 1)
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1

    # left now points to the first element >= target
    return left

def upper_bound(arr, target):
    """
    Find the first position where an element > target exists (or could be inserted).

    Args:
        arr: Sorted array of integers
        target: Value to search for

    Returns:
        Index of first element > target, or len(arr) if all elements <= target
    """
    # Initialize search boundaries (note: right = len(arr), not len(arr) - 1)
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        # Keep mid in search space by setting right = mid (not mid - 1)
        if arr[mid] > target:
            right = mid
        else:
            left = mid + 1

    # left now points to the first element > target
    return left


if __name__ == "__main__":
    # Test case 1: Standard binary search - element exists
    arr1 = [1, 3, 5, 7, 9, 11, 13, 15]
    target1 = 7
    result1 = binary_search(arr1, target1)
    print(f"Test 1 - Binary Search (element exists):\n"
          f"  Array: {arr1}\n"
          f"  Target: {target1}\n"
          f"  Result: {result1} (expected: 3)\n")

    # Test case 2: Binary search - element does not exist
    arr2 = [2, 4, 6, 8, 10, 12]
    target2 = 7
    result2 = binary_search(arr2, target2)
    print(f"Test 2 - Binary Search (element not found):\n"
          f"  Array: {arr2}\n"
          f"  Target: {target2}\n"
          f"  Result: {result2} (expected: -1)\n")

    # Test case 3: Lower bound and upper bound with duplicates
    arr3 = [1, 3, 3, 3, 7, 8, 9]
    target3 = 3
    lower = lower_bound(arr3, target3)
    upper = upper_bound(arr3, target3)
    print(f"Test 3 - Lower/Upper Bound (duplicates):\n"
          f"  Array: {arr3}\n"
          f"  Target: {target3}\n"
          f"  Lower bound: {lower} (expected: 1, first occurrence of 3)\n"
          f"  Upper bound: {upper} (expected: 4, first element > 3)\n"
          f"  All occurrences of {target3} are in range [{lower}, {upper})")
