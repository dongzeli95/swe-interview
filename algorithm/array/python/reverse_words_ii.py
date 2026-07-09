"""
Reverse Words in a String II
https://leetcode.com/problems/reverse-words-in-a-string-ii/description/

Given a character array s, reverse the order of the words in-place.
A word is a sequence of non-space characters separated by single spaces.

Approaches:
    1. reverse_words: Reverse the entire array, then reverse each word.
       Time: O(n), Space: O(1)
"""

from typing import List


def reverse_words(s: List[str]) -> None:
    """Reverse the order of words in the character list `s` in-place."""

    def reverse(lo: int, hi: int) -> None:
        # Reverses s[lo:hi] in-place (hi is exclusive, matching C++ reverse()).
        hi -= 1
        while lo < hi:
            s[lo], s[hi] = s[hi], s[lo]
            lo += 1
            hi -= 1

    n = len(s)
    reverse(0, n)

    # 'start' points to the beginning of the current word
    # 'end' points to the position just after the current word
    start, end = 0, 0

    while start < n:
        # Move 'end' to the position just after the current word
        while end < n and s[end] != ' ':
            end += 1

        # Reverse the current word: s[start:end] (end exclusive)
        reverse(start, end)

        # Move 'start' and 'end' to the beginning of the next word
        end += 1
        start = end
