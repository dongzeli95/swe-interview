"""
Count All Valid Pickup and Delivery Options (LeetCode 1359)

Given n orders, each has a pickup (P_i) and a delivery (D_i), count the number
of valid sequences where every P_i appears before its corresponding D_i.

Intuition: When adding the n-th order to a valid sequence of (n-1) orders
(which has 2*(n-1) items), we can:
  1. Insert the pickup at any of 2*(n-1)+1 positions.
  2. Then insert the delivery after the pickup. If pickup goes in slot k
     (1-indexed), delivery has 2*(n-1)+1 - (k-1) options.
Summing over k from 1..2*(n-1)+1 gives 1+2+...+(2n-1) = n*(2n-1).
Therefore: dp[i] = dp[i-1] * i * (2*i - 1).

Approaches:
  1. countOrders: bottom-up DP with 1D array. Time O(n), Space O(n).
"""


# Time: O(n), Space: O(n) -> O(1)
def countOrders(n: int) -> int:
    dp = [0] * (n + 1)
    dp[1] = 1

    mod = 10**9 + 7

    for i in range(2, n + 1):
        dp[i] = dp[i - 1]
        dp[i] *= i
        dp[i] = dp[i] % mod
        dp[i] *= (2 * i - 1)
        dp[i] = dp[i] % mod

    return dp[n]
