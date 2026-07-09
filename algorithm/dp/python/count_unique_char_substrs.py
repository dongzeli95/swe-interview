"""
Count Unique Characters of All Substrings of a Given String
https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/

Approaches:
1. uniqueLetterString: For each character occurrence, count how many substrings
   it contributes to as a unique character by tracking the last two occurrence
   indices per character. Time: O(n), Space: O(1) (fixed 26-letter alphabet).
"""


def uniqueLetterString(S: str) -> int:
    res = 0
    n = len(S)
    M = 10**9 + 7
    idx = [[-1, -1] for _ in range(26)]
    for i in range(n):
        c = ord(S[i]) - ord('A')
        res = (res + (i - idx[c][1]) * (idx[c][1] - idx[c][0]) % M) % M
        idx[c][0] = idx[c][1]
        idx[c][1] = i
    for c in range(26):
        res = (res + (n - idx[c][1]) * (idx[c][1] - idx[c][0]) % M) % M
    return res
