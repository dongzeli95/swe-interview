```cpp
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

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

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
        dfs(k-1, n-i, curr, res, i+1);
        curr.pop_back();
    }
}

// Time: 
// Upperbound: O(9^k)
// For each exploration path: O(9×8×7×...×(10−k)) = 9!/(9−k)! 
// Overall: O( k * 9!/(9−k)!)
//
// Space: O(k)
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
    vector<vector<int>> res1 = {{1,2,4}};
    vector<vector<int>> comb1 = combinationSum3(3, 7);
    assert(comb1 == res1);

    vector<vector<int>> res2 = {{1,2,6},{1,3,5},{2,3,4}};
    assert(combinationSum3(3, 9) == res2);

    vector<vector<int>> res3 = {};
    assert(combinationSum3(4, 1) == res3);

    return 0;
}```
