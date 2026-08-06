from collections import deque

board = {}
moves = [(-1, 2), (1, 2),
         (2, 1), (2, -1),
         (1, -2), (-1, -2),
         (-2, -1), (-2, 1)]


# ---------------------------------------------------------------------------
# Naive BFS (brute force, no memoization)
# ---------------------------------------------------------------------------
# Enumerate every possible k-step path from (row, column). Count how many end
# on the board, divide by the total number of paths (8^k).
#
# Time:  O(8^k)  — the queue fans out by 8 at each depth. At depth k there
#                  are up to 8^k entries. No state is shared between paths,
#                  so identical (x, y, step) triples are re-expanded many
#                  times. Explodes fast: k=20 → ~1.15e18 states.
# Space: O(8^k)  — the queue holds ~8^(k-1) frontier entries at the widest
#                  level (plus the tail of shallower levels still queued).
#
# This is why the memoized DFS below (or bottom-up DP) is required: it
# collapses the state space to (x, y, step) with at most n * n * (k+1)
# distinct states → O(n^2 * k) time and space.
def knightProbabilityBFS(n, k, row, column):
    if k == 0:
        return 1.0
    num_on_board = 0
    queue = deque()
    queue.append((row, column, 0))
    bfs_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                 (-2, -1), (-1, -2), (1, -2), (2, -1)]
    while queue:
        x, y, step = queue.popleft()
        if step == k:
            num_on_board += 1
            continue
        for dx, dy in bfs_moves:
            tempX = x + dx
            tempY = y + dy
            if tempX < 0 or tempY < 0 or tempX >= n or tempY >= n:
                continue
            queue.append((tempX, tempY, step + 1))
    return num_on_board / pow(8, k)


# ---------------------------------------------------------------------------
# Memoized DFS (top-down DP)
# ---------------------------------------------------------------------------
# Reference: https://leetcode.com/problems/knight-probability-in-chessboard/solutions/3799005/pythonic-solution-video-explanation-dynamic-programming-top-down-dp/
#
# Time:  O(n^2 * k) — each (x, y, steps) state is computed once, 8 moves per state.
# Space: O(n^2 * k) — memo table + recursion depth O(k).
#
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


# ---------------------------------------------------------------------------
# Iterative level-by-level DP with 2D array (most optimal)
# ---------------------------------------------------------------------------
# Roll a probability grid forward one step at a time. current[x][y] holds the
# probability that after `step` moves the knight is at (x, y). For the next
# step, each cell donates prob / 8 to each of its 8 neighbors that stay on
# the board; off-board contributions are simply dropped (they correspond to
# the knight having left the board).
#
# After k steps, the answer is the sum of the final grid.
#
# Why 2D array over a dict:
#   - Constant-time indexed access, no hashing.
#   - Cache-friendly contiguous memory.
#   - No amortized dict resize; predictable memory footprint.
#   - Dict wins only when the reachable set is much smaller than n*n, but
#     the knight's reachable set fills fast so the array is at worst equal
#     and usually faster.
#
# Time:  O(k * n^2) — each of k steps sweeps all n*n cells, 8 neighbors each
#                     (the 8 is a constant factor).
# Space: O(n^2)    — two grids (current + next). This is the key win over
#                     the memoized DFS's O(n^2 * k) table: we never need to
#                     retain intermediate steps, only the frontier.
def knightProbabilityIterative(n, k, row, column):
    iter_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # current[x][y] = probability of being at (x, y) after `step` moves.
    current = [[0.0] * n for _ in range(n)]
    current[row][column] = 1.0

    for _ in range(k):
        next_level = [[0.0] * n for _ in range(n)]
        for x in range(n):
            for y in range(n):
                prob = current[x][y]
                if prob == 0.0:
                    continue
                share = prob / 8.0
                for dx, dy in iter_moves:
                    tx, ty = x + dx, y + dy
                    if 0 <= tx < n and 0 <= ty < n:
                        next_level[tx][ty] += share
        current = next_level

    return sum(sum(row) for row in current)

def main():
    # print(knightProbability(3, 2, 0, 0))
    assert knightProbability(3, 2, 0, 0) == 0.0625
    assert knightProbability(3, 1, 0, 0) == 0.25
    assert knightProbability(1, 0, 0, 0) == 1.0

    # Naive BFS matches on small inputs (blows up past k ~ 10).
    assert knightProbabilityBFS(3, 2, 0, 0) == 0.0625
    assert knightProbabilityBFS(3, 1, 0, 0) == 0.25
    assert knightProbabilityBFS(1, 0, 0, 0) == 1.0

    # Iterative level-by-level DP (most optimal on space).
    assert abs(knightProbabilityIterative(3, 2, 0, 0) - 0.0625) < 1e-9
    assert abs(knightProbabilityIterative(3, 1, 0, 0) - 0.25) < 1e-9
    assert abs(knightProbabilityIterative(1, 0, 0, 0) - 1.0) < 1e-9

if __name__ == "__main__":
    main()