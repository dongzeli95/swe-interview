"""
Similar String Groups (LeetCode 839)
https://leetcode.com/problems/similar-string-groups/description/

Two strings X and Y are similar if they are identical, or can be made equal by
swapping two letters (at distinct positions) in X. Given a list of anagrams,
count the number of connected groups formed by the similarity relation.

Approaches:
  1. DFS over strings, visited set tracks seen strings.
     Time:  O(n^2 * m) — n^2 pairs, m string length for similarity check.
     Space: O(n) for recursion depth and visited set.
"""

from typing import List


def are_almost_equal(a: str, b: str) -> bool:
    """Helper mirroring the C++ `areAlmostEqual`: checks anagram + diff in {0, 2}."""
    if len(a) != len(b):
        return False

    freq = [0] * 26
    for ch in a:
        freq[ord(ch) - ord('a')] += 1
    for ch in b:
        freq[ord(ch) - ord('a')] -= 1

    for c in freq:
        if c != 0:
            return False

    diff = 0
    for x, y in zip(a, b):
        if x != y:
            diff += 1
    return diff == 0 or diff == 2


def is_similar(str1: str, str2: str) -> bool:
    """Assumes anagrams — returns True if they differ in at most 2 positions."""
    cnt = 0
    for c1, c2 in zip(str1, str2):
        if c1 == c2:
            continue
        cnt += 1
        if cnt > 2:
            return False
    return True


def helper(A: List[str], s: str, visited: set) -> None:
    if s in visited:
        return
    visited.add(s)
    for word in A:
        if is_similar(word, s):
            helper(A, word, visited)


# Time:  O(n^2 * m), n^2 edges and m string length for the similarity check.
# Space: O(n) for depth and visited set.
def numSimilarGroups(A: List[str]) -> int:
    res = 0
    visited: set = set()
    for s in A:
        if s in visited:
            continue
        res += 1
        helper(A, s, visited)
    return res
