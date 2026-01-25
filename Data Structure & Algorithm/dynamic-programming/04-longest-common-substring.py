"""
Problem:
Given two strings x = x1x2...xn and y = y1y2...ym, we wish to find the length of their longest
common substring, that is, the largest k for which there are indices i and j with xixi+1...xi+k-1 =
yjyj+1...yj+k-1.

Subproblem:
Let T(i, j) be the length of longest common substring length of the longest common substring that ends 
exactly at positions i in string x and j in string y

Recurrence:
T(0, j) = 0, 0 <= j <= m
T(i, 0) = 0, 0 <= i <= n
For 1 <= i <= n, 1 <= j <= m:
    if xi = yj:
        T(i, j) = 1 + T(i-1, j-1)
    else:
        T(i, j) = 0

Analysis:
Number of subproblems: O(nm)
Runtime to fill the table: O(nm)
Return extracted: max{T(i, j) | 1 <= i <= n, 1 <= j <= m}
Runtime for return extraction: O(1) if tracked during table fill, otherwise O(nm)
"""

def lcs(x, y):
    n, m = len(x), len(y)
    if n == 0 or m == 0:
        return 0, ""
    maximum = 0
    maximum_index = (-1, -1)
    dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if x[i-1] == y[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
                if dp[i][j] > maximum:
                    maximum = dp[i][j]
                    maximum_index = (i-1, j-1)
            else:
                dp[i][j] = 0
    i, j = maximum_index
    substring = x[i-maximum+1:i+1]
    
    return maximum, substring

if __name__ == "__main__":
    print(lcs("acdfe", "adfiq"))
    
    print(lcs("abcdefgh", "cdefxyz"))
    
    print(lcs("programming", "gaming"))