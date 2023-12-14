```cpp
// https://leetcode.com/problems/shuffle-an-array/

/*
Given an integer array nums, design an algorithm to randomly shuffle the array. All permutations of the array should be equally likely as a result of the shuffling.

Implement the Solution class:

Solution(int[] nums) Initializes the object with the integer array nums.
int[] reset() Resets the array to its original configuration and returns it.
int[] shuffle() Returns a random shuffling of the array.

Ex1:
Input
["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]
Output
[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

Explanation
Solution solution = new Solution([1, 2, 3]);
solution.shuffle();    // Shuffle the array [1,2,3] and return its result.
                       // Any permutation of [1,2,3] must be equally likely to be returned.
                       // Example: return [3, 1, 2]
solution.reset();      // Resets the array back to its original configuration [1,2,3]. Return [1, 2, 3]
solution.shuffle();    // Returns the random shuffling of array [1,2,3]. Example: return [1, 3, 2]

*/

// [3, ]
#include <vector>

using namespace std;

// Time: O(n), Space: O(n)
// Fisher-Yates algorithm
class Shuffle {
public:
    vector<int> nums;
    Shuffle(vector<int>& nums) : nums(nums) {};

    vector<int> shuffle() {
        vector<int> shuffle = nums;
        int n = shuffle.size();
        for (int i = 0; i < n; i++) {
            int idx = i + rand() % (n-i);
            swap(shuffle[i], shuffle[idx]);
        }

        return shuffle;
    }

    vector<int> reset() {
        return nums;
    }
};```
