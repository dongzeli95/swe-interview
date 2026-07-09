"""
LeetCode 900: RLE Iterator
https://leetcode.com/problems/rle-iterator/

Design an iterator that iterates through a run-length encoded sequence.

Approaches:
    1. RLEIterator - In-place decrement on the current run.
       next(n): O(k) amortized over all calls where k = pairs consumed
       (each pair is visited at most once across the lifetime of the iterator).
       Space: O(1) extra (stores the encoding by reference/copy).
"""

from typing import List


class RLEIterator:
    def __init__(self, encoding: List[int]):
        self.encoding = encoding
        self.idx = 0

    def next(self, n: int) -> int:
        while n > 0 and self.idx < len(self.encoding):
            if n > self.encoding[self.idx]:
                n -= self.encoding[self.idx]
                self.idx += 2
            else:
                self.encoding[self.idx] -= n
                break

        if self.idx + 1 >= len(self.encoding):
            return -1

        return self.encoding[self.idx + 1]
