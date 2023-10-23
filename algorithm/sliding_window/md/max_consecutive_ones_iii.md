```cpp
// https://leetcode.com/problems/max-consecutive-ones-iii

/*
Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.

Ex1:
Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Ex2:
Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

*/

#include <vector>
#include <cassert>

using namespace std;

int longestOnes(vector<int>& nums, int k) {
    if (nums.empty()) {
        return 0;
    }

    int n = nums.size();
    int l = 0, r = 0;
    int cnt = 0;
    int res = 0;

    while (r < n) {
        if (nums[r] == 1) {
            cnt++;
            r++;
        } else {
            if (k > 0) {
                cnt++;
                k--;
                r++;
            } else {
                if (nums[l] == 0) {
                    k++;
                }
                cnt--;
                l++;
            }
        }

        res = max(res, cnt);
    }

    return res;
}

int main() {
    vector<int> nums1 = {1,1,1,0,0,0,1,1,1,1,0};
    assert(longestOnes(nums1, 2) == 6);

    vector<int> nums2 = {0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1};
    assert(longestOnes(nums2, 3) == 10);
}```
