"""
LeetCode 50: Pow(x, n) - https://leetcode.com/problems/powx-n/

Implement pow(x, n), which calculates x raised to the power n.

Approaches:
    1. pow / powHelper - Recursive fast exponentiation with memoization.
       Time: O(log n), Space: O(log n)
    2. powIterative   - Iterative binary exponentiation (double-and-halve).
       Time: O(log n), Space: O(1)
"""

# 1010
# 2+8 = x^2 * x^8 = x^2 * x^4 * x^4

# Global memo mirrors the C++ file's unordered_map<int, double> m;
m: dict[int, float] = {}


# Time: O(log n), Space: O(log n)
def powHelper(x: float, n: int) -> float:
    if n == 0:
        return 1.0

    if n in m:
        return m[n]

    half = powHelper(x, n // 2)
    res = half * half if n % 2 == 0 else half * half * x

    m[n] = res
    return res


def pow(x: float, n: int) -> float:
    if x == 1:
        return 1.0
    exp = n
    return 1.0 / powHelper(x, -exp) if n < 0 else powHelper(x, exp)


# We will use a while loop which will continue until n reaches 0.
# If n is odd then we will multiply x once with the result, so that we can reduce n by 1 to make it even.
# Now, n will be even, thus, we now square the x and reduce n by half, i.e. x^n = (x^2)^(n/2)
def powIterative(x: float, n: int) -> float:
    if x == 1:
        return 1.0
    exp = n
    if n < 0:
        x = 1.0 / x
        exp = -exp

    res = 1.0
    while exp > 0:
        # Why we only multiply res when exp is odd?
        if exp % 2 == 1:
            res *= x
        x *= x
        exp //= 2

    return res


if __name__ == "__main__":
    print(pow(2.00000, 10))           # 1024
    print(powIterative(2.00000, 10))  # 1024
    print(pow(2.10000, 3))            # 9.261
    print(powIterative(2.10000, 3))   # 9.261
    print(pow(2.00000, -2))           # 0.25
    print(powIterative(2.00000, -2))  # 0.25

    print(pow(1.00000, -2147483648))
    print(powIterative(1.00000, -2147483648))
