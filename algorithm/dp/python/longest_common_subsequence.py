"""
Longest Common Subsequence
https://leetcode.com/problems/longest-common-subsequence

Given two strings text1 and text2, return the length of their longest common
subsequence. If there is no common subsequence, return 0.

Approaches:
  1. Bottom-up 2D DP where dp[i][j] = LCS of s[:i] and t[:j].
     Time: O(m * n), Space: O(m * n).
"""


def longestCommonSubsequence(s: str, t: str) -> int:
    if not s or not t:
        return 0

    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

            if s[i - 1] == t[j - 1]:
                dp[i][j] = max(dp[i][j], 1 + dp[i - 1][j - 1])

    return dp[m][n]


if __name__ == "__main__":
    # print(longestCommonSubsequence("abcde", "ace"))
    assert longestCommonSubsequence("abcde", "ace") == 3
    assert longestCommonSubsequence("abc", "abc") == 3
    assert longestCommonSubsequence("abc", "def") == 0
