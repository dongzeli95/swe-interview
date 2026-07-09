"""Merge Strings Alternately.

https://leetcode.com/problems/merge-strings-alternately

You are given two strings word1 and word2. Merge the strings by adding letters
in alternating order, starting with word1. If a string is longer than the
other, append the additional letters onto the end of the merged string.

Approaches:
    1. Two-pointer alternating merge: Time O(m+n), Space O(1) auxiliary
       (O(m+n) for the output string).
"""


def mergeAlternately(word1: str, word2: str) -> str:
    # Time complexity: O(m+n)
    # Space complexity: O(1) auxiliary (output is O(m+n))
    if not word1 or not word2:
        return word1 + word2

    i, j = 0, 0
    m, n = len(word1), len(word2)

    res = []
    while i < m and j < n:
        res.append(word1[i])
        i += 1
        res.append(word2[j])
        j += 1

    while i < m:
        res.append(word1[i])
        i += 1

    while j < n:
        res.append(word2[j])
        j += 1

    return "".join(res)


if __name__ == "__main__":
    assert mergeAlternately("abc", "pqr") == "apbqcr"
    assert mergeAlternately("ab", "pqrs") == "apbqrs"
    assert mergeAlternately("abcd", "pq") == "apbqcd"
