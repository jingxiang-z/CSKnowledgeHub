#include <iostream>
#include <vector>

// Binary Search - Single-Comparison Variants
// Time: O(log n), Space: O(1)

// Returns first element >= target (or arr.size() if none)
template<typename T>
int lower_bound(const std::vector<T>& arr, T target) {
    int left = 0;
    int right = arr.size();

    while (left < right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] >= target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    return left;
}

// Returns first element > target (or arr.size() if none)
template<typename T>
int upper_bound(const std::vector<T>& arr, T target) {
    int left = 0;
    int right = arr.size();

    while (left < right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] > target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    return left;
}

// Returns index if exact match found, -1 otherwise
template<typename T>
int binary_search(const std::vector<T>& arr, T target) {
    int left = 0;
    int right = arr.size();

    while (left < right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] >= target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    if (left < arr.size() && arr[left] == target) {
        return left;
    }
    return -1;
}

int main() {
    std::vector<int> arr = {1, 3, 3, 3, 5, 7, 9};
    
    std::cout << "Array: [";
    for (size_t i = 0; i < arr.size(); i++) {
        std::cout << arr[i];
        if (i < arr.size() - 1) std::cout << ", ";
    }
    std::cout << "]\n\n";
    
    int target = 3;
    std::cout << "Target = " << target << ":\n";
    std::cout << "  lower_bound (first >= 3): " << lower_bound(arr, target) 
              << " (value: " << arr[lower_bound(arr, target)] << ")\n";
    std::cout << "  upper_bound (first > 3):  " << upper_bound(arr, target)
              << " (value: " << arr[upper_bound(arr, target)] << ")\n";
    std::cout << "  binary_search (exact):    " << binary_search(arr, target) << "\n\n";
    
    target = 4;
    std::cout << "Target = " << target << " (not in array):\n";
    std::cout << "  lower_bound (first >= 4): " << lower_bound(arr, target)
              << " (value: " << arr[lower_bound(arr, target)] << ")\n";
    std::cout << "  upper_bound (first > 4):  " << upper_bound(arr, target)
              << " (value: " << arr[upper_bound(arr, target)] << ")\n";
    std::cout << "  binary_search (exact):    " << binary_search(arr, target) << "\n\n";
    
    target = 10;
    int lb = lower_bound(arr, target);
    int ub = upper_bound(arr, target);
    std::cout << "Target = " << target << " (larger than all):\n";
    std::cout << "  lower_bound (first >= 10): " << lb 
              << (lb == arr.size() ? " (past end)" : "") << "\n";
    std::cout << "  upper_bound (first > 10):  " << ub
              << (ub == arr.size() ? " (past end)" : "") << "\n";
    std::cout << "  binary_search (exact):     " << binary_search(arr, target) << "\n";
    
    return 0;
}
