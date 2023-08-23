// https://leetcode.com/problems/kth-largest-element-in-an-array

/*
Given an integer array nums and an integer k, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.
Can you solve it without sorting?

Ex1:
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Ex2:
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4

*/

#include <vector>
#include <queue>
#include <cassert>

using namespace std;

// Time complexity: O(N*logK), Space complexity: O(K)
int findKthLargest(vector<int>& nums, int k) {
    if (nums.size() < k) {
        return -1;
    }

    priority_queue<int, vector<int>, greater<int>> min_heap;
    
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        min_heap.push(nums[i]);
        if (min_heap.size() > k) {
            min_heap.pop();
        }
    }

    return min_heap.top();
}

int main() {
    vector<int> nums1 = {3,2,1,5,6,4};
    assert(findKthLargest(nums1, 2) == 5);

    vector<int> nums2 = {3,2,3,1,2,4,5,5,6};
    assert(findKthLargest(nums2, 4) == 4);

    return 0;
}
