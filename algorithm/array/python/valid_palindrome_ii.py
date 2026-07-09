"""
Valid Palindrome II
https://leetcode.com/problems/valid-palindrome-ii/

Given a string s, return True if s can be a palindrome after deleting at most
one character from it.

Approaches:
    1. validPalindrome (two-pointer + isValid helper) - Time: O(n), Space: O(1)
    2. helper (recursive with modified flag, uses substring splicing) -
       Time: O(n^2) worst case, Space: O(n) due to substring allocation
"""


# Approach 1: Two-pointer with isValid helper
# Time: O(n), Space: O(1)
def isValid(s: str, left: int, right: int) -> bool:
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def validPalindrome(s: str) -> bool:
    if not s:
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return isValid(s, l + 1, r) or isValid(s, l, r - 1)
        l += 1
        r -= 1

    return True


# Approach 2: Recursive with modified flag (substring splicing)
# Time: O(n^2), Space: O(n)
def helper(s: str, modified: bool) -> bool:
    if not s:
        return True
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            s1 = s[:l] + s[l + 1:]
            s2 = s[:r] + s[r + 1:]
            return (not modified) and (helper(s1, True) or helper(s2, True))
        l += 1
        r -= 1

    return True


# cbbcc
# def validPalindrome(s: str) -> bool:
#     return helper(s, False)


if __name__ == "__main__":
    assert validPalindrome("aba")
    assert validPalindrome("abca")
    assert not validPalindrome("abc")
    assert validPalindrome("cbbcc")
