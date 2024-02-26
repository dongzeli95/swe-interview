```cpp
#include <vector>

using namespace std;

// https://blog.bhxya.com/blog/start-from-knapsack-problem
// 01背包
// 有 N 件物品和一个容量为 v 的背包。放入第 i 件物品耗费的费用是 Ci，得到的价值是 Wi。 求解将哪些物品装入背包可使价值总和最大。
// F[i, v]表示使用i件物品放入v容积背包中能获得最大价值
// 其状态转移方程便是：F[i, v] = max{ F[i − 1, v], F[i − 1, v − Ci] + Wi }

// https://leetcode.com/problems/partition-equal-subset-sum/description/
/*
Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.
Ex1:
Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].

Ex2:
Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.

*/

// Time: O(n*sum), Space: O(n*sum) -> O(sum), compression
bool canPartition(vector<int>& nums) {
    int sum = 0;
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        sum += nums[i];
    }

    if (sum % 2 != 0) {
        return false;
    }

    vector<vector<bool>> dp(n + 1, vector<bool>(sum / 2 + 1, false));
    dp[0][0] = true;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= sum / 2; j++) {
            dp[i][j] = dp[i][j] || dp[i - 1][j];
            if (j - nums[i - 1] >= 0) {
                dp[i][j] = dp[i][j] || dp[i - 1][j - nums[i - 1]];
            }
        }
    }

    return dp[n][sum / 2];
}

// https://leetcode.com/problems/last-stone-weight-ii/description/
/*
You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose any two stones and smash them together. Suppose the stones have weights x and y with x <= y. The result of this smash is:

If x == y, both stones are destroyed, and
If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
At the end of the game, there is at most one stone left.

Return the smallest possible weight of the left stone. If there are no stones left, return 0.

Ex1:
Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation:
We can combine 2 and 4 to get 2, so the array converts to [2,7,1,8,1] then,
we can combine 7 and 8 to get 1, so the array converts to [2,1,1,1] then,
we can combine 2 and 1 to get 1, so the array converts to [1,1,1] then,
we can combine 1 and 1 to get 0, so the array converts to [1], then that's the optimal value.

Ex2:
Input: stones = [31,26,33,21,40]
Output: 5

*/

// Time: O(n*sum), Space: O(n*sum) -> O(sum)
int lastStoneWeightII(vector<int>& nums) {
    int sum = 0;
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        sum += nums[i];
    }

    vector<vector<int>> dp(n + 1, vector<int>(sum / 2 + 1, 0));
    dp[0][0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= sum / 2; j++) {
            dp[i][j] = max(dp[i][j], dp[i - 1][j]);
            if (j - nums[i - 1] >= 0) {
                dp[i][j] = max(dp[i][j], dp[i - 1][j - nums[i - 1]] + nums[i - 1]);
            }
        }
    }

    return abs(sum - dp[n][sum / 2] * 2);
}

// 完全背包
// 有 N 件物品和一个容量为 V 的背包。每种物品都有无限件可用。放入第 i 件物品耗费的费用是 Ci，得到的价值是 Wi。 
// 求解将哪些物品装入背包可使价值总和最大。
// 正循环v使得物品有无限件可拿

// https://leetcode.com/problems/perfect-squares/description/
/*
Given an integer n, return the least number of perfect square numbers that sum to n.
A perfect square is an integer that is the square of an integer; 
in other words, it is the product of some integer with itself. 
For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.

Ex1:
Input: n = 12
Output: 3
Explanation: 12 = 4 + 4 + 4.

Ex2:
Input: n = 13
Output: 2
Explanation: 13 = 4 + 9.

*/

// dp[i][j] = min number of perfect square that can form number j using 0-ith squares.
// dp[i][j] = min(dp[i][j-nums[i]]+1, dp[i-1][j])
// Time: O(n * sqrt(n)), Space: O(n * sqrt(n))
int numSquares(int n) {
    vector<int> candidates;
    int c = 1;
    while (c * c <= n) {
        candidates.push_back(c * c);
        c++;
    }

    int numC = candidates.size();
    vector<vector<int>> dp(numC + 1, vector<int>(n + 1, INT_MAX));
    dp[0][0] = 0;
    for (int i = 1; i <= numC; i++) {
        for (int j = 0; j <= n; j++) {
            if (dp[i - 1][j] != -1) {
                dp[i][j] = dp[i - 1][j];
            }
            if (j - candidates[i - 1] >= 0 && dp[i][j - candidates[i - 1]] != -1) {
                dp[i][j] = min(dp[i][j], 1 + dp[i][j - candidates[i - 1]]);
            }
        }
    }

    return dp[numC][n];
}

// https://leetcode.com/problems/coin-change/description/

/*

You are given an integer array coins representing coins of different denominations 
and an integer amount representing a total amount of money.
Return the fewest number of coins that you need to make up that amount. 
If that amount of money cannot be made up by any combination of the coins, return -1.
You may assume that you have an infinite number of each kind of coin.

Ex1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Ex2:
Input: coins = [2], amount = 3
Output: -1

Ex3:
Input: coins = [1], amount = 0
Output: 0

*/

// Time: O(amount*coins), Space: O(amount)
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; ++i) {
        for (int j = 0; j < coins.size(); ++j) {
            if (coins[j] <= i) {
                dp[i] = min(dp[i], dp[i - coins[j]] + 1);
            }
        }
    }
    return (dp[amount] > amount) ? -1 : dp[amount];
}```
