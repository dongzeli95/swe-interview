# Buy And Sell Stock

````cpp
// https://leetcode.com/problems/best-time-to-buy-and-sell-stock

/*
You are given an array prices where prices[i] is the price of a given stock on the ith day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
Return the maximum profit you can achieve from this transaction. 
If you cannot achieve any profit, return 0.
 
Ex1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Ex2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.

*/

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(1)
int maxProfit(vector<int>& prices) {
    if (prices.empty()) {
        return 0;
    }

    int res = 0;
    int n = prices.size();
    int mn = prices[0];

    for (int i = 1; i < n; i++) {
        res = max(res, prices[i]-mn);
        mn = min(mn, prices[i]);
    }

    return res;
}

// https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii

/*
You are given an integer array prices where prices[i] is the price of a given stock on the ith day.
On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. 
However, you can buy it then immediately sell it on the same day.
Find and return the maximum profit you can achieve.

Ex1:
Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.

Ex2:
Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Total profit is 4.

Ex3:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.
*/

int maxProfitMultipleTimes(vector<int>& prices) {
    int n = prices.size();
    int res = 0;

    for (int i = 1; i < n; i++) {
        int diff = prices[i] - prices[i - 1];
        res += (diff > 0) ? diff : 0;
    }

    return res;
}

// https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii
/*
You are given an array prices where prices[i] is the price of a given stock on the ith day.
Find the maximum profit you can achieve. You may complete at most two transactions.
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

Ex1:
Input: prices = [3,3,5,0,0,3,1,4]
Output: 6
Explanation: Buy on day 4 (price = 0) and sell on day 6 (price = 3), profit = 3-0 = 3.
Then buy on day 7 (price = 1) and sell on day 8 (price = 4), profit = 4-1 = 3.

Ex2:
Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Note that you cannot buy on day 1, buy on day 2 and sell them later, as you are engaging multiple transactions at the same time. 
You must sell before buying again.

Ex3:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transaction is done, i.e. max profit = 0.
*/

int maxProfitWithTwoTrades(vector<int>& prices) {
    int t1Cost = INT_MAX,
        t2Cost = INT_MAX;
    int t1Profit = 0,
        t2Profit = 0;

    for (int price : prices) {
        // the maximum profit if only one transaction is allowed
        t1Cost = min(t1Cost, price);
        t1Profit = max(t1Profit, price - t1Cost);
        // re-invest the gained profit in the second transaction
        t2Cost = min(t2Cost, price - t1Profit);
        t2Profit = max(t2Profit, price - t2Cost);
    }

    return t2Profit;
}

// TODO: two pass solution.

// https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
/*
You are given an integer array prices where prices[i] is the price of a given stock on the ith day, and an integer k.
Find the maximum profit you can achieve. You may complete at most k transactions: i.e. you may buy at most k times and sell at most k times.
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

Ex1:
Input: k = 2, prices = [2,4,1]
Output: 2
Explanation: Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 4-2 = 2.

Ex2:
Input: k = 2, prices = [2,4,1]
Output: 2
Explanation: Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 4-2 = 2.

*/

// Time: O(n), Space: O(k)
int maxProfitWithKTrades(vector<int>& prices, int k) {
    vector<int> costs(k, INT_MAX);
    vector<int> profits(k, 0);

    for (int price : prices) {
        costs[0] = min(costs[0], price);
        profits[0] = max(profits[0], price-costs[0]);
        for (int i = 1; i < k; i++) {
            costs[i] = min(costs[i], price - profits[i-1]);
            profits[i] = max(profits[i], price - costs[i]);
        }
    }

    return profits[k-1];
}

int main() {
    vector<int> prices1 = {7,1,5,3,6,4};
    assert(maxProfit(prices1) == 5);
    assert(maxProfitMultipleTimes(prices1) == 7);

    vector<int> prices2 = {7,6,4,3,1};
    assert(maxProfit(prices2) == 0);
    assert(maxProfitMultipleTimes(prices2) == 0);
    assert(maxProfitWithTwoTrades(prices2) == 0);

    vector<int> prices3 = {1,2,3,4,5};
    assert(maxProfitMultipleTimes(prices3) == 4);
    assert(maxProfitWithTwoTrades(prices3) == 4);

    vector<int> prices4 = {3, 3, 5, 0, 0, 3, 1, 4};
    assert(maxProfitWithTwoTrades(prices4) == 6);

    vector<int> prices5 = {2, 4, 1};
    assert(maxProfitWithKTrades(prices5, 2) == 2);

    vector<int> prices6 = {3, 2, 6, 5, 0, 3};
    assert(maxProfitWithKTrades(prices6, 2) == 7);

    vector<int> prices7 = {1, 2, 3, 0, 2};
    assert(maxProfitWithCD(prices7) == 3);

    vector<int> prices8 = {1};
    assert(maxProfitWithCD(prices8) == 0);

    vector<int> prices9 = {1, 2, 4};
    assert(maxProfitWithCD(prices9) == 3);
    return 0;
}```
````

<img src="../../../.gitbook/assets/file.excalidraw (9).svg" alt="" class="gitbook-drawing">

```cpp

// https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
/*

You are given an array prices where prices[i] is the price of a given stock on the ith day.
Find the maximum profit you can achieve.
You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:
After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

Ex1:
Input: prices = [1,2,3,0,2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]

Ex2:
Input: prices = [1]
Output: 0

*/

// state machine

// Time: O(n), Space:O(1)
int maxProfitWithCD(vector<int>& prices) {
    int sold = INT_MIN, held = INT_MIN, reset = 0;

    for (int price : prices) {
        int preSold = sold;

        sold = held + price;
        held = max(held, reset - price);
        reset = max(reset, preSold);
    }

    return max(sold, reset);
}
```
