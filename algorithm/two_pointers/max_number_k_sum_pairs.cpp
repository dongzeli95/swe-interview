// https://leetcode.com/problems/max-number-of-k-sum-pairs

/*
You are given an integer array nums and an integer k.
In one operation, you can pick two numbers from the array whose sum equals k and remove them from the array.
Return the maximum number of operations you can perform on the array.

Ex1:
Input: nums = [1,2,3,4], k = 5
Output: 2
Explanation: Starting with nums = [1,2,3,4]:
- Remove numbers 1 and 4, then nums = [2,3]
- Remove numbers 2 and 3, then nums = []
There are no more pairs that sum up to 5, hence a total of 2 operations.

Ex2:
Input: nums = [3,1,3,4,3], k = 6
Output: 1
Explanation: Starting with nums = [3,1,3,4,3]:
- Remove the first two 3's, then nums = [1,4,3]
There are no more pairs that sum up to 6, hence a total of 1 operation.
*/

#include <vector>
#include <unordered_map>
#include <cassert>
#include <iostream>

using namespace std;

// Time complexity: O(n), Space complexity: O(n)
int maxOperations(vector<int>& nums, int k) {
    if (nums.empty()) {
        return 0;
    }

    unordered_map<int, int> m;
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        m[nums[i]]++;
    }

    int res = 0;
    for (auto i : m) {
        int val = i.first;
        int cnt = i.second;
        if (cnt <= 0) continue;

        if (m.count(k-val) && m[k-val] > 0) {
            if (k-val == val) {
                res += cnt / 2;
                m[k-val] = 0;
            } else {
                res += min(cnt, m[k-val]);
                // Don't forget to clear all values to 0.
                m[k-val] = 0;
                m[val] = 0;
            }
        }
    }

    return res;
}

// Two pointers
// Time complexity: O(nlogn), Space complexity: O(1)
int maxOperationsTwoPointer(vector<int>& nums, int k) {
    if (nums.empty()) {
        return 0;
    }

    sort(nums.begin(), nums.end());
    int res = 0;
    int n = nums.size();

    int l = 0, r = n-1;

    while (l < r) {
        int sum = nums[l] + nums[r];
        if (sum > k) {
            r--;
        } else if (sum < k) {
            l++;
        } else {
            res++;
            l++;
            r--;
        }
    }

    return res;
}

int main() {
    vector<int> nums {1,2,3,4};
    int k = 5;
    assert(maxOperations(nums, k) == 2);
    assert(maxOperationsTwoPointer(nums, k) == 2);

    nums = {3,1,3,4,3};
    k = 6;
    assert(maxOperations(nums, k) == 1);
    assert(maxOperationsTwoPointer(nums, k) == 1);

    nums = {2, 2, 2, 3, 1, 1, 4, 1};
    k = 4;
    assert(maxOperations(nums, k) == 2);
    assert(maxOperationsTwoPointer(nums, k) == 2);

    nums = {2,5,4,4,1,3,4,4,1,4,4,1,2,1,2,2,3,2,4,2};
    k = 3;
    assert(maxOperations(nums, k) == 4);
    assert(maxOperationsTwoPointer(nums, k) == 4);

    return 0;
}