"""
Single Number (https://leetcode.com/problems/single-number)

Given a non-empty array of integers nums, every element appears twice except
for one. Find that single one. Must use linear time and constant extra space.

Approaches:
    1. singleNumber - XOR fold across the array. Time: O(n), Space: O(1).
"""

from typing import List


# XOR, the number xor itself is 0.
# Time: O(n), Space: O(1)
def singleNumber(nums: List[int]) -> int:
    res = 0
    for x in nums:
        res ^= x
    return res


if __name__ == "__main__":
    assert singleNumber([2, 2, 1]) == 1
    assert singleNumber([4, 1, 2, 1, 2]) == 4
    assert singleNumber([1]) == 1
