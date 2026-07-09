"""Min flips to make the string 'a's followed by 'b's.

The input string only contains 'a' and 'b'. Find the minimum number of
flips required so that all 'a's come before all 'b's (i.e., the string
matches a pattern like a*b*).

Approaches:
    1. minFlip: bitmask enumeration of every valid a*b* target and XOR/popcount
       to count differences. Time: O(n^2) in the worst case due to popcount
       over n-bit integers across n+1 targets (algorithmically O(n) if
       popcount is treated as O(1)); Space: O(1) beyond the bit integer.
"""


def convertStrToBit(s: str) -> int:
    res = 0
    for ch in s:
        res = res * 2 + (0 if ch == 'a' else 1)
    return res


def calculateFlips(num: int) -> int:
    res = 0
    while num > 0:
        res += num & 1
        num >>= 1
    return res


def minFlip(s: str) -> int:
    n = len(s)
    res = n

    target = convertStrToBit(s)
    mask = 1
    curr = 0
    for _ in range(n + 1):
        flips = calculateFlips(curr ^ target)
        res = min(res, flips)
        curr = curr | mask
        mask = mask << 1

    return res


if __name__ == "__main__":
    str1 = "abba"
    assert minFlip(str1) == 1

    str2 = "bbaaa"
    assert minFlip(str2) == 2

    str3 = "abbaaabababaaa"
    assert minFlip(str3) == 5
