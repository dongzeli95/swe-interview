```cpp
// https://leetcode.com/problems/nearest-exit-from-entrance-in-maze

/* 

You are given an m x n matrix maze (0-indexed) with empty cells (represented as '.') and walls (represented as '+'). 
You are also given the entrance of the maze, where entrance = [entrancerow, entrancecol] denotes the row and column of the cell you are initially standing at.
In one step, you can move one cell up, down, left, or right. You cannot step into a cell with a wall, and you cannot step outside the maze. 
Your goal is to find the nearest exit from the entrance. An exit is defined as an empty cell that is at the border of the maze. The entrance does not count as an exit.
Return the number of steps in the shortest path from the entrance to the nearest exit, or -1 if no such path exists.

Ex1:

Input: maze = [['+','+','.','+'],['.','.','.','+'],['+','+','+','.']], entrance = [1,2]
Output: 1
Explanation: There are 3 exits in this maze at [1,0], [0,2], and [2,3].
Initially, you are at the entrance cell [1,2].
- You can reach [1,0] by moving 2 steps left.
- You can reach [0,2] by moving 1 step up.
It is impossible to reach [2,3] from the entrance.
Thus, the nearest exit is [0,2], which is 1 step away.

Ex2:
Input: maze = [['+','+','+'],['.','.','.'],['+','+','+']], entrance = [1,0]
Output: 2
Explanation: There is 1 exit in this maze at [1,2].
[1,0] does not count as an exit since it is the entrance cell.
Initially, you are at the entrance cell [1,0].
- You can reach [1,2] by moving 2 steps right.
Thus, the nearest exit is [1,2], which is 2 steps away.

Ex3:
Input: maze = [['.','+']], entrance = [0,0]
Output: -1
Explanation: There are no exits in this maze.

Ex4:
[['+','.','+','+','+','+','+'],['+','.','+','.','.','.','+'],['+','.','+','.','+','.','+'],['+','.','.','.','+','.','+'],['+','+','+','+','+','.','+']]
entrance = [0, 1]
Output: 12

*/

#include <vector>
#include <queue>
#include <iostream>

using namespace std;

bool isBorder(pair<int, int> pos, int m, int n) {
    return pos.first == 0 || pos.first == m - 1 || pos.second == 0 || pos.second == n - 1;
}

// Time: O(m*n), Space: O(m*n)
int nearestExit(vector<vector<char>>& maze, vector<int>& entrance) {
    if (maze.empty() || maze[0].empty()) {
        return -1;
    }

    int m = maze.size();
    int n = maze[0].size();

    vector<int> neighbors {-1, 0, 1, 0, -1};
    queue<pair<int, int>> q;
    q.push({entrance[0], entrance[1]});
    // Don't forget to mark the entrance as visited
    maze[entrance[0]][entrance[1]] = '+';

    int res = 0;
    while (!q.empty()) {
        int s = q.size();

        for (int i = 0; i < s; i++) {
            pair<int, int> curr = q.front();
            q.pop();

            if (res > 0 && isBorder(curr, m, n)) {
                return res;
            }

            int x = curr.first;
            int y = curr.second;
            for (int i = 0; i < 4; i++) {
                int nx = x + neighbors[i];
                int ny = y + neighbors[i+1];
                if (nx < 0 || ny < 0 || nx >= m || ny >= n || maze[nx][ny] == '+') {
                    continue;
                }

                maze[nx][ny] = '+';
                q.push({nx, ny});
            }
        }
        res++;
    }

    return -1;
}

int main() {
    vector<vector<char>> maze1 {{'+','+','.','+'},{'.','.','.','+'},{'+','+','+','.'}};
    vector<int> entrance = {1, 2};
    int res = nearestExit(maze1, entrance);
    assert(res == 1);

    vector<vector<char>> maze2 {{'+','+','+'},{'.','.','.'},{'+','+','+'}};
    entrance = {1, 0};
    res = nearestExit(maze2, entrance);
    assert(res == 2);

    vector<vector<char>> maze3 {{'.','+'}};
    entrance = {0, 0};
    res = nearestExit(maze3, entrance);
    assert(res == -1);

    vector<vector<char>> maze4{{'+','.','+','+','+','+','+'}, 
                                {'+','.','+','.','.','.','+'},
                                {'+','.','+','.','+','.','+'},
                                {'+','.','.','.','+','.','+'},
                                {'+','+','+','+','+','.','+'}};
    entrance = {0, 1};
    res = nearestExit(maze4, entrance);
    assert(res == 12);
}```
