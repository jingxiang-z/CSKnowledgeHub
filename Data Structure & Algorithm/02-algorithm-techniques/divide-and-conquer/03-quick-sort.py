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
    Sorts an array in-place using quick sort algorithm with Lomuto partition.

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


def partition_hoare(arr, left, right):
    """
    Partitions the array segment arr[left:right+1] using Hoare's partition scheme.
    More efficient than Lomuto - does about 3x fewer swaps on average.

    Args:
        arr: Array to partition
        left: Start index (inclusive)
        right: End index (inclusive)

    Returns:
        Index that splits the array such that elements to the left are <= pivot
        and elements to the right are >= pivot. Note: pivot may not be at this index.

    Key differences from Lomuto:
        - Uses two pointers moving from both ends toward center
        - Fewer swaps (more efficient)
        - Pivot ends up somewhere in the middle, not necessarily at the partition index
        - Returns partition index, not final pivot position
    """
    # Choose the middle element as pivot (better for sorted/reverse sorted arrays)
    pivot = arr[(left + right) // 2]

    # Two pointers: i moves right, j moves left
    i = left - 1
    j = right + 1

    while True:
        # Move i right until we find an element >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1

        # Move j left until we find an element <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1

        # If pointers crossed, we're done partitioning
        if i >= j:
            return j

        # Swap elements that are on the wrong side
        arr[i], arr[j] = arr[j], arr[i]


def quick_sort_hoare_helper(arr, left, right):
    """
    Helper function that recursively sorts arr[left:right+1] using Hoare partition.

    Args:
        arr: Array to sort
        left: Start index (inclusive)
        right: End index (inclusive)
    """
    # Base case: array segment has 0 or 1 element
    if left >= right:
        return

    # Divide: partition the array using Hoare's scheme
    partition_index = partition_hoare(arr, left, right)

    # Conquer: recursively sort both halves
    # Note: In Hoare's scheme, the partition index is included in the left subarray
    quick_sort_hoare_helper(arr, left, partition_index)
    quick_sort_hoare_helper(arr, partition_index + 1, right)


def quick_sort_hoare(arr):
    """
    Sorts an array in-place using quick sort with Hoare partition scheme.
    Generally more efficient than Lomuto partition (fewer swaps).

    Args:
        arr: Array of integers to sort

    Time complexity:
        - Average case: O(n log n)
        - Worst case: O(n²) (less likely with middle element as pivot)
    Space complexity: O(log n) average for recursion stack, O(n) worst case
    """
    # Base case: empty or single-element arrays are already sorted
    if len(arr) <= 1:
        return

    # Sort the entire array using Hoare partition
    left, right = 0, len(arr) - 1
    quick_sort_hoare_helper(arr, left, right)




if __name__ == "__main__":
    print("=" * 60)
    print("LOMUTO PARTITION SCHEME")
    print("=" * 60)

    # Test case 1: Standard unsorted array
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    quick_sort(arr1)
    print(f"Test 1 - Standard unsorted array:\n"
          f"  Result: {arr1}\n"
          f"  Expected: [3, 9, 10, 27, 38, 43, 82]\n")

    # Test case 2: Already sorted array (worst case for Lomuto with last element pivot)
    arr2 = [1, 2, 3, 4, 5]
    quick_sort(arr2)
    print(f"Test 2 - Already sorted array (worst case for Lomuto):\n"
          f"  Result: {arr2}\n"
          f"  Expected: [1, 2, 3, 4, 5]\n")

    # Test case 3: Array with duplicates
    arr3 = [5, 2, 8, 2, 9, 1, 5, 5]
    quick_sort(arr3)
    print(f"Test 3 - Array with duplicates:\n"
          f"  Result: {arr3}\n"
          f"  Expected: [1, 2, 2, 5, 5, 5, 8, 9]\n")

    print("=" * 60)
    print("HOARE PARTITION SCHEME")
    print("=" * 60)

    # Test case 1: Standard unsorted array
    arr1_hoare = [38, 27, 43, 3, 9, 82, 10]
    quick_sort_hoare(arr1_hoare)
    print(f"Test 1 - Standard unsorted array:\n"
          f"  Result: {arr1_hoare}\n"
          f"  Expected: [3, 9, 10, 27, 38, 43, 82]\n")

    # Test case 2: Already sorted array (better performance with middle pivot)
    arr2_hoare = [1, 2, 3, 4, 5]
    quick_sort_hoare(arr2_hoare)
    print(f"Test 2 - Already sorted array (better with Hoare):\n"
          f"  Result: {arr2_hoare}\n"
          f"  Expected: [1, 2, 3, 4, 5]\n")

    # Test case 3: Array with duplicates
    arr3_hoare = [5, 2, 8, 2, 9, 1, 5, 5]
    quick_sort_hoare(arr3_hoare)
    print(f"Test 3 - Array with duplicates:\n"
          f"  Result: {arr3_hoare}\n"
          f"  Expected: [1, 2, 2, 5, 5, 5, 8, 9]\n")

    # Test case 4: Reverse sorted (challenging for both)
    arr4_lomuto = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    arr4_hoare = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    quick_sort(arr4_lomuto)
    quick_sort_hoare(arr4_hoare)
    print(f"Test 4 - Reverse sorted array:\n"
          f"  Lomuto result: {arr4_lomuto}\n"
          f"  Hoare result:  {arr4_hoare}\n"
          f"  Expected:      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n")
