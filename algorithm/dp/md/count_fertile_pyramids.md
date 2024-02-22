```cpp
// https://leetcode.com/problems/count-fertile-pyramids-in-a-land/description/
/*
A farmer has a rectangular grid of land with m rows and n columns that can be divided into unit cells. 
Each cell is either fertile (represented by a 1) or barren (represented by a 0). All cells outside the grid are considered barren.

A pyramidal plot of land can be defined as a set of cells with the following criteria:

The number of cells in the set has to be greater than 1 and all cells must be fertile.
The apex of a pyramid is the topmost cell of the pyramid. The height of a pyramid is the number of rows it covers. 
Let (r, c) be the apex of the pyramid, and its height be h. Then, the plot comprises of cells (i, j) where r <= i <= r + h - 1 and c - (i - r) <= j <= c + (i - r).
An inverse pyramidal plot of land can be defined as a set of cells with similar criteria:

The number of cells in the set has to be greater than 1 and all cells must be fertile.
The apex of an inverse pyramid is the bottommost cell of the inverse pyramid. 
The height of an inverse pyramid is the number of rows it covers. Let (r, c) be the apex of the pyramid, and its height be h. Then, the plot comprises of cells (i, j) where r - h + 1 <= i <= r and c - (r - i) <= j <= c + (r - i).
Some examples of valid and invalid pyramidal (and inverse pyramidal) plots are shown below. Black cells indicate fertile cells.

Given a 0-indexed m x n binary matrix grid representing the farmland, 
return the total number of pyramidal and inverse pyramidal plots that can be found in grid.

Ex1:
Input: grid = [[0,1,1,0],[1,1,1,1]]
Output: 2
Explanation: The 2 possible pyramidal plots are shown in blue and red respectively.
There are no inverse pyramidal plots in this grid.
Hence total number of pyramidal and inverse pyramidal plots is 2 + 0 = 2.

Ex2:
Input: grid = [[1,1,1],[1,1,1]]
Output: 2
Explanation: The pyramidal plot is shown in blue, and the inverse pyramidal plot is shown in red.
Hence the total number of plots is 1 + 1 = 2.

Ex3:
Input: grid = [[1,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[0,1,0,0,1]]
Output: 13
Explanation: There are 7 pyramidal plots, 3 of which are shown in the 2nd and 3rd figures.
There are 6 inverse pyramidal plots, 2 of which are shown in the last figure.
The total number of plots is 7 + 6 = 13.

*/

// The key point here is how to represent a pyramid.For sake of simplicity assume a fertile land as a pyramid of height 1.

// Now, A pyramid of height 2 can be seen as two joint pyramid of height 1 and two extra 1s(the peak and one just below it).

// 0 1 0        0 2 0
// 1 1 1        1 1 1
// Similiarly, A pyramid of height 3 can be seen as two joint pyramid of height 2 and two extra 1s(the peak and one just below it).

// 0 0 1 0 0           0 0 3 0 0
// 0 1 1 1 0           0 2 2 2 0
// 1 1 1 1 1           1 1 1 1 1
// And so on...

// Once this is clear, the rest of the code is simple.We just need to keep the count of all pyramids with height greater than 1. For that just itererate over the grid and check whether the current cell is the tip of pyramid or not.If it is a pyramid, then find its height.This can be done in O(1).

// And we only need to write code for one type of pyramid(inverse).For other type simply reverse all the rows and count again.

// NOTE: The examples above are for Simple Pyramid.But the code below counts for the inverse pyramids as it is easier to write.

#include <vector>

using namespace std;

class Solution {
public:
    // Time: O(m*n), Space: O(m*n)
    int count(vector<vector<int>> grid) {
        int i, j, n = grid.size(), m = grid[0].size(), ans = 0;
        for (i = 1; i < n; i++) {
            for (j = 1; j < m - 1; j++) {
                if (grid[i][j] && grid[i - 1][j]) { // check if current cell can be a tip of pyramid or not.
                    grid[i][j] = min(grid[i - 1][j - 1], grid[i - 1][j + 1]) + 1; // if its a pyramid, find the height.
                    ans += grid[i][j] - 1;
                    // pyramid of size n contributes n - 1 times to the answer.
                }
            }
        }
        return ans;
    }
    int countPyramids(vector<vector<int>>& grid) {
        int ans = count(grid); // this will count inverse pyramid.
        reverse(grid.begin(), grid.end());
        ans += count(grid); // this will count simple pyramid.
        return ans;
    }
};```
