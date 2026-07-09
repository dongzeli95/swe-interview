"""
LeetCode 398: Random Pick Index
https://leetcode.com/problems/random-pick-index/

Given an integer array nums with possible duplicates, randomly output the
index of a given target number. Each valid index must be returned with
equal probability.

Approaches:
1. IndexPicker (hash map of indices): __init__ O(n) time / O(n) space,
   pick O(1) time — precompute a map from value -> list of indices and
   sample uniformly from the list.
2. Solution (reservoir sampling): __init__ O(1) time / O(n) space (just
   store reference), pick O(n) time / O(1) extra space — scan and keep
   the current candidate with probability 1/count.
"""

import random
from collections import defaultdict
from typing import List


class IndexPicker:
    def __init__(self, nums: List[int]):
        self.nums = nums
        self.m = defaultdict(list)
        for i, v in enumerate(nums):
            self.m[v].append(i)

    def pick(self, num: int) -> int:
        if num not in self.m:
            return -1
        indices = self.m[num]
        n = len(indices)
        idx = random.randrange(n)
        return indices[idx]


# Reservoir Sampling
# Shuffle an array
# Linked List Random Node.
class Solution:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        n = len(self.nums)
        count = 0
        idx = 0
        for i in range(n):
            # if nums[i] is equal to target, i is a potential candidate
            # which needs to be chosen uniformly at random
            if self.nums[i] == target:
                # increment the count of total candidates
                # available to be chosen uniformly at random
                count += 1
                # we pick the current number with probability 1 / count (reservoir sampling)
                if random.randrange(count) == 0:
                    idx = i
        return idx
