"""
Longest Palindrome by Concatenating Two Letter Words
https://leetcode.com/problems/longest-palindrome-by-concatenating-two-letter-words/

Approaches:
    1. Hash map pairing (reversed + identical counts) - Time: O(n), Space: O(n)
       Intuition: We need to find pairs of words to put on either side of the
       string. We can also put a single pair of identical words (e.g. "gg") in
       the middle of the palindrome string.
"""

from collections import defaultdict
from typing import List


def is_identical(word: str) -> bool:
    return word[0] == word[1]


def reverse_word(word: str) -> str:
    return word[1] + word[0]


# Time: O(n), Space: O(n)
# Intuition: We need to find pairs of words to put on either side of the string.
# We can also put odd numbers of identical words in the middle of the palindrome string.
def longestPalindrome(words: List[str]) -> int:
    reversed_counts = defaultdict(int)
    identical_counts = defaultdict(int)

    res = 0
    for word in words:
        rev = reverse_word(word)
        if reversed_counts[rev] > 0:
            res += 4
            reversed_counts[rev] -= 1
            if is_identical(word):
                identical_counts[word] -= 1
        else:
            reversed_counts[word] += 1
            if is_identical(word):
                identical_counts[word] += 1

    mx = 0
    for count in identical_counts.values():
        mx = max(mx, count)

    res += mx * 2
    return res
