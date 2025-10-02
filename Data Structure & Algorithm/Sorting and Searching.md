# Sorting and Searching

## Sorting

### Bubble Sort

- **How it works:** Bubble Sort repeatedly compares adjacent elements and swaps them if they are in the wrong order. It continues this process until no more swaps are needed.
- **Time Complexity:** O(n^2) in the worst and average cases, where 'n' is the number of elements.
- **Space Complexity:** O(1) - Bubble Sort is an in-place sorting algorithm, which means it doesn't require additional memory for sorting.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
```

### Insertion Sort

- **How it works:** Insertion Sort builds the final sorted array one item at a time by taking an element from the unsorted part and inserting it into its correct position within the sorted part.
- **Time Complexity:** O(n^2) in the worst and average cases.
- **Space Complexity:** O(1) - Like the previous two, Insertion Sort is an in-place sorting 

```python
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        j = i-1
        item = arr[i]
        while j >= 0 and arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]
            j -= 1
        arr[j+1] = item
```

### Selection Sort

- **How it works:** Selection Sort divides the input into two parts: a sorted part and an unsorted part. It repeatedly selects the minimum element from the unsorted part and appends it to the sorted part.
- **Time Complexity:** O(n^2) in the worst and average cases.
- **Space Complexity:** O(1) - Selection Sort is also an in-place sorting algorithm.

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
```

### Quick Sort

- **How it works:** Quick Sort also uses a divide-and-conquer approach. It selects a pivot element and partitions the array into two subarrays: one with elements less than the pivot and one with elements greater than the pivot. It then recursively sorts the subarrays.
- **Time Complexity:** O(n^2) in the worst case (rare), but O(n log n) on average and in the best case.
- **Space Complexity:** O(log n) - Quick Sort is often in-place, and the space complexity is determined by the recursion stack.

```python
def quick_sort(arr, low, high):
    if low >= high:
        return
    mid = partition(arr, low, high)
    quick_sort(arr, low, mid-1)
    quick_sort(arr, mid+1, high)

def partition(arr, low, high):
    key = arr[high]
    j = low
    for i in range(low, high):
        if arr[i] <= key:
            arr[j], arr[i] = arr[i], arr[j]
            j += 1
    arr[j], arr[high] = arr[high], arr[j]
    return j
```

### Merge Sort

- **How it works:** Merge Sort is a divide-and-conquer algorithm. It divides the unsorted list into smaller sublists, sorts them, and then merges the sorted sublists until the entire list is sorted.
- **Time Complexity:** O(n log n) in the worst, average, and best cases.
- **Space Complexity:** O(n) - Merge Sort typically requires additional space for the merging step, making it not entirely in-place.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    sort_arr = merge(left, right)
    return sort_arr

def merge(left, right):
    sort_arr = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sort_arr.append(left[i])
            i += 1
        else:
            sort_arr.append(right[j])
            j += 1
    while i < len(left):
        sort_arr.append(left[i])
        i += 1
    while j < len(right):
        sort_arr.append(right[j])
        j += 1
    return sort_arr
```

### Heap Sort

- **How it works:** Heap Sort uses a binary heap data structure to repeatedly extract the maximum element (for ascending order) and place it at the end of the sorted portion of the array.

- **Time Complexity:** O(n log n) in all cases.

- **Space Complexity:** O(1) - Heap Sort is an in-place sorting algorithm.

```python
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    # Build a max heap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one.
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap the root (maximum element) with the last element.
        heapify(arr, i, 0)
```

## Searching

### Linear Search

```python
def linear_serach(arr, target):
    n = len(arr)
    for i in range(n):
        if arr[i] == target:
            return i
    return -1
```

### Binary Search

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left
```
