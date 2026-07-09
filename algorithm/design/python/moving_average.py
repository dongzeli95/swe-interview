"""
Moving Average from Data Stream
https://leetcode.com/problems/moving-average-from-data-stream/

Approaches:
1. MovingAverage (deque + running sum): next() runs in O(1) time, O(size) space.
"""

from collections import deque


# Time: O(1), Space: O(size)
class MovingAverage:
    def __init__(self, size: int):
        self.s = size
        self.nums = deque()
        self.sum = 0

    def next(self, val: int) -> float:
        self.sum += val
        self.nums.append(val)
        if len(self.nums) > self.s:
            self.sum -= self.nums.popleft()

        return self.sum / len(self.nums)


if __name__ == "__main__":
    ma = MovingAverage(3)
    print(ma.next(1))
    print(ma.next(10))
    print(ma.next(3))
    print(ma.next(5))
