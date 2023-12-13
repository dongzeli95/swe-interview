```cpp
// https://leetcode.com/problems/find-peak-element

/*
A peak element is an element that is strictly greater than its neighbors.
Given a 0-indexed integer array nums, find a peak element, and return its index. 
If the array contains multiple peaks, return the index to any of the peaks.
You may imagine that nums[-1] = nums[n] = -∞. 
In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
You must write an algorithm that runs in O(log n) time.

Ex1:
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.

Ex2:
Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.

*/

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(logn), Space: O(1)
int findPeakElement(vector<int>& nums) {
    if (nums.empty()) {
        return -1;
    }

    if (nums.size() == 1) {
        return 0;
    }

    int n = nums.size();
    int l = 0;
    int r = n-1;

    if (nums[l] > nums[l+1]) {
        return l;
    }

    if (nums[r] > nums[r-1]) {
        return r;
    }

    while (l <= r) {
        int m = l + (r-l) / 2;
        // We find a peak.
        bool greaterThanLeft = (m-1 < 0 || nums[m] > nums[m-1]);
        bool greaterThanRight = (m+1 >= n || nums[m] > nums[m+1]);
        if (greaterThanLeft && greaterThanRight) {
            return m;
        } else if (greaterThanLeft) {
            l = m+1;
        } else {
            r = m-1;
        }
    }

    return -1;
}

int findLowElement(vector<int>& nums) {
    if (nums.empty()) {
        return -1;
    }

    if (nums.size() == 1) {
        return 0;
    }

    int n = nums.size();
    int l = 0;
    int r = n - 1;

    if (nums[l] < nums[l + 1]) {
        return l;
    }

    if (nums[r] < nums[r - 1]) {
        return r;
    }

    while (l <= r) {
        int m = l + (r - l) / 2;
        // We find a peak.
        bool lessThanLeft = (m - 1 < 0 || nums[m] < nums[m - 1]);
        bool lessThanRight = (m + 1 >= n || nums[m] < nums[m + 1]);
        if (lessThanLeft && lessThanRight) {
            return m;
        }
        else if (lessThanLeft) {
            l = m + 1;
        }
        else {
            r = m - 1;
        }
    }

    return -1;
}

int main() {
    vector <int> nums = {1,2,3,1};
    int res = findPeakElement(nums);
    assert(res == 2);
    int low = findLowElement(nums);
    cout << "low: " << low << endl;

    nums = {1,2,1,3,5,6,4};
    res = findPeakElement(nums);
    assert(res == 5);
    low = findLowElement(nums);
    cout << "low: " << low << endl;

    // [3,4,3,2,1]
    nums = {3,4,3,2,1};
    res = findPeakElement(nums);
    assert(res == 1);
    low = findLowElement(nums);
    cout << "low: " << low << endl;

    nums = {5, 4, 3, 4};
    low = findLowElement(nums);
    cout << "low: " << low << endl;
}```
