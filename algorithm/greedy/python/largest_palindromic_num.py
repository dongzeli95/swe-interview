"""
Largest Palindromic Number
https://leetcode.com/problems/largest-palindromic-number/description/

Given a string ``num`` of digits, return the largest palindromic integer (as a
string) that can be built using a subset of those digits, with no leading
zeroes and at least one digit used.

Approaches:
    1. largestPalindromic - Digit frequency counting (greedy).
       Time: O(n), Space: O(1) (fixed size-10 frequency array).
"""

from typing import List


# Time: O(n), Space: O(n) for the output string
def largestPalindromic(num: str) -> str:
    # Frequency array of only size 10 as digit range is 0-9.
    freqArr: List[int] = [0] * 10

    for ch in num:  # storing the frequency
        freqArr[ord(ch) - ord('0')] += 1

    front, back = "", ""  # initialising two empty strings

    # Loop in reverse as we want the largest palindrome number.
    for i in range(9, -1, -1):
        # If front is empty and we try to add zero, it would produce a
        # leading zero, which we explicitly do not want.
        if i == 0 and not front:
            continue

        # We can pair up digits into front/back while at least 2 remain.
        while freqArr[i] > 1:
            front += str(i)
            back += str(i)
            freqArr[i] -= 2

    # At most one digit with odd remaining count can sit in the middle;
    # pick the largest available one to maximize the palindrome.
    for i in range(9, -1, -1):
        if freqArr[i]:
            front += str(i)
            break

    # Reverse the back string and concatenate.
    back = back[::-1]

    return front + back
