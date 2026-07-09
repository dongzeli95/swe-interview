"""
Word Break II
https://leetcode.com/problems/word-break-ii/

Given a string s and a dictionary of strings wordDict, add spaces in s to
construct a sentence where each word is a valid dictionary word. Return all
such possible sentences in any order. Words in the dictionary may be reused.

Approaches:
  1. wordBreak2: DFS with memoization on start index.
     Time:  O(n^3) with memo (n^2 substrings, O(n) copy per result list).
     Space: O(n) stack, O(n^3) heap for cached lists.
  2. wordBreak: Plain DFS/backtracking collecting all splits, then joining.
     Time:  O(2^n) worst case without memoization.
     Space: O(n) stack + output size.
"""

from typing import Dict, List, Set


# Why we need memoization?
# For example: s = "aabb", dict: ["a", "b", "aa", "bb"]
# In this case "bb" substring will be evaluated twice: once after "a a" and
# another one after "aa". Memoization eliminates duplicate calculations.
# Time complexity without memoization: O(2^n)
# Time complexity with memoization: O(n^3), where n is the length of the string
# We have n^2 substrings and for each substring we copy the list of strings, so
# it is O(n^3).
# Space: Stack O(n), Heap O(n^3)
def dfsWithMemo(s: str, idx: int, dict_set: Set[str],
                cache: Dict[int, List[str]]) -> List[str]:
    # Base case
    if idx == len(s):
        return [""]

    if idx in cache:
        return cache[idx]

    n = len(s)
    res: List[str] = []
    for i in range(idx, n):
        word = s[idx:i + 1]
        if word not in dict_set:
            continue
        sub = dfsWithMemo(s, i + 1, dict_set, cache)
        for tail in sub:
            new_str = word if not tail else word + " " + tail
            res.append(new_str)

    cache[idx] = res
    return res


def wordBreak2(s: str, dict_words: List[str]) -> List[str]:
    if not s:
        return []

    d: Set[str] = set(dict_words)
    cache: Dict[int, List[str]] = {}

    return dfsWithMemo(s, 0, d, cache)


def dfs(s: str, idx: int, dict_set: Set[str],
        res: List[List[str]], curr: List[str]) -> None:
    # Base case
    if idx == len(s):
        res.append(list(curr))
        return

    n = len(s)
    for i in range(idx, n):
        word = s[idx:i + 1]
        if word not in dict_set:
            continue
        curr.append(word)
        dfs(s, i + 1, dict_set, res, curr)
        curr.pop()


def wordBreak(s: str, dict_words: List[str]) -> List[str]:
    if not s:
        return []

    d: Set[str] = set(dict_words)
    res: List[List[str]] = []
    curr: List[str] = []

    dfs(s, 0, d, res, curr)

    return [" ".join(v) for v in res]


if __name__ == "__main__":
    dict1 = ["cat", "cats", "and", "sand", "dog"]
    res1 = ["cats and dog", "cat sand dog"]
    output1 = wordBreak2("catsanddog", dict1)
    for i in output1:
        print(i)
    # assert wordBreak("catsanddog", dict1) == res1

    dict2 = ["apple", "pen", "applepen", "pine", "pineapple"]
    res2 = ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]
    output2 = wordBreak2("pineapplepenapple", dict2)
    for i in output2:
        print(i)

    dict3 = ["cats", "dog", "sand", "and", "cat"]
    res3: List[str] = []
    assert wordBreak2("catsandog", dict3) == res3
