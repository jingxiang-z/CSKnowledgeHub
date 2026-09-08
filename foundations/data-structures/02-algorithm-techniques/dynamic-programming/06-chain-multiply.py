"""
Problem:
Given a sequence of matrices A1, A2,..., An, where matrix Ai has dimensions pi-1 * pi,
determine the minimum number of scalar multiplications needed to compute the product
A1A2...An by choosing the optimal order of parenthesization.

Subproblem:
Let T(i, j) be the minimum number of scalar multiplications needed to compute the product Ai...Aj

Recurrence:
T(i, i) = 0, 1 <= i <= n
T(i, j) = min{T(i, k) + T(k + 1, j) + pi-1pkpj | i <= k < j}

Analysis:
Number of subproblems: O(n^2)
Runtime to fill the table: O(n^3)
Return extracted: T(1, n)
Runtime for return extraction: O(1)
"""

def multiply(p: List[int]) -> int:
    # Let n be the DP table dimension
    # Matrices are A1..A(n-1), where Ai is p[i-1] x p[i].
    n = len(p)
    if n <= 2:
        return 0

    dp = [[0] * n for _ in range(n)]

    # DP Table Iteration Strategy:
    # We iterate by CHAIN LENGTH (L) from small to large, ensuring that when we
    # compute dp[i][j], all smaller subproblems dp[i][k] and dp[k+1][j] are already solved.
    #
    # Example for n=4 (3 matrices):
    # L=2: compute dp[1][2], dp[2][3]           (chains of length 2)
    # L=3: compute dp[1][3]                     (chains of length 3)
    #
    # Visual representation of computation order:
    #     1   2   3
    # 1 [ 0 | 1 | 3 ]
    # 2 [   | 0 | 2 ]
    # 3 [   |   | 0 ]
    # Numbers show the order cells are computed (diagonal is base case)
    
    for L in range(2, n):  # L is the chain length (number of matrices)
        # For each starting position i, compute dp[i][j] where j = i + L - 1
        for i in range(1, n - L + 1):  # i ranges from 1 to ensure valid matrix indices
            j = i + L - 1  # Ending position: i and j are L-1 positions apart
            
            best = float("inf")
            # Try all possible split points k between i and j
            # Split the chain into [i..k] and [k+1..j]
            for k in range(i, j):  # k goes from i to j-1
                # Cost = (cost of left chain) + (cost of right chain) + (cost to multiply results)
                # The final multiplication multiplies a (p[i-1] x p[k]) matrix with a (p[k] x p[j]) matrix
                cost = dp[i][k] + dp[k+1][j] + p[i-1] * p[k] * p[j]
                best = min(best, cost)
            
            dp[i][j] = best

    # Return dp[1][n-1]: minimum cost to multiply all matrices A1 through A(n-1)
    return dp[1][n - 1]


if __name__ == "__main__":
    # Test Case 1: Classic example with 4 matrices
    # Matrices: A1(10x30), A2(30x5), A3(5x60)
    # Possible parenthesizations:
    # - ((A1A2)A3): (10*30*5) + (10*5*60) = 1500 + 3000 = 4500 ✓ optimal
    # - (A1(A2A3)): (30*5*60) + (10*30*60) = 9000 + 18000 = 27000
    p1 = [10, 30, 5, 60]
    print(multiply(p1))    
    # Test Case 2: 4 matrices with varying dimensions
    # Matrices: A1(30x35), A2(35x15), A3(15x5), A4(5x10)
    # Optimal: ((A1(A2A3))A4)
    # - A2A3: 35*15*5 = 2625
    # - A1(A2A3): 30*35*5 = 5250
    # - ((A1(A2A3))A4): 30*5*10 = 1500
    # Total: 2625 + 5250 + 1500 = 9375
    p2 = [30, 35, 15, 5, 10]
    print(multiply(p2))    
    # Test Case 3: 6 matrices - larger chain
    # Matrices: A1(5x10), A2(10x3), A3(3x12), A4(12x5), A5(5x50), A6(50x6)
    # This tests the algorithm with a longer chain
    p3 = [5, 10, 3, 12, 5, 50, 6]
    print(multiply(p3))
