```cpp
// https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element

/*
Given a binary array nums, you should delete one element from it.
Return the size of the longest non-empty subarray containing only 1's in the resulting array. 
Return 0 if there is no such subarray.

Ex1:
Input: nums = [1,1,0,1]
Output: 3
Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.

Ex2:
Input: nums = [0,1,1,1,0,1,1,0,1]
Output: 5
Explanation: After deleting the number in position 4, [0,1,1,1,1,1,0,1] longest subarray with value of 1's is [1,1,1,1,1].

Ex3:
Input: nums = [1,1,1]
Output: 2
Explanation: You must delete one element.

*/

#include <vector>
#include <cassert>

using namespace std;

// Time complexity: O(N), Space complexity: O(1)
int longestSubarray(vector<int>& nums) {
    if (nums.empty()) {
        return 0;
    }

    int res = 0;
    int l = 0, r = 0;
    int n = nums.size();
    bool deleted = false;

    while (r < n) {
        if (nums[r] == 1) {
            r++;
        } else {
            if (deleted) {
                if (nums[l] == 0) {
                    deleted = false;
                }
                l++;
            } else {
                deleted = true;
                r++;
            }
        }

        res = max(res, r-l-1); // -1 is for the deleted element
    }

    return res;
}

int main() {
    vector<int> nums1 = {1,1,0,1};
    assert(longestSubarray(nums1) == 3);

    vector<int> nums2 = {0,1,1,1,0,1,1,0,1};
    assert(longestSubarray(nums2) == 5);

    vector<int> nums3 = {1,1,1};
    assert(longestSubarray(nums3) == 2);

    return 0;
}```
