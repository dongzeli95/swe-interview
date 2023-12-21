```cpp
// https://leetcode.com/problems/rearrange-array-elements-by-sign/
/*
You are given a 0-indexed integer array nums of even length consisting of an equal number of positive and negative integers.

You should rearrange the elements of nums such that the modified array follows the given conditions:

Every consecutive pair of integers have opposite signs.
For all integers with the same sign, the order in which they were present in nums is preserved.
The rearranged array begins with a positive integer.
Return the modified array after rearranging the elements to satisfy the aforementioned conditions.

Ex1:
Input: nums = [3,1,-2,-5,2,-4]
Output: [3,-2,1,-5,2,-4]
Explanation:
The positive integers in nums are [3,1,2]. The negative integers are [-2,-5,-4].
The only possible way to rearrange them such that they satisfy all conditions is [3,-2,1,-5,2,-4].
Other ways such as [1,-2,2,-5,3,-4], [3,1,2,-2,-5,-4], [-2,3,-5,1,-4,2] are incorrect because they do not satisfy one or more conditions.

Ex2:
Input: nums = [-1,1]
Output: [1,-1]
Explanation:
1 is the only positive integer and -1 the only negative integer in nums.
So nums is rearranged to [1,-1].

*/

#include <vector>
#include <iostream>

using namespace std;

// Time: O(n), Space: O(n)
vector<int> rearrangeArray(vector<int>& nums) {
    if (nums.empty()) {
        return {};
    }

    vector<int> pos;
    vector<int> negs;
    vector<int> res;

    int n = nums.size();
    for (int i = 0; i < n; i++) {
        if (nums[i] > 0) pos.push_back(nums[i]);
        else negs.push_back(nums[i]);
    }

    int i1 = 0, i2 = 0;
    for (int i = 0; i < n; i++) {
        res.push_back((i % 2 == 0) ? pos[i1++] : negs[i2++]);
    }

    return res;
}

int main() {
    vector<int> nums {3, 1, -2, -5, 2, -4};
    // vector<int> res = rearrangeArray(nums);
    // for (int i = 0; i < res.size(); i++) {
    //     cout << res[i] << " ";
    // }
    // cout << endl;

    vector<int> nums2{ 28,-41,22,-8,-37,46,35,-9,18,-6,19,-26,-37,-10,-9,15,14,31 };
    vector<int> res2 = rearrangeArray(nums2);
    for (int i = 0; i < res2.size(); i++) {
        cout << res2[i] << " ";
    }
    cout << endl;

    return 0;
}```
