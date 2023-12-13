```cpp
// https://leetcode.com/problems/random-pick-index/

/*
Given an integer array nums with possible duplicates, randomly output the index of a given target number. 
You can assume that the given target number must exist in the array.

Implement the Solution class:

Solution(int[] nums) Initializes the object with the array nums.
int pick(int target) Picks a random index i from nums where nums[i] == target. 
If there are multiple valid i's, then each index should have an equal probability of returning.

Ex1:

Input
["Solution", "pick", "pick", "pick"]
[[[1, 2, 3, 3, 3]], [3], [1], [3]]
Output
[null, 4, 0, 2]

Explanation
Solution solution = new Solution([1, 2, 3, 3, 3]);
solution.pick(3); // It should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
solution.pick(1); // It should return 0. Since in the array only nums[0] is equal to 1.
solution.pick(3); // It should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
*/

#include <vector>
#include <unordered_map>

using namespace std;

class IndexPicker {
public:
    vector<int> nums;
    unordered_map<int, vector<int>> m;
    IndexPicker(vector<int>& nums) : nums(nums) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            if (!m.count(nums[i])) {
                m[nums[i]] = {i};
            } else {
                m[nums[i]].push_back(i);
            }
        }
    }

    int pick(int num) {
        if (!m.count(num)) {
            return -1;
        }

        vector<int> indices = m[num];
        int n = indices.size();
        int idx = rand() % n;
        return indices[idx];
    }

};

// Reservoir Sampling
// Shuffle an array
// Linked List Random Node.
class Solution {
public:

    vector<int> nums;

    Solution(vector<int>& nums) {
        this->nums.swap(nums);
    }

    int pick(int target) {
        int n = nums.size();
        int count = 0;
        int idx = 0;
        for (int i = 0; i < n; ++i) {
            // if nums[i] is equal to target, i is a potential candidate
            // which needs to be chosen uniformly at random
            if (nums[i] == target) {
                // increment the count of total candidates
                // available to be chosen uniformly at random
                count++;
                // we pick the current number with probability 1 / count (reservoir sampling)
                if (rand() % count == 0) {
                    idx = i;
                }
            }
        }
        return idx;
    }
};```
