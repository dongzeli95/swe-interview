"""
String Compression
https://leetcode.com/problems/string-compression

Given an array of characters chars, compress it in place. For each group of
consecutive repeating characters, append the character; if the group length is
greater than 1, also append the digits of the length. Return the new length.

Approaches:
    1. Solution.compress - Two-pointer in-place scan with a helper that writes
       the character (and multi-digit run-length) back into the array.
       Time: O(n), Space: O(1) extra (ignoring output string conversion).
"""

from typing import List


def _reassign_chars(chars: List[str], current: str, idx: int, counter: int) -> int:
    """Write `current` (and its run-length digits when counter > 1) starting at
    position `idx`. Returns the new write index."""
    chars[idx] = current
    idx += 1
    if counter == 1:
        return idx

    for ch in str(counter):
        chars[idx] = ch
        idx += 1
    return idx


class Solution:
    # Time: O(n), Space: O(1)
    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0

        res = 0
        counter = 1
        n = len(chars)
        idx = 0

        for i in range(1, n):
            if chars[i] == chars[i - 1]:
                counter += 1
            else:
                group_len = str(counter)
                # +1 for the character itself if the group length greater than 1.
                res += len(group_len) + (1 if counter > 1 else 0)
                # Reassign the character and group length to the original array.
                idx = _reassign_chars(chars, chars[i - 1], idx, counter)

                counter = 1

        # Add the last group length to the result length.
        group_len = str(counter)
        # +1 for the character itself if the group length greater than 1.
        res += len(group_len) + (1 if counter > 1 else 0)
        # Reassign the character and group length to the original array.
        idx = _reassign_chars(chars, chars[n - 1], idx, counter)

        return res


if __name__ == "__main__":
    sol = Solution()

    chars = ['a', 'a', 'b', 'b', 'c', 'c', 'c']
    assert sol.compress(chars) == 6
    assert chars[0] == 'a'
    assert chars[1] == '2'
    assert chars[2] == 'b'
    assert chars[3] == '2'
    assert chars[4] == 'c'
    assert chars[5] == '3'

    chars2 = ['a']
    assert sol.compress(chars2) == 1
    assert chars2[0] == 'a'

    chars3 = ['a', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
    assert sol.compress(chars3) == 4
    assert chars3[0] == 'a'
    assert chars3[1] == 'b'
    assert chars3[2] == '1'
    assert chars3[3] == '2'
