```cpp
#include <vector>
#include <iostream>
#include <cassert>
#include <set>

using namespace std;

// https://leetcode.com/problems/combination-sum-ii/
// Given a collection of candidate numbers(candidates) and a target number(target), 
// find all unique combinations in candidates where the candidate numbers sum to target.
// Each number in candidates may only be used once in the combination.
// Note: The solution set must not contain duplicate combinations.

/*
Ex1:
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output:
[
    [1,1,6],
    [1,2,5],
    [1,7],
    [2,6]
]

Ex2:
1, 2, 2, 2
Input: candidates = [2,5,2,1,2], target = 5
Output:
[
    [1,2,2],
    [5]
]
*/

void dfs2(vector<int>& candidates, 
            int idx, 
            vector<int>& curr,
            int& sum, const int& target, vector<vector<int>>& res) {
    if (sum == target) {
        res.push_back(curr);
        return;
    }

    int n = candidates.size();
    if (idx >= n || sum > target) return;

    for (int i = idx; i < n; i++) {
        // This optimization prevents using set
        if (i > idx && candidates[i] == candidates[i - 1]) continue;
        curr.push_back(candidates[i]);
        sum += candidates[i];
        dfs2(candidates, i+1, curr, sum, target, res);
        sum -= candidates[i];
        curr.pop_back();
    }
}

vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
    // sort to dedup duplicates caused by order.
    sort(candidates.begin(), candidates.end());
    vector<vector<int>> res;
    vector<int> curr;
    int sum = 0;
    set<vector<int>> s;
    dfs2(candidates, 0, curr, sum, target, res);
    return res;
}


// https://leetcode.com/problems/combination-sum-iii

/*
Find all valid combinations of k numbers that sum up to n such that the following conditions are true:

Only numbers 1 through 9 are used.
Each number is used at most once.
Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.

Ex1:
Input: k = 3, n = 7
Output: [[1,2,4]]
Explanation:
1 + 2 + 4 = 7
There are no other valid combinations.

Ex2:
Input: k = 3, n = 9
Output: [[1,2,6],[1,3,5],[2,3,4]]
Explanation:
1 + 2 + 6 = 9
1 + 3 + 5 = 9
2 + 3 + 4 = 9
There are no other valid combinations.

Ex3:
Input: k = 4, n = 1
Output: []
Explanation: There are no valid combinations.
Using 4 different numbers in the range [1,9], the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1, there are no valid combination.
*/

// Time: 
// Upperbound: O(9^k)
// For each exploration path: O(9×8×7×...×(10−k)) = 9!/(9−k)! 
// Overall: O( k * 9!/(9−k)!)
//
// Space: O(k)

void dfs(int k, int n, vector<int>& curr, vector<vector<int>>& res, int idx) {
    if (k == 0 && n == 0) {
        res.push_back(curr);
        return;
    }

    for (int i = idx; i <= 9; i++) {
        if (i > n) {
            break;
        }

        curr.push_back(i);
        dfs(k - 1, n - i, curr, res, i + 1);
        curr.pop_back();
    }
}

vector<vector<int>> combinationSum3(int k, int n) {
    if (k == 0 || n == 0) {
        return {};
    }

    vector<vector<int>> res;
    vector<int> curr;
    dfs(k, n, curr, res, 1);

    return res;
}

int main() {
    // vector<vector<int>> res1 = {{1,2,4}};
    // vector<vector<int>> comb1 = combinationSum3(3, 7);
    // assert(comb1 == res1);

    // vector<vector<int>> res2 = {{1,2,6},{1,3,5},{2,3,4}};
    // assert(combinationSum3(3, 9) == res2);

    // vector<vector<int>> res3 = {};
    // assert(combinationSum3(4, 1) == res3);

    vector<int> candidates = {10, 1, 2, 7, 6, 1, 5};
    int target = 8;
    vector<vector<int>> res = combinationSum2(candidates, target);
    for (vector<int> i : res) {
        for (int j = 0; j < i.size(); j++) {
            cout << i[j] << ", ";
        }
        cout << endl;
    }

    return 0;
}```
