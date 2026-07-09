"""
Greatest Common Divisor of Strings
https://leetcode.com/problems/greatest-common-divisor-of-strings

Approaches:
1. gcd_of_strings: Try every candidate prefix of the shorter string from longest
   to shortest and verify it divides both strings.
   Time: O(min(m, n) * (m + n)), Space: O(min(m, n)).
2. gcd_of_strings_with_math: If str1 + str2 == str2 + str1, then the answer is
   the prefix of str1 with length gcd(len(str1), len(str2)); otherwise "".
   Time: O(m + n), Space: O(m + n).
"""

from math import gcd


# Time complexity: O(min(m, n)*(m+n)), Space complexity: O(min(m, n))
def valid_gcd(str1: str, base: str) -> bool:
    m = len(str1)
    d = len(base)

    if m % d != 0:
        return False

    output = base * (m // d)
    return output == str1


def gcd_of_strings(str1: str, str2: str) -> str:
    m = len(str1)
    n = len(str2)

    min_str = str1 if m < n else str2
    for i in range(min(m, n), 0, -1):
        base = min_str[:i]
        if valid_gcd(str2, base) and valid_gcd(str1, base):
            return base

    return ""


# 奇技淫巧
# Intuition: If str1 + str2 != str2 + str1, there is no solution.
# Otherwise, the answer is str1[:gcd(len(str1), len(str2))].
# Time complexity: O(m+n), Space complexity: O(m+n)
def gcd_of_strings_with_math(str1: str, str2: str) -> str:
    if str1 + str2 != str2 + str1:
        return ""

    return str1[: gcd(len(str1), len(str2))]


if __name__ == "__main__":
    str1 = "ABCABC"
    str2 = "ABC"
    assert gcd_of_strings(str1, str2) == "ABC"
    assert gcd_of_strings_with_math(str1, str2) == "ABC"

    str1 = "ABABAB"
    str2 = "ABAB"
    assert gcd_of_strings(str1, str2) == "AB"
    assert gcd_of_strings_with_math(str1, str2) == "AB"

    str1 = "LEET"
    str2 = "CODE"
    assert gcd_of_strings(str1, str2) == ""
    assert gcd_of_strings_with_math(str1, str2) == ""

    str1 = "TAUXXTAUXXTAUXXTAUXXTAUXX"
    str2 = "TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX"
    assert gcd_of_strings(str1, str2) == "TAUXX"
    assert gcd_of_strings_with_math(str1, str2) == "TAUXX"
