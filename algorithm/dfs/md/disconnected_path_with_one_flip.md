```cpp
// https://leetcode.com/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/description/

/*
You are given a 0-indexed m x n binary matrix grid. You can move from a cell (row, col) to any of the cells (row + 1, col) or (row, col + 1) that has the value 1. 
The matrix is disconnected if there is no path from (0, 0) to (m - 1, n - 1).
You can flip the value of at most one (possibly none) cell. You cannot flip the cells (0, 0) and (m - 1, n - 1).
Return true if it is possible to make the matrix disconnect or false otherwise.
Note that flipping a cell changes its value from 0 to 1 or from 1 to 0.

Input: grid = [[1,1,1],[1,0,0],[1,1,1]]

111
111
111

Output: true
Explanation: We can change the cell shown in the diagram above. 
There is no path from (0, 0) to (2, 2) in the resulting grid.

Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: false
Explanation: It is not possible to change at most one cell such that there is not path from (0, 0) to (2, 2).

*/

#include <vector>
#include <string>
#include <cassert>
#include <iostream>

using namespace std;

void dfs(vector<vector<int>>& grid, int x, int y, bool &canReachEnd) {
    if (canReachEnd) {
        return;
    }
    int m = grid.size();
    int n = grid[0].size();

    if (x == m-1 && y == n-1) {
        canReachEnd = true;
        return;
    }
    if (x >= m || y >= n || grid[x][y] == 0) return;
    dfs(grid, x + 1, y, canReachEnd);
    if (canReachEnd) {
        grid[x][y] = 0;
        return;
    }

    dfs(grid, x, y + 1, canReachEnd);
    if (canReachEnd) grid[x][y] = 0;
    return;
}

void debug(vector<vector<int>>& grid) {
    int m = grid.size();
    int n = grid[0].size();
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cout << grid[i][j] << " ";
        }
        cout << endl;
    }
}

// Time: O(m+n), Space: O(m+n)
bool isPossibleToCutPath(vector<vector<int>>& grid) {
    bool canReachEnd = false;
    dfs(grid, 0, 0, canReachEnd);
    if (!canReachEnd) return true;

    canReachEnd = false;
    grid[0][0] = 1;
    dfs(grid, 0, 0, canReachEnd);
    return !canReachEnd;
}

// Time: O(m*n), Space: O(m*n)
bool isPossibleToCutPathDP(vector<vector<int>>& grid) {
    int m = grid.size();
    int n = grid[0].size();

    vector<vector<int>> dp(m, vector<int>(n, 0));
    dp[0][0] = 1;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (i == 0 && j == 0) continue;
            if (grid[i][j] == 0) continue;
            int path1 = (i-1 >= 0) ? dp[i-1][j] : 0;
            int path2 = (j-1 >= 0) ? dp[i][j-1] : 0;
            dp[i][j] = path1 + path2;
        }
    }

    vector<vector<int>> dp2(m, vector<int>(n, 0));
    dp2[m-1][n-1] = 1;
    for (int i = m-1; i >= 0; i--) {
        for (int j = n-1; j >= 0; j--) {
            if (i == m-1 && j == n-1) continue;
            if (grid[i][j] == 0) continue;
            int path1 = (i+1 < m) ? dp2[i+1][j] : 0;
            int path2 = (j+1 < n) ? dp2[i][j+1] : 0;
            dp2[i][j] = path1 + path2;
        }
    }


    int target = dp[m-1][n-1];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (i == 0 && j == 0) continue;
            if (i == m-1 && j == n-1) continue;
            if (grid[i][j] == 0) continue;
            // Why? This is the common point that all paths 
            // from start to end must go through.
            // If there is another path that doesn't go through this point,
            // it's not possible since the total target will be different.
            if (dp[i][j]*dp2[i][j] == target) {
                return true;
            }
        }
    }

    return false;
}

int main() {
    vector<vector<int>> grid1 = {{1,1,1},{1,0,0},{1,1,1}};
    assert(isPossibleToCutPath(grid1) == true);
    assert(isPossibleToCutPathDP(grid1) == true);

    vector<vector<int>> grid2 = {{1,1,1},{1,0,1},{1,1,1}};
    assert(isPossibleToCutPath(grid2) == false);
    assert(isPossibleToCutPathDP(grid2) == false);

    return 0;
}```
