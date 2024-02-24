// https://leetcode.com/problems/removing-minimum-and-maximum-from-array/description/
/*
You are given a 0-indexed array of distinct integers nums.

There is an element in nums that has the lowest value and an element that has the highest value. 
We call them the minimum and maximum respectively. 
Your goal is to remove both these elements from the array.

A deletion is defined as either removing an element from the front of the array or removing an element from the back of the array.
Return the minimum number of deletions it would take to remove both the minimum and maximum element from the array.

*/

#include <vector>

using namespace std;

// Time: O(n), Space: O(1)
int minimumDeletions(vector<int>& nums) {
    // finding index of minimum amd maximum element
    int idx_max = -1;
    int idx_min = -1;
    int mini = INT_MAX;
    int maxi = INT_MIN;
    int n = nums.size();

    for (int i = 0;i < n;i++) {
        if (nums[i] < mini) {
            mini = nums[i];
            idx_min = i;
        }

        if (nums[i] > maxi) {
            maxi = nums[i];
            idx_max = i;
        }
    }

    // Three posibilties of answer
    int num1 = max(idx_min + 1, idx_max + 1);// from front deletion only
    int num2 = max(n - idx_min, n - idx_max);// from back deletion only
    int num3 = min(idx_min + 1, idx_max + 1) + min(n - idx_min, n - idx_max);  // from front and back deletion both

    //minimum of all three possibilties
    return min(min(num1, num2), num3);
}