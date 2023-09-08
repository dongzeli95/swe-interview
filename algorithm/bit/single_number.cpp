// https://leetcode.com/problems/single-number

/*
Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.
You must implement a solution with a linear runtime complexity and use only constant extra space.

Ex1:
Input: nums = [2,2,1]
Output: 1

Ex2:
Input: nums = [4,1,2,1,2]
Output: 4

Ex3:
Input: nums = [1]
Output: 1

*/

#include <cassert>
#include <vector>
#include <iostream>

using namespace std;

// XOR, the number xor itself is 0.
// Time: O(n), Space: O(1)
int singleNumber(vector<int>& nums) {
    int n = nums.size();
    int res = 0;
    for (int i = 0; i < n; i++) {
        res ^= nums[i];
    }
    return res;
}

int main() {
    vector<int> nums = {2,2,1};
    assert(singleNumber(nums) == 1);
    nums = {4,1,2,1,2};
    assert(singleNumber(nums) == 4);
    nums = {1};
    assert(singleNumber(nums) == 1);
    return 0;
}