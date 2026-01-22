
#include <iostream>
#include <utility>
#include <vector>

// Quicksort Implementation
// Time: O(n log n) average, O(n²) worst case
// Space: O(log n) for recursion stack

// Lomuto partition: elements ≤ pivot go left, > pivot go right
// Returns pivot's final position
template<typename T>
int partition(std::vector<T>& arr, int left, int right) {
    T pivot = arr[right];
    int i = left - 1;
    
    for (int j = left; j < right; j++)  {
        if (arr[j] <= pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    
    std::swap(arr[i+1], arr[right]);
    return i + 1;
}

// Hoare partition: two pointers move from both ends
// More efficient than Lomuto (fewer swaps)
template<typename T>
int partitionHoare(std::vector<T>& arr, int left, int right) {
    T pivot = arr[left];
    int i = left - 1;
    int j = right + 1;
    
    while (true) {
        do {
            i++;
        } while (arr[i] < pivot);
        
        do {
            j--;
        } while (arr[j] > pivot);
        
        if (i >= j)
            return j;
        
        std::swap(arr[i], arr[j]);
    }
}

// Recursive quicksort helper (Lomuto partition)
template<typename T>
void quicksortHelper(std::vector<T>& arr, int left, int right) {
    if (left >= right)
        return;
    
    int pivotIndex = partition(arr, left, right);
    quicksortHelper(arr, left, pivotIndex - 1);
    quicksortHelper(arr, pivotIndex + 1, right);
}

// Recursive quicksort helper (Hoare partition)
template<typename T>
void quicksortHelperHoare(std::vector<T>& arr, int left, int right) {
    if (left >= right)
        return;
    
    int partitionIndex = partitionHoare(arr, left, right);
    // Hoare partition includes partitionIndex in left subarray
    quicksortHelperHoare(arr, left, partitionIndex);
    quicksortHelperHoare(arr, partitionIndex + 1, right);
}

// Public interface - Lomuto partition
template<typename T>
void quicksort(std::vector<T>& arr) {
    if (!arr.empty()) {
        quicksortHelper(arr, 0, arr.size() - 1);
    }
}

// Public interface - Hoare partition (more efficient)
template<typename T>
void quicksortHoare(std::vector<T>& arr) {
    if (!arr.empty()) {
        quicksortHelperHoare(arr, 0, arr.size() - 1);
    }
}

int main() {
    std::cout << "=== Lomuto Partition ===" << std::endl;
    std::vector<int> vec1 = {3, 1, 5, 2, 9, 7};
    std::vector<double> vec2 = {3.2, 1.0, 5.2, 2.7, 6.4, 3.3};

    quicksort(vec1);
    quicksort(vec2);

    std::cout << "Sorted integers: ";
    for (const auto& num : vec1) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::cout << "Sorted doubles: ";
    for (const auto& num: vec2) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::cout << "\n=== Hoare Partition ===" << std::endl;
    std::vector<int> vec3 = {3, 1, 5, 2, 9, 7};
    std::vector<double> vec4 = {3.2, 1.0, 5.2, 2.7, 6.4, 3.3};

    quicksortHoare(vec3);
    quicksortHoare(vec4);

    std::cout << "Sorted integers: ";
    for (const auto& num : vec3) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::cout << "Sorted doubles: ";
    for (const auto& num: vec4) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}
