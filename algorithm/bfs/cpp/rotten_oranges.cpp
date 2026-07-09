// https://leetcode.com/problems/rotting-oranges

/*
You are given an m x n grid where each cell can have one of three values:

0 representing an empty cell,
1 representing a fresh orange, or
2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

Ex1:
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4

Ex2:
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Ex3:
Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.

*/

#include <vector>
#include <queue>
#include <iostream>

using namespace std;

// Time: O(m*n), Space: O(m*n)
int orangesRotting(vector<vector<int>>& grid) {
    if (grid.empty()) {
        return 0;
    }

    int m = grid.size();
    int n = grid[0].size();

    vector<int> neighbors {-1, 0, 1, 0, -1};

    queue<pair<int, int>> q;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 2) {
                q.push({i, j});
            }
        }
    }

    int res = 0;
    while (!q.empty()) {
        int s = q.size();
        for (int i = 0; i < s; i++) {
            pair<int, int> curr = q.front();
            q.pop();

            int x = curr.first;
            int y = curr.second;

            for (int j = 0; j < 4; j++) {
                int nx = x + neighbors[j];
                int ny = y + neighbors[j+1];
                if (nx < 0 || ny < 0 || nx >= m || ny >= n || grid[nx][ny] == 0 || grid[nx][ny] == 2) {
                    continue;
                }

                grid[nx][ny] = 2;
                q.push({nx, ny});
            }
        }

        if (!q.empty()) {
            res++;
        }
    }

    for (auto row : grid) {
        for (auto cell : row) {
            if (cell == 1) {
                return -1;
            }
        }
    }

    return res;
}

int main() {
    vector<vector<int>> grid = {{2,1,1},{1,1,0},{0,1,1}};
    assert(orangesRotting(grid) == 4);

    grid = {{2,1,1},{0,1,1},{1,0,1}};
    assert(orangesRotting(grid) == -1);

    grid = {{0,2}};
    assert(orangesRotting(grid) == 0);
    return 0;
}