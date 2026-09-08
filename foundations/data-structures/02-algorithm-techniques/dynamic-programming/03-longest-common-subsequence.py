"""
Problem:
Given two sequences x = x1,x2,...,xn and y = y1,y2,...,ym, find the maximum length of a 
sequence of characters that appears as a subsequence in both x and y

Subproblem:
Let T(i, j) be the length of longest common subsequence of the sequence x1,x2,...,xi and y1,y2,...,yj

Recurrence:
T(0, j) = 0, for 0 <= j <= m
T(i, 0) = 0, for 0 <= i <= n

For 1 <= i <= n, 1 <= j <= m:
    if xi = yj:
        T(i, j) = 1 + T(i-1, j-1)
    else:
        T(i, j) = max(T(i-1, j), T(i, j-1))

Analysis:
Number of subproblems: O(nm)
Runtime to fill the table: O(nm)
Return extracted: T(n, m)
Runtime for return extraction: O(1)
"""

def lcs(x: List[int], y: List[int]):
    n, m = len(x), len(y)
    if n == 0 or m == 0:
        return 0, []
    dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if x[i-1] == y[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    res = []
    i, j = n, m
    while i > 0 and j > 0:
        if x[i-1] == y[j-1]:
            res.append(x[i-1])
            i -= 1
            j -= 1
        else:
            if dp[i][j] == dp[i-1][j]:
                i -= 1
            else:
                j -= 1
    res.reverse()
    return dp[n][m], res

if __name__ == "__main__":
    x1, y1 = [3, 5, 2, 6, 7], [2, 3, 5, 7, 1]
    print(lcs(x1, y1))
    
    x2, y2 = [1, 2, 3, 4, 5], [2, 4, 5, 6, 7]
    print(lcs(x2, y2))
    
    x3, y3 = [10, 20, 30, 40], [50, 60, 70, 80]
    print(lcs(x3, y3))
