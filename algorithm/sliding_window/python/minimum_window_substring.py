"""
Minimum Window Substring
https://leetcode.com/problems/minimum-window-substring/

Given two strings s and t of lengths m and n respectively, return the minimum
window substring of s such that every character in t (including duplicates) is
included in the window. If there is no such substring, return the empty
string "".

Approaches:
    1. minWindow - Sliding window with hash map, tracking matched distinct chars. Time: O(n)
"""

from collections import defaultdict


# Time: O(n)
def minWindow(s: str, t: str) -> str:
    if not s:
        return ""

    m, n = len(s), len(t)
    char_map: dict = defaultdict(int)
    for c in t:
        char_map[c] += 1
    total = len(char_map)
    left, right = 0, 0
    match = 0
    res = ""

    while right < m:
        if s[right] in char_map:
            char_map[s[right]] -= 1
            # We only count a match when num of a specific char
            # equals between s and t.
            if char_map[s[right]] == 0:
                match += 1

        while left < m and match == total:
            if not res or right - left + 1 < len(res):
                res = s[left:right + 1]

            if s[left] in char_map:
                # If already equal, this char is matched before.
                # We need to decrement match since we are getting rid of this char.
                if char_map[s[left]] == 0:
                    match -= 1
                char_map[s[left]] += 1
            left += 1

        right += 1

    return res


if __name__ == "__main__":
    s = "ADOBECODEBANC"
    t = "ABC"
    print(minWindow(s, t))

    s = "a"
    t = "a"
    print(minWindow(s, t))

    s = "a"
    t = "aa"
    print(minWindow(s, t))

    s = "bba"
    t = "ab"
    print(minWindow(s, t))
