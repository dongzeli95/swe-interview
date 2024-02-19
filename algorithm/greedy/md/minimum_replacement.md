```cpp
// https://leetcode.com/problems/minimum-replacements-to-sort-the-array/description/

/*
You are given a 0-indexed integer array nums. In one operation you can replace any element of the array with any two elements that sum to it.

For example, consider nums = [5,6,7]. In one operation, we can replace nums[1] with 2 and 4 and convert nums to [5,2,4,7].
Return the minimum number of operations to make an array that is sorted in non-decreasing order.

Ex1:
Input: nums = [3,9,3]
Output: 2
Explanation: Here are the steps to sort the array in non-decreasing order:
- From [3,9,3], replace the 9 with 3 and 6 so the array becomes [3,3,6,3]
- From [3,3,6,3], replace the 6 with 3 and 3 so the array becomes [3,3,3,3,3]
There are 2 steps to sort the array in non-decreasing order. Therefore, we return 2.

Ex2:
Input: nums = [1,2,3,4,5]
Output: 0
Explanation: The array is already in non-decreasing order. Therefore, we return 0.
*/

// Intuition:
/*
For a specific position number [7 3]
we need to calculate how much is the minimum number we can split a number like 7 such that each number is less or equal to 3.
Obviously if we use 3, it would ended up with minimal number of slots.
But if we use 3, we would use [1, 3, 3] which is not optimal since the minimum is too small, will probably cause more operations for number before it.

The intuition is that for the fixed number of slots we find, which is 3 in this case.
How we can assign the smallest number such that it is as large as possible. We can find is by doing 7 / slots = 2
*/

#include <vector>

using namespace std;

long long minimumReplacement(vector<int>& nums) {
    if (nums.empty()) {
        return 0;
    }

    int n = nums.size();
    long long res = 0;
    for (int i = n - 2; i >= 0; i--) {
        if (nums[i] > nums[i + 1]) {
            int mod = nums[i] % nums[i + 1];
            int num_elements = (nums[i] / nums[i + 1]) + ((mod == 0) ? 0 : 1);
            int smallest = nums[i] / num_elements;
            int operations = num_elements - 1;
            res += operations;
            nums[i] = smallest;
        }
    }

    return res;
}```
