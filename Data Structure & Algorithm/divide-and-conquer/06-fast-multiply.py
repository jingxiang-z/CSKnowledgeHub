"""
Fast Integer Multiplication (Karatsuba) - Divide and Conquer

PROBLEM DESCRIPTION
===================
Given two large integers, multiply them efficiently. The standard grade-school
multiplication algorithm takes O(n²) time for n-digit numbers. Karatsuba's algorithm
uses divide and conquer to achieve better asymptotic complexity.

Example: 1234 * 5678 = 7006652


ALGORITHM DESCRIPTION
=====================
- **Base case**: If the numbers are small enough (single bit or small threshold), multiply directly
- **Divide**: Split each number at the midpoint into high and low bit halves: x = x_high*2^(n/2) + x_low, y = y_high*2^(n/2) + y_low
- **Conquer**: Recursively compute three products: p1 = x_high * y_high, p2 = x_low * y_low, p3 = (x_high + x_low) * (y_high + y_low)
- **Combine**: Compute result = p1*2^n + (p3 - p1 - p2)*2^(n/2) + p2 (using bit shifts for efficiency)
- **Return value**: The product of x and y


CORRECTNESS JUSTIFICATION
==========================
- Splitting numbers and recursively multiplying works because x*y = (x_high*2^(n/2) + x_low)*(y_high*2^(n/2) + y_low), which expands to the standard multiplication formula
- The Karatsuba trick uses (x_high + x_low)*(y_high + y_low) = x_high*y_high + x_high*y_low + x_low*y_high + x_low*y_low, which contains all four products we need
- We only need 3 multiplications because p3 - p1 - p2 gives us x_high*y_low + x_low*y_high, eliminating the need for two separate multiplications


RUNTIME ANALYSIS
================
Recurrence: T(n) = 3T(n/2) + O(n)

- Three recursive calls on half-sized numbers: 3T(n/2)
- O(n) work for splitting numbers and combining results (addition and shifting)
- Master Theorem: a = 3, b = 2, f(n) = O(n), so log_b(a) = log_2(3) ≈ 1.585
- Since f(n) = O(n^1) and 1 < 1.585, Case 1 applies
- Total: O(n^log_2(3)) ≈ O(n^1.585)

Comparison: Naive multiplication O(n²) requires 4 recursive calls, Karatsuba O(n^1.585) needs only 3

Space: O(log n) for recursion stack depth
"""


def karatsuba(x, y):
    """
    Multiply two integers using Karatsuba's divide-and-conquer algorithm.

    Args:
        x: First integer
        y: Second integer

    Returns:
        Product of x and y

    Time: O(n^1.585) where n is the number of digits
    Space: O(log n) for recursion stack
    """
    # Base case: use direct multiplication for small numbers
    if x < 10 or y < 10:
        return x * y

    # Determine the size (number of digits)
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # Split x and y into high and low parts
    # x = x_high * 10^half + x_low
    # y = y_high * 10^half + y_low
    divisor = 10 ** half
    x_high, x_low = divmod(x, divisor)
    y_high, y_low = divmod(y, divisor)

    # Three recursive multiplications (Karatsuba's key insight)
    p1 = karatsuba(x_high, y_high)  # High parts
    p2 = karatsuba(x_low, y_low)    # Low parts
    p3 = karatsuba(x_high + x_low, y_high + y_low)  # Sum of parts

    # Combine results using the formula:
    # x*y = p1*10^(2*half) + (p3 - p1 - p2)*10^half + p2
    return p1 * (10 ** (2 * half)) + (p3 - p1 - p2) * (10 ** half) + p2


def karatsuba_binary(x, y):
    """
    Multiply two integers using Karatsuba algorithm with binary splitting.
    More efficient for computer representation using bit shifts.

    Args:
        x: First integer
        y: Second integer

    Returns:
        Product of x and y

    Time: O(n^1.585) where n is the number of bits
    Space: O(log n) for recursion stack
    """
    # Base case: use direct multiplication for small numbers
    if x < 10 or y < 10:
        return x * y

    # Determine the size in bits
    n = max(x.bit_length(), y.bit_length())
    half = n // 2

    # Split x and y using bit operations
    # x = x_high * 2^half + x_low
    # y = y_high * 2^half + y_low
    x_high = x >> half
    x_low = x & ((1 << half) - 1)
    y_high = y >> half
    y_low = y & ((1 << half) - 1)

    # Three recursive multiplications
    p1 = karatsuba_binary(x_high, y_high)
    p2 = karatsuba_binary(x_low, y_low)
    p3 = karatsuba_binary(x_high + x_low, y_high + y_low)

    # Combine using bit shifts
    return (p1 << (2 * half)) + ((p3 - p1 - p2) << half) + p2


def naive_multiply(x, y):
    """
    Naive O(n²) multiplication for comparison.

    Args:
        x: First integer
        y: Second integer

    Returns:
        Product of x and y

    Time: O(n²) where n is the number of digits
    """
    return x * y


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_cases = [
        (1234, 5678),
        (12, 34),
        (999, 999),
        (123456789, 987654321),
        (10, 10),
        (7, 8),
    ]

    print("Karatsuba Fast Multiplication Algorithm")
    print("=" * 50)

    for x, y in test_cases:
        result_karatsuba = karatsuba(x, y)
        result_binary = karatsuba_binary(x, y)
        result_naive = naive_multiply(x, y)
        expected = x * y

        print(f"\n{x} × {y}")
        print(f"  Karatsuba (decimal): {result_karatsuba}")
        print(f"  Karatsuba (binary):  {result_binary}")
        print(f"  Expected:            {expected}")

        # Verify correctness
        assert result_karatsuba == expected, f"Decimal version failed for {x} × {y}"
        assert result_binary == expected, f"Binary version failed for {x} × {y}"
        print(f"  ✓ Correct!")

    print("\n" + "=" * 50)
    print("All tests passed!")
