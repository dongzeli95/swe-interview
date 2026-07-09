// https://leetcode.com/problems/next-permutation/

/*
A permutation of an array of integers is an arrangement of its members into a sequence or linear order.

For example, for arr = [1,2,3], the following are all the permutations of arr: [1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1].
The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).

For example, the next permutation of arr = [1,2,3] is [1,3,2].
Similarly, the next permutation of arr = [2,3,1] is [3,1,2].
While the next permutation of arr = [3,2,1] is [1,2,3] because [3,2,1] does not have a lexicographical larger rearrangement.
Given an array of integers nums, find the next permutation of nums.

The replacement must be in place and use only constant extra memory.

Ex1:
Input: nums = [1,2,3]
Output: [1,3,2]

Ex2:
Input: nums = [3,2,1]
Output: [1,2,3]

Ex3:
Input: nums = [1,1,5]
Output: [1,5,1]

*/

// 1 2 3
// 1 3 2
// 2 1 3
// 2 3 1
// 3 1 2
// 3 2 1

#include <vector>
#include <iostream>

using namespace std;


// Intuition: need to find a sequence such that it keeps decreasing to the right side.
// The index before this sequence is the position we want to swap i.
// And then we would want to sort the sequence after i. reversing it is enough.
// Time: O(n), Space: O(1)
void nextPermutation(vector<int>& nums) {
    int n = nums.size(), i = n - 2, j = n - 1;
    while (i >= 0 && nums[i] >= nums[i + 1]) --i;
    if (i >= 0) {
        while (nums[j] <= nums[i]) --j;
        swap(nums[i], nums[j]);
    }
    reverse(nums.begin() + i + 1, nums.end());
}

void print(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        cout << nums[i] << " ";
    }
    cout << endl;
}

int main() {
    vector<int> nums {3, 2, 1};
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);

    nums = {1, 1, 5};
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);
    nextPermutation(nums);
    print(nums);

    return 0;
}