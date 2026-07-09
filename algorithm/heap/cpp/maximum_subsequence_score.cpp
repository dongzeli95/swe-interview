// https://leetcode.com/problems/maximum-subsequence-score

/*
You are given two 0-indexed integer arrays nums1 and nums2 of equal length n and a positive integer k. 
You must choose a subsequence of indices from nums1 of length k.
For chosen indices i0, i1, ..., ik - 1, your score is defined as:

The sum of the selected elements from nums1 multiplied with the minimum of the selected elements from nums2.
It can defined simply as: (nums1[i0] + nums1[i1] +...+ nums1[ik - 1]) * min(nums2[i0] , nums2[i1], ... ,nums2[ik - 1]).
Return the maximum possible score.

A subsequence of indices of an array is a set that can be derived from the set {0, 1, ..., n-1} by deleting some or no elements.

Ex1:
Input: nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3
Output: 12
Explanation:
The four possible subsequence scores are:
- We choose the indices 0, 1, and 2 with score = (1+3+3) * min(2,1,3) = 7.
- We choose the indices 0, 1, and 3 with score = (1+3+2) * min(2,1,4) = 6.
- We choose the indices 0, 2, and 3 with score = (1+3+2) * min(2,3,4) = 12.
- We choose the indices 1, 2, and 3 with score = (3+3+2) * min(1,3,4) = 8.
Therefore, we return the max score, which is 12.

Ex2:
Input: nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1
Output: 30
Explanation:
Choosing index 2 is optimal: nums1[2] * nums2[2] = 3 * 10 = 30 is the maximum possible score.
*/

// (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)

#include <vector>
#include <iostream>
#include <algorithm>
#include <cassert>
#include <queue>

using namespace std;

/*
Intuition: 

We consider all possible combos for nums2 and we realize if we sort nums1 in descending order and loop through it in that order,
we already considered all the possible minimums for nums2.

For the rest of the problem, we just need to figure out what's the maximum combo for nums1 given the current idx of nums2.
We need a priority queue to keep track of the k largest values of nums1, so we need to maintain a min heap to pop the smallest value before index i.

At the end, we just need to return the maximum score.
*/

// Time complexity: O(nlogn), Space complexity: O(n)
long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
    if (nums1.empty()) {
        return 0;
    }

    int n = nums1.size();

    vector<pair<int, int>> combos;
    for (int i = 0; i < n; i++) {
        combos.push_back({nums1[i], nums2[i]});
    }

    sort(combos.begin(), combos.end(), [](pair<int, int>& p1, pair<int, int>& p2) {
        return p1.second > p2.second;
    });

    // store k largest nums1 values
    long long sum = 0;
    int mn = combos[k-1].second;

    // min heap
    priority_queue<int, vector<int>, greater<int>> q;
    for (int i = 0; i < k; i++) {
        q.push(combos[i].first);
        sum += combos[i].first;
    }

    long long res = sum * mn;
    for (int i = k; i < n; i++) {
        mn = combos[i].second;
        sum += combos[i].first;
        q.push(combos[i].first);

        int val = q.top();
        q.pop();
        sum -= val;

        res = max(res, sum * mn);
    }

    return res;
}

int main() {
    vector<int> nums1 = {1,3,3,2};
    vector<int> nums2 = {2,1,3,4};
    int k = 3;
    assert(maxScore(nums1, nums2, k) == 12);

    nums1 = {4,2,3,1,1};
    nums2 = {7,5,10,9,6};
    k = 1;
    assert(maxScore(nums1, nums2, k) == 30);

    return 0;
}