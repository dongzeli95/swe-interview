```cpp
// https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee

/*
You are given an array prices where prices[i] is the price of a given stock on the ith day, and an integer fee representing a transaction fee.

Find the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the transaction fee for each transaction.

Note:

You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
The transaction fee is only charged once for each stock purchase and sale.

Ex1:
Input: prices = [1,3,2,8,4,9], fee = 2
Output: 8
Explanation: The maximum profit can be achieved by:
- Buying at prices[0] = 1
- Selling at prices[3] = 8
- Buying at prices[4] = 4
- Selling at prices[5] = 9
The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.

Ex2:
Input: prices = [1,3,7,5,10,3], fee = 3
Output: 6

*/

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

/*
Intuition:

dp[i] represents the maximum profit on day i without holding the stock.
Two states: 
1. Not holding the stock from previous day: dp[i] = dp[i-1]
2. Holding the stock and sell it today: prices[i] - min_cost - fee

min_cost keeps track of minimum effective cost of the stock until day i.
Two states:
1. Not holding the stock from previous day -> buy it today: min_cost = prices[i] - dp[i-1]
2. Holding the stock from previous day -> do nothing: min_cost = min_cost

*/

// Time complexity: O(n), Space complexity: O(n)
int maxProfit(vector<int>& prices, int fee) {
    int n = prices.size();
    if (n <= 1) {
        return 0;
    }

    vector<int> dp(n, 0);
    int min_price = prices[0];
    for (int i = 1; i < n; i++) {
        dp[i] = max(dp[i-1], prices[i] - min_price - fee);
        min_price = min(min_price, prices[i] - dp[i-1]); 
    }

    return dp[n-1];
}

// Time complexity: O(n), Space complexity: O(1)
int maxProfitWithSpaceOptimization(vector<int>& prices, int fee) {
    int n = prices.size();
    if (n <= 1) {
        return 0;
    }

    int mx = 0;
    int min_price = prices[0];
    for (int i = 1; i < n; i++) {
        int prev_mx = mx;
        mx = max(mx, prices[i] - min_price - fee);
        min_price = min(min_price, prices[i] - prev_mx);
    }

    return mx;
}

int main() {
    vector<int> prices = {1,3,2,8,4,9};
    int fee = 2;
    assert(maxProfit(prices, fee) == 8);
    assert(maxProfitWithSpaceOptimization(prices, fee) == 8);

    prices = {1,3,7,5,10,3};
    fee = 3;
    assert(maxProfit(prices, fee) == 6);
    assert(maxProfitWithSpaceOptimization(prices, fee) == 6);
    return 0;
}

```
