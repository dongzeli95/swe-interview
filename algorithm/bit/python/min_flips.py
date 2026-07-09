"""
Minimum Flips to Make a OR b Equal to c
https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c

Given 3 positive numbers a, b, and c, return the minimum number of bit flips
required in a and b so that (a OR b) == c.

Approaches:
    1. Bit-by-bit scan comparing (a | b) against c.
       Time: O(n) over n bits. Space: O(1).
"""


def extract_bit(num: int, pos: int) -> int:
    return (num & (1 << pos)) >> pos


# Time: O(n), n bits.
# Space: O(1)
def minFlips(a: int, b: int, c: int) -> int:
    or_res = a | b
    if or_res == c:
        return 0

    pos = 0
    res = 0

    # We have to use max here since the largest bit can
    # exist in both c or or_res.
    mx = c | or_res
    while mx > 0:
        or_res_bit = extract_bit(or_res, pos)
        c_bit = extract_bit(c, pos)
        if or_res_bit != c_bit:
            if or_res_bit == 0:
                res += 1
            else:
                a_bit = extract_bit(a, pos)
                b_bit = extract_bit(b, pos)
                res += 2 if a_bit == b_bit else 1

        mx = mx >> 1
        pos += 1

    return res


if __name__ == "__main__":
    assert minFlips(2, 6, 5) == 3
    assert minFlips(4, 2, 7) == 1
    assert minFlips(1, 2, 3) == 0
    assert minFlips(8, 3, 5) == 3
    assert minFlips(2, 5, 8) == 4
