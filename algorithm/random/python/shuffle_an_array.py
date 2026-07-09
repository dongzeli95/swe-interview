"""
Shuffle an Array
https://leetcode.com/problems/shuffle-an-array/

Given an integer array nums, design an algorithm to randomly shuffle the array.
All permutations of the array should be equally likely as a result of the shuffling.

Approaches:
1. Shuffle (Fisher-Yates): O(n) time, O(n) space for storing the original array.
"""

import random
from typing import List


# Time: O(n), Space: O(n)
# Fisher-Yates algorithm
class Shuffle:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def shuffle(self) -> List[int]:
        shuffled = list(self.nums)
        n = len(shuffled)
        for i in range(n):
            idx = i + random.randint(0, n - i - 1)
            shuffled[i], shuffled[idx] = shuffled[idx], shuffled[i]
        return shuffled

    def reset(self) -> List[int]:
        return self.nums
