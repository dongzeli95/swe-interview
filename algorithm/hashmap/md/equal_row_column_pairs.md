```cpp
// https://leetcode.com/problems/equal-row-and-column-pairs

/*

Given a 0-indexed n x n integer matrix grid, return the number of pairs (ri, cj) such that row ri and column cj are equal.
A row and column pair is considered equal if they contain the same elements in the same order (i.e., an equal array).

Input: grid = [[3,2,1],[1,7,6],[2,7,7]]
Output: 1
Explanation: There is 1 equal row and column pair:
- (Row 2, Column 1): [2,7,7]

Ex1:
Input: grid = [[3,2,1],[1,7,6],[2,7,7]]
Output: 1
Explanation: There is 1 equal row and column pair:
- (Row 2, Column 1): [2,7,7]

Ex2:
Input: grid = [[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]
Output: 3
Explanation: There are 3 equal row and column pairs:
- (Row 0, Column 0): [3,1,2,2]
- (Row 2, Column 2): [2,4,2,2]
- (Row 3, Column 2): [2,4,2,2]

*/

#include <cassert>
#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

// Time: O(n^2), Space: O(n^2)
int equalPairs(vector<vector<int>>& grid) {
    if (grid.empty() || grid[0].empty()) {
        return 0;
    }

    int n = grid.size();

    int res = 0;

    unordered_map<string, string> m;
    for (int i = 0; i < n; i++) {
        string rk = "row" + to_string(i);
        string ck = "col" + to_string(i);
        for (int j = 0; j < n; j++) {
            if (!m.count(rk)) {
                m[rk] = to_string(grid[i][j]);
            } else {
                m[rk].push_back(grid[i][j] + '0');
            }

            if (!m.count(ck)) {
                m[ck] = to_string(grid[j][i]);
            }
            else {
                m[ck].push_back(grid[j][i] + '0');
            }
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            string rk = "row" + to_string(i);
            string ck = "col" + to_string(j);
            if (m[rk] == m[ck]) res++;
        }
    }

    return res;
}

int main() {
    vector<vector<int>> grid1 = {{3,2,1},{1,7,6},{2,7,7}};
    assert(equalPairs(grid1) == 1);

    vector<vector<int>> grid2 = {{3,1,2,2},{1,4,4,5},{2,4,2,2},{2,4,2,2}};
    assert(equalPairs(grid2) == 3);

    return 0;
}```
