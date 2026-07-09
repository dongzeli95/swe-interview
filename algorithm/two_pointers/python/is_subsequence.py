"""
Is Subsequence
https://leetcode.com/problems/is-subsequence

Given two strings s and t, return True if s is a subsequence of t, or False otherwise.

Approaches:
1. Two pointers - Time: O(n), Space: O(1) where n = min(len(s), len(t))
"""


# Time complexity: O(n), Space complexity: O(1)
# n is minimum of len(s) and len(t)
def isSubsequence(s: str, t: str) -> bool:
    if not s:
        return True

    m, n = len(s), len(t)
    i, j = 0, 0

    while i < m and j < n:
        if s[i] == t[j]:
            i += 1

        j += 1

    return i == m


if __name__ == "__main__":
    assert isSubsequence("abc", "ahbgdc") is True
    assert isSubsequence("axc", "ahbgdc") is False
