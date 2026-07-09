"""
Maximum Number of Vowels in a Substring of Given Length
https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length

Given a string s and an integer k, return the maximum number of vowel letters
in any substring of s with length k. Vowel letters are 'a', 'e', 'i', 'o', 'u'.

Approaches:
    1. maxVowels - Sliding window of size k, tracking vowel count.
       Time: O(n), Space: O(1)
"""


def isVowel(c: str) -> bool:
    return c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u'


# Time complexity: O(n), Space complexity: O(1)
def maxVowels(s: str, k: int) -> int:
    if not s:
        return 0

    n = len(s)
    l, r = 0, 0
    res = 0
    cnt = 0

    while r < n:
        if isVowel(s[r]):
            cnt += 1
            res = max(res, cnt)

        if r - l + 1 == k:
            if isVowel(s[l]):
                cnt -= 1
            l += 1

        r += 1

    return res


if __name__ == "__main__":
    assert maxVowels("abciiidef", 3) == 3
    assert maxVowels("aeiou", 2) == 2
    assert maxVowels("leetcode", 3) == 2
