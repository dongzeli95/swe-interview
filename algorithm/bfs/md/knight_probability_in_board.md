# Knight Probability in Chessboard (LeetCode 688)

Given an `n x n` board, a knight starts at `(row, column)` and makes exactly `k` moves. Each of the 8 knight moves is chosen uniformly at random. Return the probability that the knight is still on the board after `k` moves.

## Approach 1 — Naive BFS (brute force)

Enumerate every possible k-step path. Count how many end on the board and divide by the total number of paths `8^k` (each step has 8 equally-likely choices, regardless of whether a landing square is off-board — off-board paths are counted in the denominator but not the numerator).

```python
from collections import deque

def knightProbabilityBFS(n, k, row, column):
    if k == 0:
        return 1.0
    num_on_board = 0
    queue = deque()
    queue.append((row, column, 0))
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
             (-2, -1), (-1, -2), (1, -2), (2, -1)]
    while queue:
        x, y, step = queue.popleft()
        if step == k:
            num_on_board += 1
            continue
        for dx, dy in moves:
            tempX = x + dx
            tempY = y + dy
            if tempX < 0 or tempY < 0 or tempX >= n or tempY >= n:
                continue
            queue.append((tempX, tempY, step + 1))
    return num_on_board / pow(8, k)
```

### Complexity

- **Time:** `O(8^k)`. The queue fans out by up to 8 at each depth. At depth `k` there are up to `8^k` entries. No state is shared between paths, so identical `(x, y, step)` triples are re-expanded many times.
  - `k = 10` → ~1e9 states (already too slow)
  - `k = 20` → ~1.15e18 states (impossible)
- **Space:** `O(8^k)`. The queue holds ~`8^(k-1)` frontier entries at the widest level, plus the tail of shallower levels still queued.

### Why it fails at scale

The state `(x, y, step)` has only `n * n * (k + 1)` distinct values, but naive BFS revisits the same state along many different paths. On a 25×25 board with `k = 100`, the true state space is `62,500` — but naive BFS would explore `8^100 ≈ 2e90` paths.

Fix: memoize by `(x, y, step)` (Approach 2) or roll a bottom-up DP over step-by-step probability grids.

## Approach 2 — Memoized DFS (top-down DP)

Reference: [LeetCode discussion](https://leetcode.com/problems/knight-probability-in-chessboard/solutions/3799005/pythonic-solution-video-explanation-dynamic-programming-top-down-dp/)

`dfs(x, y, steps)` returns the number of length-`steps` paths starting at `(x, y)` that stay on the board. Divide the final count by `8^k` for the probability.

```python
from collections import deque

board = {}
moves = [(-1, 2), (1, 2),
         (2, 1), (2, -1),
         (1, -2), (-1, -2),
         (-2, -1), (-2, 1)]

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
    return total / pow(8, k)

def main():
    assert knightProbability(3, 2, 0, 0) == 0.0625
    assert knightProbability(3, 1, 0, 0) == 0.25
    assert knightProbability(1, 0, 0, 0) == 1.0

if __name__ == "__main__":
    main()
```

### Complexity

- **Time:** `O(n^2 * k)`. Each `(x, y, steps)` state is computed once; 8 moves per state.
- **Space:** `O(n^2 * k)` for the memo table, plus `O(k)` recursion depth.

Note: the memo `board` is a module-level dict here — reset it between test cases if reusing across different `n`, or scope it to the function.

## Approach 3 — Iterative level-by-level DP with 2D array (most optimal)

Roll a probability grid forward one step at a time. `current[x][y]` is the probability that after `step` moves the knight is at `(x, y)`. On each step, every cell donates `prob / 8` to each of its 8 knight-neighbors that stay on the board; off-board contributions are dropped (they represent the knight having left the board). After `k` steps the answer is the sum of the final grid.

```python
def knightProbabilityIterative(n, k, row, column):
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
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
                for dx, dy in moves:
                    tx, ty = x + dx, y + dy
                    if 0 <= tx < n and 0 <= ty < n:
                        next_level[tx][ty] += share
        current = next_level

    return sum(sum(row) for row in current)
```

### Why 2D array over a dict

The dict version (`current: dict[(x, y)] -> prob`) is clean but incurs:
- Hash cost per read/write.
- Non-contiguous memory → poor cache behavior.
- Dict resizes as the reachable set grows.

The 2D array wins because:
- **Constant-time indexed access, no hashing.**
- **Cache-friendly** contiguous memory — a single step is a linear sweep.
- **Predictable footprint** — always `2 * n²` floats, no resize churn.

Dict would only win when the reachable set stays much smaller than `n²`, but a knight's reach fans out fast, so within a few steps most of the board is populated. The array is at worst equal and usually faster.

### Complexity

- **Time:** `O(k · n²)`. Each of `k` steps sweeps all `n²` cells; each cell inspects 8 constant-cost neighbors.
- **Space:** `O(n²)`. Two grids — `current` and `next_level`. This is the key improvement over Approach 2's `O(n² · k)` memo table: we only retain the frontier, never past steps.

### Comparison

| Approach            | Time         | Space        | Notes                                              |
| ------------------- | ------------ | ------------ | -------------------------------------------------- |
| Naive BFS           | `O(8^k)`     | `O(8^k)`     | Explodes past `k ≈ 10`.                            |
| Memoized DFS        | `O(n² · k)`  | `O(n² · k)`  | Correct polynomial time but keeps every step.      |
| **Iterative 2D DP** | **`O(n² · k)`** | **`O(n²)`**  | Same time as memo, but `k`× less memory. Preferred. |

### One caveat: floating-point accumulation

Tracking probability directly means each step multiplies by `1/8` and sums; errors accumulate over `k` steps. For LeetCode 688 with `k ≤ 100` this stays comfortably under the 1e-5 tolerance. If tighter precision were required, keep integer path counts on the grid and divide by `8^k` only at the end (same recurrence, exact arithmetic).

