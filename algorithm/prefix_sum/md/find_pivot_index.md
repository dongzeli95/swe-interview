```cpp
// https://leetcode.com/problems/find-pivot-index

/*
Given an array of integers nums, calculate the pivot index of this array.
The pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right.
If the index is on the left edge of the array, then the left sum is 0 because there are no elements to the left. This also applies to the right edge of the array.
Return the leftmost pivot index. If no such index exists, return -1.

Ex1:
Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
The pivot index is 3.
Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
Right sum = nums[4] + nums[5] = 5 + 6 = 11

Ex2:
Input: nums = [1,2,3]
Output: -1
Explanation:
There is no index that satisfies the conditions in the problem statement.

Ex3:
Input: nums = [2,1,-1]
Output: 0
Explanation:
The pivot index is 0.
Left sum = 0 (no elements to the left of index 0)
Right sum = nums[1] + nums[2] = 1 + -1 = 0

*/

#include <vector>
#include <cassert>
#include <iostream>

using namespace std;

// Time: O(n), Space: O(1)
int pivotIndex(vector<int>& nums) {
    if (nums.empty()) {
        return -1;
    }

    int res = -1;
    int n = nums.size();
    int total = 0;
    int sum = 0;

    for (int i = 0; i < n; i++) {
        total += nums[i];
    }

    for (int i = 0; i < n; i++) {
        if (total-nums[i] == sum*2) {
            res = i;
            break;
        }
        sum += nums[i];
    }

    return res;
}

int main() {
    vector<int> nums1 = {1,7,3,6,5,6};
    assert(pivotIndex(nums1) == 3);

    vector<int> nums2 = {1,2,3};
    assert(pivotIndex(nums2) == -1);

    vector<int> nums3 = {2,1,-1};
    assert(pivotIndex(nums3) == 0);

    return 0;
}```
