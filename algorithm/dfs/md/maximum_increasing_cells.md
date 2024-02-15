```cpp
// https://leetcode.com/problems/maximum-strictly-increasing-cells-in-a-matrix/

/*

Given a 1 - indexed m x n integer matrix mat, you can select any cell in the matrix as your starting cell.
From the starting cell, you can move to any other cell in the same row or column, but only if the value of the destination cell is strictly greater than the value of the current cell.
You can repeat this process as many times as possible, moving from cell to cell until you can no longer make any moves.
Your task is to find the maximum number of cells that you can visit in the matrix by starting from some cell.
Return an integer denoting the maximum number of cells that can be visited.

Ex1:
Input: mat = [[3, 1], [3, 4]]
Output : 2
Explanation : The image shows how we can visit 2 cells starting from row 1, column 2. It can be shown that we cannot visit more than 2 cells no matter where we start from, so the answer is 2.

Ex2:
Input : mat = [[1, 1], [1, 1]]
Output : 1
Explanation : Since the cells must be strictly increasing, we can only visit one cell in this example.

Ex3:
Input : mat = [[3, 1, 6], [-9, 5, 7]]
Output : 4
Explanation : The image above shows how we can visit 4 cells starting from row 2, column 1. It can be shown that we cannot visit more than 4 cells no matter where we start from, so the answer is 4.

*/

#include <vector>
#include <string>
#include <iostream>

using namespace std;


bool cmp(const vector<int>& v1, const vector<int>& v2) {
    return v1[2] < v2[2];
};

class Solution {
public:
    string getKey(int x, int y) {
        return to_string(x) + "#" + to_string(y);
    }

    int dfs(unordered_map<string, vector<vector<int>>>& graph,
        vector<vector<int>>& mat,
        int x, int y,
        unordered_map<string, int>& cache,
        vector<vector<bool>>& visited) {
        string k = getKey(x, y);
        if (cache.count(k)) {
            return cache[k];
        }

        int res = 1;

        string rowK = "r" + to_string(x);
        string colK = "c" + to_string(y);

        // cout << "x: " << x << ", y: " << y << endl;
        auto pos = upper_bound(graph[rowK].begin(), graph[rowK].end(), vector<int>{x, y, mat[x][y]}, cmp);
        int iPos = pos - graph[rowK].begin();
        for (int i = iPos; i < graph[rowK].size(); i++) {
            int tempX = graph[rowK][i][0];
            int tempY = graph[rowK][i][1];
            int v = graph[rowK][i][2];
            if (v <= mat[x][y] || visited[tempX][tempY]) continue;
            // cout << rowK << " " << "x: " << tempX << " y: " << tempY << " v: " << v << endl; 
            visited[tempX][tempY] = true;
            int cells = dfs(graph, mat, tempX, tempY, cache, visited);
            visited[tempX][tempY] = false;
            res = max(res, 1 + cells);
        }

        auto pos2 = upper_bound(graph[colK].begin(), graph[colK].end(), vector<int>{x, y, mat[x][y]}, cmp);
        iPos = pos2 - graph[colK].begin();
        for (int i = iPos; i < graph[colK].size(); i++) {
            int tempX = graph[colK][i][0];
            int tempY = graph[colK][i][1];
            int v = graph[colK][i][2];
            if (v <= mat[x][y] || visited[tempX][tempY]) continue;
            // cout << colK << " " << "x: " << tempX << " y: " << tempY << " v: " << v << endl; 
            visited[tempX][tempY] = true;
            int cells = dfs(graph, mat, tempX, tempY, cache, visited);
            visited[tempX][tempY] = false;
            res = max(res, 1 + cells);
        }

        cache[k] = res;
        return res;
    }
    int maxIncreasingCells(vector<vector<int>>& mat) {
        unordered_map<string, int> cache;
        int m = mat.size(), n = mat[0].size();
        vector<vector<bool>> visited(m, vector<bool>(n, false));
        unordered_map<string, vector<vector<int>>> graph;

        auto cmp = [](vector<int>& v1, vector<int>& v2) {
            return v1[2] < v2[2];
            };

        for (int i = 0; i < m; i++) {
            vector<vector<int>> row;
            for (int j = 0; j < n; j++) {
                row.push_back({ i, j, mat[i][j] });
            }
            sort(row.begin(), row.end(), cmp);
            string k = "r" + to_string(i);
            graph[k] = row;
        }

        for (int j = 0; j < n; j++) {
            vector<vector<int>> col;
            for (int i = 0; i < m; i++) {
                col.push_back({ i, j, mat[i][j] });
            }
            sort(col.begin(), col.end(), cmp);
            string k = "c" + to_string(j);
            graph[k] = col;
        }

        // cout << "about to dfs 1" << endl;

        int res = 1;
        for (int i = 0; i < m; i++) {
            string k = "r" + to_string(i);
            vector<vector<int>> row = graph[k];
            int x = row[0][0];
            int y = row[0][1];
            int v = row[0][2];
            visited[x][y] = true;
            res = max(res, dfs(graph, mat, x, y, cache, visited));
            visited[x][y] = false;
        }

        // cout << "about to dfs 2" << endl;

        for (int j = 0; j < n; j++) {
            string k = "c" + to_string(j);
            vector<vector<int>> col = graph[k];
            int x = col[0][0];
            int y = col[0][1];
            int v = col[0][2];
            visited[x][y] = true;
            res = max(res, dfs(graph, mat, x, y, cache, visited));
            visited[x][y] = false;
        }

        return res;
    }

    void debug(vector<vector<int>>& row) {
        cout << "row" << endl;
        for (int i = 0; i < row.size(); i++) {
            cout << "x: " << row[i][0] << " y: " << row[i][1] << " v: " << row[i][2] << endl;
        }
    }
};```
