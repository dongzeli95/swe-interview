"""
Knapsack DP problems (ported 1-to-1 from cpp/knapsack.cpp).

Background:
    01 Knapsack: N items, capacity V, each item picked at most once.
        F[i, v] = max(F[i-1, v], F[i-1, v - C_i] + W_i)
    Unbounded (Complete) Knapsack: each item has unlimited copies.
        Iterate v forward so items can be re-used.

Approaches (each is a stand-alone LeetCode problem):
    1. canPartition        - Partition Equal Subset Sum (01 knapsack, bool DP).
                             Time: O(n * sum), Space: O(n * sum).
    2. lastStoneWeightII   - Last Stone Weight II (01 knapsack, max value DP).
                             Time: O(n * sum), Space: O(n * sum).
    3. numSquares          - Perfect Squares (unbounded knapsack).
                             Time: O(n * sqrt(n)), Space: O(n * sqrt(n)).
    4. coinChange          - Coin Change (unbounded knapsack, compressed 1-D).
                             Time: O(amount * len(coins)), Space: O(amount).
"""

from typing import List


# https://leetcode.com/problems/partition-equal-subset-sum/description/
# Time: O(n*sum), Space: O(n*sum) -> O(sum), compression
def canPartition(nums: List[int]) -> bool:
    total = sum(nums)
    n = len(nums)

    if total % 2 != 0:
        return False

    half = total // 2
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        for j in range(half + 1):
            dp[i][j] = dp[i][j] or dp[i - 1][j]
            if j - nums[i - 1] >= 0:
                dp[i][j] = dp[i][j] or dp[i - 1][j - nums[i - 1]]

    return dp[n][half]


# https://leetcode.com/problems/last-stone-weight-ii/description/
# Time: O(n*sum), Space: O(n*sum) -> O(sum)
def lastStoneWeightII(nums: List[int]) -> int:
    total = sum(nums)
    n = len(nums)

    half = total // 2
    dp = [[0] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(half + 1):
            dp[i][j] = max(dp[i][j], dp[i - 1][j])
            if j - nums[i - 1] >= 0:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - nums[i - 1]] + nums[i - 1])

    return abs(total - dp[n][half] * 2)


# https://leetcode.com/problems/perfect-squares/description/
# dp[i][j] = min number of perfect squares that can form number j using 0..i-1 squares.
# dp[i][j] = min(dp[i][j - nums[i-1]] + 1, dp[i-1][j])  (unbounded: reuses dp[i][...])
# Time: O(n * sqrt(n)), Space: O(n * sqrt(n))
def numSquares(n: int) -> int:
    candidates = []
    c = 1
    while c * c <= n:
        candidates.append(c * c)
        c += 1

    num_c = len(candidates)
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(num_c + 1)]
    dp[0][0] = 0
    for i in range(1, num_c + 1):
        for j in range(n + 1):
            if dp[i - 1][j] != INF:
                dp[i][j] = dp[i - 1][j]
            if j - candidates[i - 1] >= 0 and dp[i][j - candidates[i - 1]] != INF:
                dp[i][j] = min(dp[i][j], 1 + dp[i][j - candidates[i - 1]])

    return dp[num_c][n]


# https://leetcode.com/problems/coin-change/description/
# Time: O(amount*coins), Space: O(amount)
def coinChange(coins: List[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for j in range(len(coins)):
            if coins[j] <= i:
                dp[i] = min(dp[i], dp[i - coins[j]] + 1)
    return -1 if dp[amount] > amount else dp[amount]
