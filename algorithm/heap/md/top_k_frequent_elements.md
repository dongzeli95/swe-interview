```cpp
// https://leetcode.com/problems/top-k-frequent-elements/

/*
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

Example 1:
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:
Input: nums = [1], k = 1
Output: [1]

*/

#include <vector>
#include <unordered_map>
#include <iostream>
#include <queue>

using namespace std;

// Time: O(nlogk), Space: O(n)
vector<int> topKFrequent(vector<int>& nums, int k) {
    int n = nums.size();
    unordered_map<int, int> m;
    for (int i = 0; i < n; i++) {
        m[nums[i]]++;
    }

    auto cmp = [&](int a, int b) {
        return m[a] > m[b]; // min heap
    };

    priority_queue<int, vector<int>, decltype(cmp)> pq(cmp);
    for (auto i : m) {
        pq.push(i.first);
        if (pq.size() > k) {
            pq.pop();
        }
    }

    vector<int> res;
    while (!pq.empty()) {
        int num = pq.top();
        pq.pop();
        res.push_back(num);
    }

    return res;
}

int partitionPivot(vector<int>& unique, int left, int right, int pivot_idx, 
                unordered_map<int, int>& m) {
    int idx = left;
    swap(unique[pivot_idx], unique[right]);
    for (int i = left; i < right; i++) {
        if (m[unique[i]] > m[unique[right]]) {
            swap(unique[idx++], unique[i]);
        }
    }
    swap(unique[right], unique[idx]);
    return idx;
}

// Time: O(n), Space: O(n)
vector<int> topKFrequentQuickSelect(vector<int>& nums, int k) {
    if (nums.size() < k) {
        return nums;
    }

    int n = nums.size();
    unordered_map<int, int> m;
    vector<int> unique;
    for (int i = 0; i < n; i++) {
        if (!m.count(nums[i])) {
            unique.push_back(nums[i]);
        }
        m[nums[i]]++;
    }

    int u = unique.size();
    int left = 0, right = u-1;
    while (left <= right) {
        int pivot_idx = left + rand() % (right-left+1);
        int new_pivot = partitionPivot(unique, left, right, pivot_idx, m);
        if (new_pivot == k-1) {
            return vector<int>{unique.begin(), unique.begin()+k};
        } else if (new_pivot > k-1) {
            right = new_pivot-1;
        } else {
            left = new_pivot+1;
        }
    }

    return {};
}

int main() {
    vector<int> nums1 {1, 1, 1, 2, 2, 3};
    vector<int> res = topKFrequentQuickSelect(nums1, 2);
    for (int i : res) {
        cout << i << endl;
    }
    // vector<int> nums2 {1};
    return 0;
}```
