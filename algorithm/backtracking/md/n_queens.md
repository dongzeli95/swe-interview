\n```python\n
# https://leetcode.com/problems/n-queens/

# The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

# Given an integer n, return all distinct solutions to the n-queens puzzle. 
# You may return the answer in any order.

# Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

# Ex1:
# Input: n = 4
# Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
# Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above

# Ex2:
# Input: n = 1
# Output: [["Q"]]

# Q...
# ...Q
# .Q..
# ..Q.

import copy

def update_mark(mark, row, col, n):
    # Invalidate the same column after row.
    for j in range(row+1, n):
        mark[j][col] = False
        
    # invalidate the same diagnal after row.
    # left diagonal, col-1, row+1
    c = col-1
    r = row+1
    while c >= 0 and r < n:
        mark[r][c] = False
        r += 1
        c -= 1

    # right diagonal, col+1, row+1
    c = col+1
    r = row+1
    while c < n and r < n:
        mark[r][c] = False
        r += 1
        c += 1

def dfs(n, row, board, mark, res):
    if row == n:
        res.append(["".join(row) for row in board])
        return
    
    for i in range(n):
        if mark[row][i] == False:
            # print("continue, row: " + str(row) + " i: " + str(i))
            continue

        # Put queen at this position
        board[row][i] = 'Q'
        mark_copy = copy.deepcopy(mark)
        update_mark(mark, row, i, n)
        dfs(n, row+1, board, mark, res)
        mark = copy.deepcopy(mark_copy)
        board[row][i] = '.'

def solveNQueens(n):
    board = [['.' for _ in range(n)] for _ in range(n)]
    mark = [[True for _ in range(n)] for _ in range(n)]
    res = []
    dfs(n, 0, board, mark, res)
    return res

def main():
    # test case
    print(solveNQueens(4))
    print(solveNQueens(1))

if __name__ == "__main__":
    main()```
