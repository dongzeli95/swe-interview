```cpp
// Product Of Array Except Self.
// Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

// The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

// You must write an algorithm that runs in O(n) time and without using the division operation.

// Ex1:
// Input: nums = [1,2,3,4]
// Output: [24,12,8,6]

// Ex2:
// Input: nums = [-1,1,0,-3,3]
// Output: [0,0,9,0,0]

// [1, 2, 6, 24]
// [24, 24, 12, 4]

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

// Time complexity: O(n), Space complexity: O(n), Two pass
vector<int> productExceptSelfTwoPassTwoArray(vector<int>& nums) {
    if (nums.empty()) {
        return {};
    }

    int n = nums.size();
    vector<int> left(n, 1);
    vector<int> right (n, 1);

    left[0] = nums[0];
    for (int i = 1; i < n; i++) {
        left[i] = left[i-1]*nums[i];
    }

    right[n-1] = nums[n-1];
    for (int i = n-2; i >= 0; i--) {
        right[i] = right[i+1] * nums[i];
    }

    vector<int> res(n, 1);
    for (int i = 0; i < n; i++) {
        int l = (i-1) >= 0 ? left[i-1] : 1;
        int r = (i+1) < n ? right[i+1] : 1;

        res[i] = l*r;
    }

    return res;
}

// Two pass but using same output array
// Time complexity: O(n), Space complexity: O(1) if we don't count the output array.
vector<int> productExceptSelfTwoPass(vector<int>& nums) {
    int n = nums.size();
    vector<int> res(n, 1);
    int prefix = 1;
    for (int i = 0; i < n; i++) {
        res[i] *= prefix;
        prefix *= nums[i];
    }
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        res[i] *= suffix;
        suffix *= nums[i];
    }
    return res;
}

// One pass
// Time complexity: O(n), Space complexity: O(1) if we don't count the output array.
vector<int> productExceptSelfOnePass(vector<int>& nums) {
    vector<int> res(nums.size(), 1);
    int prefix = 1;
    int suffix = 1;
    int n = nums.size();

    for (int i = 0; i < n; i++) {
        res[i] *= prefix;
        prefix *= nums[i];

        res[n - 1 - i] *= suffix;
        suffix *= nums[n - 1 - i];
    }

    return res;
}


int main() {
    // Test two pass with two arrays
    vector<int> nums = {1,2,3,4};
    vector<int> res = productExceptSelfTwoPassTwoArray(nums);
    vector<int> expected = {24,12,8,6};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }

    nums = {-1,1,0,-3,3};
    res = productExceptSelfTwoPassTwoArray(nums);
    expected = {0,0,9,0,0};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }

    nums = {1,2,3,4};
    res = productExceptSelfTwoPass(nums);
    expected = {24,12,8,6};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }

    nums = {-1,1,0,-3,3};
    res = productExceptSelfTwoPass(nums);
    expected = {0,0,9,0,0};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }

    // Test one pass
    nums = {1, 2, 3, 4};
    res = productExceptSelfOnePass(nums);
    expected = {24, 12, 8, 6};
    for (int i = 0; i < res.size(); i++)
    {
        assert(res[i] == expected[i]);
    }

    nums = {-1, 1, 0, -3, 3};
    res = productExceptSelfOnePass(nums);
    expected = {0, 0, 9, 0, 0};
    for (int i = 0; i < res.size(); i++)
    {
        assert(res[i] == expected[i]);
    }
}```
