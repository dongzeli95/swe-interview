```cpp
// https://leetcode.com/problems/valid-sudoku/description/

// Determine if a 9 x 9 Sudoku board is valid.Only the filled cells need to be validated according to the following rules :

// Each row must contain the digits 1 - 9 without repetition.
// Each column must contain the digits 1 - 9 without repetition.
// Each of the nine 3 x 3 sub - boxes of the grid must contain the digits 1 - 9 without repetition.
// Note :

// A Sudoku board(partially filled) could be valid but is not necessarily solvable.
// Only the filled cells need to be validated according to the mentioned rules.

// Ex1:
// Input: board =
// [["5", "3", ".", ".", "7", ".", ".", ".", "."]
// , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
// , [".", "9", "8", ".", ".", ".", ".", "6", "."]
// , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
// , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
// , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
// , [".", "6", ".", ".", ".", ".", "2", "8", "."]
// , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
// , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
// Output: true

// Ex2:
// Input : board =
// [["8", "3", ".", ".", "7", ".", ".", ".", "."]
// , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
// , [".", "9", "8", ".", ".", ".", ".", "6", "."]
// , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
// , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
// , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
// , [".", "6", ".", ".", ".", ".", "2", "8", "."]
// , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
// , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
// Output: false
// Explanation : Same as Example 1, except with the 5 in the top left corner being modified to 8. 
// Since there are two 8's in the top left 3x3 sub-box, it is invalid.

#include <vector>

using namespace std;

bool isValidSudoku(vector<vector<char>>& board) {
    vector<vector<bool>> rowFlag(9, vector<bool>(9));
    vector<vector<bool>> colFlag(9, vector<bool>(9));
    vector<vector<bool>> cellFlag(9, vector<bool>(9));
    for (int i = 0; i < 9; ++i) {
        for (int j = 0; j < 9; ++j) {
            if (board[i][j] == '.') continue;
            int c = board[i][j] - '1';
            if (rowFlag[i][c] || colFlag[c][j] || cellFlag[3 * (i / 3) + j / 3][c]) return false;
            rowFlag[i][c] = true;
            colFlag[c][j] = true;
            cellFlag[3 * (i / 3) + j / 3][c] = true;
        }
    }
    return true;
}

// Time: O((9!)^9), Space: O(81)
// each row we have 9! number of possibility.
void solveSudoku(vector<vector<char>>& board) {
    helper(board, 0, 0);
}
bool helper(vector<vector<char>>& board, int i, int j) {
    if (i == 9) return true;
    if (j >= 9) return helper(board, i + 1, 0);
    if (board[i][j] != '.') return helper(board, i, j + 1);
    for (char c = '1'; c <= '9'; ++c) {
        if (!isValid(board, i, j, c)) continue;
        board[i][j] = c;
        if (helper(board, i, j + 1)) return true;
        board[i][j] = '.';
    }
    return false;
}
bool isValid(vector<vector<char>>& board, int i, int j, char val) {
    for (int x = 0; x < 9; ++x) {
        if (board[x][j] == val) return false;
    }
    for (int y = 0; y < 9; ++y) {
        if (board[i][y] == val) return false;
    }
    int row = i - i % 3, col = j - j % 3;
    for (int x = 0; x < 3; ++x) {
        for (int y = 0; y < 3; ++y) {
            if (board[x + row][y + col] == val) return false;
        }
    }
    return true;
}```
