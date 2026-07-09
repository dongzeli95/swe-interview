"""
Domino and Tromino Tiling
https://leetcode.com/problems/domino-and-tromino-tiling

Approaches:
1. Bottom-up DP tracking fully-covered f(k) and partially-covered p(k) states.
   Recurrences:
       f(k) = f(k-1) + f(k-2) + 2 * p(k-1)
       p(k) = p(k-1) + f(k-2)
   Time complexity: O(n), Space complexity: O(n).
"""


# Time complexity: O(n), Space complexity: O(n)
def numTilings(n: int) -> int:
    if n <= 2:
        return n

    MOD = 10**9 + 7
    f = [0] * (n + 1)
    p = [0] * (n + 1)

    f[0] = 1
    f[1] = 1
    f[2] = 2
    p[0] = 0
    p[1] = 0
    p[2] = 1

    for i in range(3, n + 1):
        f[i] = (f[i - 1] + f[i - 2] + 2 * p[i - 1]) % MOD
        p[i] = (p[i - 1] + f[i - 2]) % MOD

    return f[n]


if __name__ == "__main__":
    assert numTilings(3) == 5
    assert numTilings(4) == 11
    assert numTilings(5) == 24
    assert numTilings(30) == 312342182
