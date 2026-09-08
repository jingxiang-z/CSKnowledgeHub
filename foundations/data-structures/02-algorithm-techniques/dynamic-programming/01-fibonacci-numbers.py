"""
Fibonacci Numbers

Problem:
Given a non-negative integer n, compute the n-th Fibonacci number F(n),
where the sequence is defined by:

    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2)   for n >= 2

Subproblem:
Let F(i) be the i-th Fibonacci number, for 0 <= i <= n

Recurrence:
F(0) = 0
F(1) = 1
F(i) = F(i-1) + F(i-2) for i >= 2

Analysis:
Number of subproblems: O(n)
Runtime for table fill: O(n)
Return extracted: F(n)
Runtime for return extraction: O(1)
"""

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    prev, curr = 0, 1
    for i in range(2, n+1):
        prev, curr = curr, prev + curr
    return curr


if __name__ == "__main__":
    print(fib(2))
    print(fib(5))
    print(fib(10))