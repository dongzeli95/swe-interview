"""
House Robber
https://leetcode.com/problems/house-robber/

Given an integer array `nums` representing the amount of money at each house,
return the maximum amount of money you can rob tonight without robbing two
adjacent houses.

Approaches:
1. rob (Top-down recursion + memoization): Time O(n), Space O(n).
   Without memoization time would be O(n^2).
2. robWithDP (Bottom-up DP table): Time O(n), Space O(n).
"""

from typing import List


# Stack + Memoization
# Time complexity: O(n), Space complexity: O(n)
# Without memoization, time complexity is O(n^2)
cache: dict = {}


def robHelper(nums: List[int], idx: int) -> int:
    # Base case
    if idx < 0:
        return 0
    if idx == 0:
        return nums[0]

    if idx in cache:
        return cache[idx]

    res = max(
        robHelper(nums, idx - 1),
        robHelper(nums, idx - 2) + nums[idx],
    )
    cache[idx] = res
    return res


def rob(nums: List[int]) -> int:
    if not nums:
        return 0

    n = len(nums)
    return robHelper(nums, n - 1)


# DP
# Time complexity: O(n), Space complexity: O(n)
def robWithDP(nums: List[int]) -> int:
    if not nums:
        return 0

    n = len(nums)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        if i == 1:
            dp[i] = nums[i - 1]
        else:
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])

    return dp[n]


if __name__ == "__main__":
    nums = [2, 7, 9, 3, 1]
    assert rob(nums) == 12
    assert robWithDP(nums) == 12

    cache.clear()
    nums = [1, 2, 3, 1]
    assert rob(nums) == 4
    assert robWithDP(nums) == 4
