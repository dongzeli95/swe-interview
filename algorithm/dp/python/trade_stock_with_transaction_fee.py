"""
Best Time to Buy and Sell Stock with Transaction Fee
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee

You are given an array prices where prices[i] is the price of a given stock on
the ith day, and an integer fee representing a transaction fee. Find the
maximum profit you can achieve. You may complete as many transactions as you
like, but you need to pay the transaction fee for each transaction.

Approaches:
1. max_profit                            - DP with O(n) time and O(n) space.
2. max_profit_with_space_optimization    - DP with O(n) time and O(1) space.

Intuition:
    dp[i] represents the maximum profit on day i without holding the stock.
    Two states:
      1. Not holding the stock from previous day: dp[i] = dp[i-1]
      2. Holding the stock and sell it today: prices[i] - min_cost - fee

    min_price keeps track of minimum effective cost of the stock until day i.
    Two states:
      1. Not holding from previous day -> buy today: min_price = prices[i] - dp[i-1]
      2. Holding from previous day -> do nothing: min_price = min_price
"""

from typing import List


# Time complexity: O(n), Space complexity: O(n)
def max_profit(prices: List[int], fee: int) -> int:
    n = len(prices)
    if n <= 1:
        return 0

    dp = [0] * n
    min_price = prices[0]
    for i in range(1, n):
        dp[i] = max(dp[i - 1], prices[i] - min_price - fee)
        min_price = min(min_price, prices[i] - dp[i - 1])

    return dp[n - 1]


# Time complexity: O(n), Space complexity: O(1)
def max_profit_with_space_optimization(prices: List[int], fee: int) -> int:
    n = len(prices)
    if n <= 1:
        return 0

    mx = 0
    min_price = prices[0]
    for i in range(1, n):
        prev_mx = mx
        mx = max(mx, prices[i] - min_price - fee)
        min_price = min(min_price, prices[i] - prev_mx)

    return mx


if __name__ == "__main__":
    prices = [1, 3, 2, 8, 4, 9]
    fee = 2
    assert max_profit(prices, fee) == 8
    assert max_profit_with_space_optimization(prices, fee) == 8

    prices = [1, 3, 7, 5, 10, 3]
    fee = 3
    assert max_profit(prices, fee) == 6
    assert max_profit_with_space_optimization(prices, fee) == 6
