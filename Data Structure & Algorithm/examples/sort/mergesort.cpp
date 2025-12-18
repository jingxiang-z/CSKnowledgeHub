#include <iostream>
#include <vector>

template<typename T>
void merge(std::vector<T>& arr, int left, int mid, int right, std::vector<T>& aux) {
    // Copy data to auxiliary array
    for (int i = left; i <= right; i++) {
        aux[i] = arr[i];
    }
    
    int i = left;      // Pointer for left subarray
    int j = mid + 1;   // Pointer for right subarray
    int k = left;      // Pointer for merged array
    
    // Merge the two subarrays back into arr
    while (i <= mid && j <= right) {
        if (aux[i] <= aux[j]) {
            arr[k++] = aux[i++];
        } else {
            arr[k++] = aux[j++];
        }
    }
    
    // Copy remaining elements from left subarray (if any)
    while (i <= mid) {
        arr[k++] = aux[i++];
    }
    
    // Copy remaining elements from right subarray (if any)
    while (j <= right) {
        arr[k++] = aux[j++];
    }
}

// Internal recursive mergesort function
template<typename T>
void mergeSortHelper(std::vector<T>& arr, int left, int right, std::vector<T>& aux) {
    if (left >= right) {
        return;  // Base case: single element or empty
    }
    
    int mid = left + (right - left) / 2;  // Avoid overflow
    
    // Recursively sort left and right halves
    mergeSortHelper(arr, left, mid, aux);
    mergeSortHelper(arr, mid + 1, right, aux);
    
    // Merge the sorted halves
    merge(arr, left, mid, right, aux);
}

// Main mergesort function - public interface
template<typename T>
void mergesort(std::vector<T>& arr) {
    if (arr.size() <= 1) {
        return;  // Already sorted
    }
    
    // Allocate auxiliary array once - O(n) space
    std::vector<T> aux(arr.size());
    
    // Call helper with indices
    mergeSortHelper(arr, 0, arr.size() - 1, aux);
}

int main() {
    std::vector<int> arr1 = {38, 27, 43, 3, 9, 82, 10};
    std::vector<double> arr2 = {3.2, 1.0, 5.2, 2.7, 6.4, 3.3};
    
    mergesort(arr1);
    mergesort(arr2);
    
    std::cout << "Sorted integers: ";
    for (const auto& num : arr1) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    std::cout << "Sorted doubles:  ";
    for (const auto& num : arr2) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    return 0;
}