```cpp
// https://leetcode.com/problems/longest-increasing-subsequence-ii/

/*
You are given an integer array nums and an integer k.

Find the longest subsequence of nums that meets the following requirements:

The subsequence is strictly increasing and
The difference between adjacent elements in the subsequence is at most k.
Return the length of the longest subsequence that meets the requirements.

A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

Ex1:
Input: nums = [4,2,1,4,3,4,5,8,15], k = 3
Output: 5
Explanation:
The longest subsequence that meets the requirements is [1,3,4,5,8].
The subsequence has a length of 5, so we return 5.
Note that the subsequence [1,3,4,5,8,15] does not meet the requirements because 15 - 8 = 7 is larger than 3.

Ex2:
Input: nums = [7,4,5,1,8,12,4,7], k = 5
Output: 4
Explanation:
The longest subsequence that meets the requirements is [4,5,8,12].
The subsequence has a length of 4, so we return 4.

Ex3:
Input: nums = [1,5], k = 1
Output: 1
Explanation:
The longest subsequence that meets the requirements is [1].
The subsequence has a length of 1, so we return 1.

*/

#include <vector>
#include <algorithm>
#include <iostream>
#include <cassert>

using namespace std;

int lengthOfLIS(vector<int>& nums, int k) {
    if (nums.empty()) {
        return 0;
    }

    int res = 1;
    int n = nums.size();
    vector<int> dp(n, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[i]-nums[j] <= k && nums[j] < nums[i]) {
                dp[i] = max(dp[i], 1+dp[j]);
            }
        }
        res = max(res, dp[i]);
    }

    return res;
}

// Using segmentation tree.
// The idea is to keep track of length of subsequence ending in number i in the segment tree.
// Time: O(nlogm), Space: O(m)
class SegmentTree{
public:
    vector<int> segTree;
    int n;
    SegmentTree(int n_) : n(n_) {
        int size = (int)(ceil(log2(n)));
        size = (2 * pow(2, size)) - 1;
        segTree = vector<int>(size);
    }

    int max_value() { return segTree[0]; }

    void update(int i, int val) {
        // For the end range, we should use n-1, instead of the size of entire seg tree!!
        update_util(0, 0, n - 1, i, val);
    }
    // Update the latest longest length for subsequence for ranges.
    void update_util(int idx, int start, int end, int pos, int val) {
        if (start == end) {
            segTree[idx] = max(val, segTree[idx]);
            return;
        }

        int mid = (start + end) / 2;
        if (pos <= mid) {
            update_util(2 * idx + 1, start, mid, pos, val);
        }
        else {
            update_util(2 * idx + 2, mid + 1, end, pos, val);
        }
        segTree[idx] = max(segTree[2 * idx + 1], segTree[2 * idx + 2]);
    }

    int query(int l, int r) { return query_util(0, 0, n - 1, l, r); }

    int query_util(int idx, int start, int end, int l, int r) {
        if (r < start || end < l) return INT_MIN;
        if (l <= start && end <= r) {
            return segTree[idx];
        }

        int mid = (start + end) / 2;
        return max(query_util(2 * idx + 1, start, mid, l, r),
            query_util(2 * idx + 2, mid + 1, end, l, r));
    }
};

int lengthOfLISSeg(vector<int>& nums, int k) {
    SegmentTree seg(1e5 + 1);
    for (int i : nums) {
        int lower = max(0, i - k);
        int q = seg.query(lower, i - 1);
        int cur = 1 + q;
        seg.update(i, cur);
    }

    return seg.max_value();
}

int main() {
    vector<int> nums1{ 4,2,1,4,3,4,5,8,15 };
    int k1 = 3;
    assert(lengthOfLIS(nums1, k1) == 5);
    assert(lengthOfLISSeg(nums1, k1) == 5);

    vector<int> nums2 {7,4,5,1,8,12,4,7};
    int k2 = 5;
    assert(lengthOfLIS(nums2, k2) == 4);
    assert(lengthOfLISSeg(nums2, k2) == 4);

    vector<int> nums3 {1,5};
    int k3 = 1;
    assert(lengthOfLIS(nums3, k3) == 1);
    assert(lengthOfLISSeg(nums3, k3) == 1);

    return 0;
}```
