"""
You are given:
A knapsack with maximum capacity W, n items, where each item i has weight w[i] and value v[i].
Your goal is to select items to put into the knapsack so that the total weight of selected items 
is ≤ W and the total value of selected items is maximized.

Problem 1: Each item can be taken at most once.
Problem 2: Each item can be taken any number of times.

Subproblem 1: Let T(i, j) be the maximum total value when having items 1, 2,..., i and the maximum capacity is j.
Subproblem 2: Let T(j) be the maximum total value when the maximum capacity is j.

Recurrence 1:
T(0, j) = 0, 0 <= j <= W
T(i, 0) = 0, 1 <= i <= n
if j - w[i] >= 0: 
    T(i, j) = max{T(i - 1, j), T(i - 1, j - w[i]) + v[i]}, 1 <= i <= n, 1 <= j <= W
else:  
    T(i, j) = T(i - 1, j), 1 <= i <= n, 1 <= j <= W

Recurrence 2:
T(0) = 0
T(j) = max{T(j - w[i]) + v[i] | 1 <= j <= W, 1 <= i <= n, j - w[i] >= 0}

Analaysis 1:
Number of Subproblems: O(nW)
Runtime to fill the table: O(nW)
Return extracted: T(n, W)
Runtime for return extraction: O(1)

Analaysis 2:
Number of Subproblems: O(W)
Runtime to fill the table: O(nW)
Return extracted: T(W)
Runtime for return extraction: O(1)
"""

def knapsack1(w, v, W):
    n = len(w)
    if n == 0 or W == 0:
        return 0
    dp = [[0 for _ in range(W+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, W+1):
            if j - w[i-1] >= 0:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-w[i-1]] + v[i-1])
            else:
                dp[i][j] = dp[i-1][j]
    return dp[n][W]

def knapsack2(w, v, W):
    n = len(w)
    if n == 0 or W == 0:
        return 0
    dp = [0 for _ in range(W+1)]
    for i in range(1, n+1):
        for j in range(w[i-1], W+1):
            dp[j] = max(dp[j], dp[j-w[i-1]] + v[i-1])
    return dp[W]

if __name__ == "__main__":
    # Test case 1: Basic case showing difference
    w1 = [2, 3, 4, 5]
    v1 = [3, 4, 5, 6]
    W1 = 8
    print(f"Test 1 - 0/1 Knapsack: {knapsack1(w1, v1, W1)}")  # Expected: 10
    print(f"Test 1 - Unbounded Knapsack: {knapsack2(w1, v1, W1)}")  # Expected: 12

    # Test case 2: All items too heavy (edge case)
    w2 = [5, 6, 7]
    v2 = [10, 12, 14]
    W2 = 4
    print(f"Test 2 - 0/1 Knapsack: {knapsack1(w2, v2, W2)}")  # Expected: 0
    print(f"Test 2 - Unbounded Knapsack: {knapsack2(w2, v2, W2)}")  # Expected: 0

    # Test case 3: High value density small item
    w3 = [1, 3, 4]
    v3 = [15, 20, 30]
    W3 = 6
    print(f"Test 3 - 0/1 Knapsack: {knapsack1(w3, v3, W3)}")  # Expected: 45
    print(f"Test 3 - Unbounded Knapsack: {knapsack2(w3, v3, W3)}")  # Expected: 90