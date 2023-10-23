```cpp
// https://leetcode.com/problems/increasing-triplet-subsequence
// Given an integer array nums, return true if there exists a triple of indices(i, j, k)
// such that i < j < k and nums[i] < nums[j] < nums[k].If no such indices exists, return false.

// Ex1: 
// Input : nums = [ 1, 2, 3, 4, 5 ] 
// Output : true 
// Explanation : Any triplet where i < j < k is valid.

// Ex2: 
// Input : nums = [ 5, 4, 3, 2, 1 ] 
// Output : false 
// Explanation : No triplet exists.

// Ex3: Input: nums = [ 2, 1, 5, 0, 4, 6 ]
// Output : true 
// Explanation : The triplet(3, 4, 5) is valid because nums[3] == 0 < nums[4] == 4 < nums[5] == 6.

// num1, num2, num3
// 2
// 1
// 1, 5
// [0], [1, 5]
// [0, 4], [1, 5]
// [0, 4, 6], [1, 5, 6]

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(1)
bool increasingTriplet(vector<int>& nums) {
  if (nums.empty()) {
    return false;
  }

    int n = nums.size();
    int num1 = nums[0];
    int num2 = INT_MAX;

    for (int i = 1; i < n; i++) {
        // Need = sign here to handle case like [1, 1, 1, 1, 1]
        // We only place the number at the next position if it is strictly larger than the current number.
        // If less or equal, we just update the number at current position.
        if (nums[i] <= num1) {
            num1 = nums[i];
        } else if (nums[i] <= num2) {
            num2 = nums[i];
        } else {
            return true;
        }
    }

    return false;
}

int main() {
    vector<int> nums = { 2, 1, 5, 0, 4, 6 };
    assert(increasingTriplet(nums) == true);

    nums = {1, 1, 1, 1, 1};
    assert(increasingTriplet(nums) == false);

    nums = {2, 1, 5, 0, 6};
    assert(increasingTriplet(nums) == true);

    nums = {2, 1, 5, 0, 1, 2};
    assert(increasingTriplet(nums) == true);

    nums = { 5, 4, 3, 2, 1 };
    assert(increasingTriplet(nums) == false);

    nums = { 1, 2, 3, 4, 5 };
    assert(increasingTriplet(nums) == true);
}```
