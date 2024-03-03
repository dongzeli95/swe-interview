// https://leetcode.com/problems/walls-and-gates/description/

/*
You are given an m x n grid rooms initialized with these three possible values.

-1 A wall or an obstacle.
0 A gate.
INF Infinity means an empty room. 

We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the distance to a gate is less than 2147483647.
Fill each empty room with the distance to its nearest gate. 
If it is impossible to reach a gate, it should be filled with INF.

Ex1:
Input: rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
Output: [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]

Ex2:
Input: rooms = [[-1]]
Output: [[-1]]

*/

#include <vector>

using namespace std;

// Time: (m*n), Space: O(m*n)
void wallsAndGates(vector<vector<int>>& rooms) {
    for (int i = 0; i < rooms.size(); ++i) {
        for (int j = 0; j < rooms[i].size(); ++j) {
            if (rooms[i][j] == 0) dfs(rooms, i, j, 0);
        }
    }
}
void dfs(vector<vector<int>>& rooms, int i, int j, int val) {
    if (i < 0 || i >= rooms.size() || j < 0 || j >= rooms[i].size() || rooms[i][j] < val) return;
    rooms[i][j] = val;
    dfs(rooms, i + 1, j, val + 1);
    dfs(rooms, i - 1, j, val + 1);
    dfs(rooms, i, j + 1, val + 1);
    dfs(rooms, i, j - 1, val + 1);
}