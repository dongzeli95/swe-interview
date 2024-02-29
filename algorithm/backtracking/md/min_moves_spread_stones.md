```cpp
// https://leetcode.com/problems/minimum-moves-to-spread-stones-over-grid/description/
/*
You are given a 0-indexed 2D integer matrix grid of size 3 * 3, 
representing the number of stones in each cell. 
The grid contains exactly 9 stones, and there can be multiple stones in a single cell.
In one move, you can move a single stone from its current cell to any other cell if the two cells share a side.
Return the minimum number of moves required to place one stone in each cell.

Ex1:
Input: grid = [[1,1,0],
               [1,1,1],
               [1,2,1]]
Output: 3
Explanation: One possible sequence of moves to place one stone in each cell is:
1- Move one stone from cell (2,1) to cell (2,2).
2- Move one stone from cell (2,2) to cell (1,2).
3- Move one stone from cell (1,2) to cell (0,2).
In total, it takes 3 moves to place one stone in each cell of the grid.
It can be shown that 3 is the minimum number of moves required to place one stone in each cell.

Ex2:
Input: grid = [[1,3,0],
               [1,0,0],
               [1,0,3]]
Output: 4
Explanation: One possible sequence of moves to place one stone in each cell is:
1- Move one stone from cell (0,1) to cell (0,2).
2- Move one stone from cell (0,1) to cell (1,1).
3- Move one stone from cell (2,2) to cell (1,2).
4- Move one stone from cell (2,2) to cell (2,1).
In total, it takes 4 moves to place one stone in each cell of the grid.
It can be shown that 4 is the minimum number of moves required to place one stone in each cell.

*/

/*
Intuition: 
Each time we encounter a cell with grid[i][j] == 0 
then we can take 1 from any of the other 8 cells which have a value > 1

Time: O(9!) -> O(N*N)!
if you consider each permutation of the grid as a distinct state and explore transitions between these states. 
This method is akin to treating the problem as a state-space search problem, 
where each state is a unique configuration of the grid, 
and you search for the shortest path from the initial state to the goal state.

Space: (N^2)
The space complexity is O(D), where D is the maximum depth of the recursion
*/

#include <vector>

using namespace std;

int minimumMoves(vector<vector<int>>& grid) {
    // Base Case
    int t = 0;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (grid[i][j] == 0) {
                t++;
            }
        }
    }

    if (t == 0) {
        return 0;
    }

    int ans = INT_MAX;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (grid[i][j] == 0) {
                for (int ni = 0; ni < 3; ++ni) {
                    for (int nj = 0; nj < 3; ++nj) {
                        if (grid[ni][nj] <= 1) continue;
                        int d = abs(ni - i) + abs(nj - j);
                        grid[ni][nj]--;
                        grid[i][j]++;
                        ans = min(ans, d + minimumMoves(grid));
                        grid[ni][nj]++;
                        grid[i][j]--;
                    }
                }
            }
        }
    }
    return ans;
}```
