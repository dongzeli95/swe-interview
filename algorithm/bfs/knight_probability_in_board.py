from collections import deque

board = {}
moves = [(-1, 2), (1, 2),
         (2, 1), (2, -1),
         (1, -2), (-1, -2),
         (-2, -1), (-2, 1)]

# Complexity: https://leetcode.com/problems/knight-probability-in-chessboard/solutions/3799005/pythonic-solution-video-explanation-dynamic-programming-top-down-dp/
# How many points are at (x, y) after steps
def dfs(n, steps, x, y):
    # Base case
    if steps == 0:
        return 1
    
    if (x, y, steps) in board:
        return board[(x, y, steps)]
    
    res = 0
    for m in moves:
        tempX = x + m[0]
        tempY = y + m[1]
        if tempX < 0 or tempX >= n or tempY < 0 or tempY >= n:
            continue
        res += dfs(n, steps - 1, tempX, tempY)

    board[(x, y, steps)] = res
    return res


# n steps -> n-1 steps
def knightProbability(n, k, row, column):
    total = dfs(n, k, row, column)
    # Your logic here
    return total / pow(8, k)

def main():
    # print(knightProbability(3, 2, 0, 0))
    assert knightProbability(3, 2, 0, 0) == 0.0625
    assert knightProbability(3, 1, 0, 0) == 0.25
    assert knightProbability(1, 0, 0, 0) == 1.0

if __name__ == "__main__":
    main()