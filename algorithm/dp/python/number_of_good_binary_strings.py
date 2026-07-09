"""
Number of Good Binary Strings
https://leetcode.com/problems/number-of-good-binary-strings/description/

Approaches:
1. goodBinaryStrings: 1D DP where dp[i] = number of good binary strings of length i.
   Transition: dp[i] += dp[i - oneGroup] + dp[i - zeroGroup]. Sum dp[minLength..maxLength].
   Time: O(maxLength), Space: O(maxLength).
"""


# dp[i] means with length i, how many good binary strings we have.
# Time: O(max), Space: O(max)
def goodBinaryStrings(minLength: int, maxLength: int, oneGroup: int, zeroGroup: int) -> int:
    dp = [0] * (maxLength + 1)
    dp[0] = 1
    mod = 10**9 + 7

    for i in range(1, maxLength + 1):
        if i - oneGroup >= 0:
            dp[i] = (dp[i] + dp[i - oneGroup]) % mod
        if i - zeroGroup >= 0:
            dp[i] = (dp[i] + dp[i - zeroGroup]) % mod

    res = 0
    for i in range(minLength, maxLength + 1):
        res = (res + dp[i]) % mod

    return res


if __name__ == "__main__":
    assert goodBinaryStrings(2, 3, 1, 2) == 5
    assert goodBinaryStrings(4, 4, 4, 3) == 1
