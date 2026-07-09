"""
Best Time to Buy and Sell Stock (family of problems).

Ports algorithm/dp/cpp/buy_and_sell_stock.cpp one-to-one.

Approaches:
    1. max_profit
        LeetCode 121 — Best Time to Buy and Sell Stock (single transaction).
        Track running minimum price, update best (price - min).
        Time: O(n), Space: O(1).

    2. max_profit_multiple_times
        LeetCode 122 — Best Time to Buy and Sell Stock II (unlimited transactions).
        Sum every positive daily delta (greedy).
        Time: O(n), Space: O(1).

    3. max_profit_with_two_trades
        LeetCode 123 — Best Time to Buy and Sell Stock III (at most 2 transactions).
        Roll two (cost, profit) states forward; reinvest first profit into the
        second buy.
        Time: O(n), Space: O(1).

    4. max_profit_with_k_trades
        LeetCode 188 — Best Time to Buy and Sell Stock IV (at most k transactions).
        Generalises approach 3 with k parallel (cost, profit) states.
        Time: O(n * k), Space: O(k).

    5. max_profit_with_cd
        LeetCode 309 — Best Time to Buy and Sell Stock with Cooldown.
        State machine over {sold, held, reset}, one day of cooldown after a sell.
        Time: O(n), Space: O(1).
"""

from typing import List


# Time: O(n), Space: O(1)
def max_profit(prices: List[int]) -> int:
    if not prices:
        return 0

    res = 0
    mn = prices[0]

    for i in range(1, len(prices)):
        res = max(res, prices[i] - mn)
        mn = min(mn, prices[i])

    return res


def max_profit_multiple_times(prices: List[int]) -> int:
    n = len(prices)
    res = 0

    for i in range(1, n):
        diff = prices[i] - prices[i - 1]
        res += diff if diff > 0 else 0

    return res


def max_profit_with_two_trades(prices: List[int]) -> int:
    t1_cost = float('inf')
    t2_cost = float('inf')
    t1_profit = 0
    t2_profit = 0

    for price in prices:
        # the maximum profit if only one transaction is allowed
        t1_cost = min(t1_cost, price)
        t1_profit = max(t1_profit, price - t1_cost)
        # re-invest the gained profit in the second transaction
        t2_cost = min(t2_cost, price - t1_profit)
        t2_profit = max(t2_profit, price - t2_cost)

    return t2_profit


# TODO: two pass solution.


# Time: O(n), Space: O(k)
def max_profit_with_k_trades(prices: List[int], k: int) -> int:
    costs = [float('inf')] * k
    profits = [0] * k

    for price in prices:
        costs[0] = min(costs[0], price)
        profits[0] = max(profits[0], price - costs[0])
        for i in range(1, k):
            costs[i] = min(costs[i], price - profits[i - 1])
            profits[i] = max(profits[i], price - costs[i])

    return profits[k - 1]


# state machine
# Time: O(n), Space: O(1)
def max_profit_with_cd(prices: List[int]) -> int:
    sold = float('-inf')
    held = float('-inf')
    reset = 0

    for price in prices:
        pre_sold = sold

        sold = held + price
        held = max(held, reset - price)
        reset = max(reset, pre_sold)

    return max(sold, reset)


if __name__ == "__main__":
    prices1 = [7, 1, 5, 3, 6, 4]
    assert max_profit(prices1) == 5
    assert max_profit_multiple_times(prices1) == 7

    prices2 = [7, 6, 4, 3, 1]
    assert max_profit(prices2) == 0
    assert max_profit_multiple_times(prices2) == 0
    assert max_profit_with_two_trades(prices2) == 0

    prices3 = [1, 2, 3, 4, 5]
    assert max_profit_multiple_times(prices3) == 4
    assert max_profit_with_two_trades(prices3) == 4

    prices4 = [3, 3, 5, 0, 0, 3, 1, 4]
    assert max_profit_with_two_trades(prices4) == 6

    prices5 = [2, 4, 1]
    assert max_profit_with_k_trades(prices5, 2) == 2

    prices6 = [3, 2, 6, 5, 0, 3]
    assert max_profit_with_k_trades(prices6, 2) == 7

    prices7 = [1, 2, 3, 0, 2]
    assert max_profit_with_cd(prices7) == 3

    prices8 = [1]
    assert max_profit_with_cd(prices8) == 0

    prices9 = [1, 2, 4]
    assert max_profit_with_cd(prices9) == 3

    print("All assertions passed.")
