"""
Longest Increasing Subsequence

Problem:
Given a sequence of numbers a1, a2,..., an, find the maximum length of a subsequence (not necessarily contiguous)
in which the elements are strictly increasing and appear in the same order as in the original sequence.

Subproblem:
Let T(i) be the maximum length of a subsequence in sequence a1, a2,..., ai that ends at ai

Recurrence:
T(1) = 1
T(i) = 1 + max{T(j) | 1 <= j < i, aj < ai}, where 2 <= i <= n

Analysis
Number of subproblems: O(n)
Runtime to fill the table: O(n^2)
Return extracted: max{T(i) | 1 <= i <= n}
Runtime for return extraction: O(n)
"""

def lis(seq: List[int]) -> Tuple[int, List[int]]:
    if len(seq) == 0:
        return 0, []
    dp = [1 for _ in range(len(seq))]
    prev = [-1 for _ in range(len(seq))]
    for i in range(1, len(seq)):
        for j in range(i):
            if seq[i] > seq[j] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    # find best end index
    max_index = max(range(len(seq)), key=lambda i: dp[i])
    maximum = dp[max_index]

    # reconstruct
    res = []
    while max_index != -1:
        res.append(seq[max_index])
        max_index = prev[max_index]
    res.reverse()

    return maximum, res

if __name__ == "__main__":
    seq1 = [1, 3, -2, 6, 2, 5]
    print(lis(seq1))
    seq2 = []
    print(lis(seq2))
    seq3 = [1, 2, 3, 4, 5]
    print(lis(seq3))