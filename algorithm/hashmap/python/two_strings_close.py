"""
Determine if Two Strings Are Close
https://leetcode.com/problems/determine-if-two-strings-are-close

Two strings are considered close if you can attain one from the other using:
  Op 1: Swap any two existing characters.
  Op 2: Transform every occurrence of one existing character into another
        existing character, and do the same with the other character.

Approaches:
  1. closeStrings — count characters in each string, verify the same set of
     characters appears in both, and verify the sorted frequency vectors match.
     Time: O(n), Space: O(1) (fixed 26-length arrays).
"""


def closeStrings(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False

    m1 = [0] * 26
    m2 = [0] * 26

    n = len(word1)
    a = ord('a')
    for i in range(n):
        m1[ord(word1[i]) - a] += 1
        m2[ord(word2[i]) - a] += 1

    for i in range(26):
        if m1[i] != 0 and m2[i] == 0:
            return False
        if m2[i] != 0 and m1[i] == 0:
            return False

    m1.sort()
    m2.sort()

    for i in range(26):
        if m1[i] != m2[i]:
            return False

    return True


if __name__ == "__main__":
    assert closeStrings("abc", "bca") == True
    assert closeStrings("a", "aa") == False
    assert closeStrings("cabbba", "abbccc") == True

    # a: 2, b: 3, c: 1
    # a: 1, b: 2, c: 3
