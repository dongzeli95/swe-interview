// https://leetcode.com/problems/delete-and-earn/
/*
You are given an integer array nums. 
You want to maximize the number of points you get by performing the following operation any number of times:
Pick any nums[i] and delete it to earn nums[i] points. 
Afterwards, you must delete every element equal to nums[i] - 1 and every element equal to nums[i] + 1.
Return the maximum number of points you can earn by applying the above operation some number of times.

Ex1:
Input: nums = [3,4,2]
Output: 6
Explanation: You can perform the following operations:
- Delete 4 to earn 4 points. Consequently, 3 is also deleted. nums = [2].
- Delete 2 to earn 2 points. nums = [].
You earn a total of 6 points.

Ex2:
Input: nums = [2,2,3,3,3,4]
Output: 9
Explanation: You can perform the following operations:
- Delete a 3 to earn 3 points. All 2's and 4's are also deleted. nums = [3,3].
- Delete a 3 again to earn 3 points. nums = [3].
- Delete a 3 once more to earn 3 points. nums = [].
You earn a total of 9 points.

*/

#include <unordered_map>
#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

int dfs(unordered_map<int, pair<int, int>>& m, string key, unordered_map<string, int>& cache) {
    if (cache.count(key)) {
        return cache[key];
    }

    int sum = 0;
    for (auto i : m) {
        int num = i.first;
        int s = i.second.first;
        int idx = i.second.second;
        if (s == 0) {
            continue;
        }

        int plusOne = m[num+1].first;
        int minusOne = m[num-1].first;
        m[num].first = 0;
        m[num+1].first = 0;
        m[num-1].first = 0;
        char c = key[idx];
        key[idx] = '#';
        sum = max(sum, s + dfs(m, key, cache));
        m[num+1].first = plusOne;
        m[num-1].first = minusOne;
        m[num].first = s;
        key[idx] = c;
    }

    cache[key] = sum;
    return sum;
}

int deleteAndEarn1(vector<int>& nums) {
    unordered_map<int, pair<int, int>> m;
    unordered_map<string, int> cache;
    int n = nums.size();

    string key = "";
    for (int i = 0; i < n; i++) {
        if (!m.count(nums[i])) {
            m[nums[i]].second = key.size();
            key += to_string(nums[i]);
        }
        m[nums[i]].first += nums[i];
    }

    return dfs(m, key, cache);
}

// Time: O(n + mx), Space: O(n + mx)
int topDownDP(int num, unordered_map<int, int>& cache,
                        unordered_map<int, int>& m) {
    if (num == 0) {
        return num;
    }

    if (num == 1) {
        return m[1];
    }

    if (cache.count(num)) {
        return cache[num];
    }

    int res = max(m[num] + topDownDP(num-2, cache, m), 
            topDownDP(num-1, cache, m));
    cache[num] = res;
    return res;
}

int deleteAndEarn(vector<int>& nums) {
    int n = nums.size();
    int mx = 0;
    unordered_map<int, int> m;
    for (int i = 0; i < n; i++) {
        mx = max(nums[i], mx);
        m[nums[i]] += nums[i];
    }

    unordered_map<int, int> cache;
    return topDownDP(mx, cache, m);
}

int main() {
    vector<int> nums = {3,4,2};
    assert(deleteAndEarn(nums) == 6);

    nums = {2,2,3,3,3,4};
    assert(deleteAndEarn(nums) == 9);

    return 0;
}