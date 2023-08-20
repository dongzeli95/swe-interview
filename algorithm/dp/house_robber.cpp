// https://leetcode.com/problems/house-robber/

/*
You are a professional robber planning to rob houses along a street. 
Each house has a certain amount of money stashed, 
the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

Ex1:
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Ex2:
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.

*/

#include <vector>
#include <iostream>
#include <unordered_map>

using namespace std;

// Stack + Memorization
// Time complexity: O(n), Space complexity: O(n)
// Without memorization, time complexity is O(n^2)
unordered_map<int, int> cache;
int robHelper(vector<int>& nums, int idx) {
    // Base case
    if (idx < 0) {
        return 0;
    }
    if (idx == 0) {
        return nums[0];
    }

    if (cache.count(idx)) {
        return cache[idx];
    }

    int res = max(robHelper(nums, idx - 1),
        robHelper(nums, idx - 2) + nums[idx]);
    cache[idx] = res;
    return res;
}

int rob(vector<int>& nums) {
    if (nums.empty()) {
        return 0;
    }

    int n = nums.size();
    return robHelper(nums, n-1);
}

// DP
// Time complexity: O(n), Space complexity: O(n)
int robWithDP(vector<int>& nums) {
    if (nums.empty()) {
        return 0;
    }

    int n = nums.size();
    vector<int> dp(n+1, 0);
    for (int i = 1; i <= n; i++) {
        if (i == 1) {
            dp[i] = nums[i-1];
        } else {
            dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]);
        }
    }
    
    return dp[n];
}

int main() {
    vector<int> nums = {2,7,9,3,1};
    assert(rob(nums) == 12);
    assert(robWithDP(nums) == 12);

    cache.clear();
    nums = {1,2,3,1};
    assert(rob(nums) == 4);
    assert(robWithDP(nums) == 4);

    return 0;
}