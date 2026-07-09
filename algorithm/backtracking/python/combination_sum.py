"""
Combination Sum I / II / III (LeetCode 39, 40, 216).

Approaches:
1. combinationSum  - Backtracking over sorted-by-index candidates, at each index
                     try using the current candidate 0..k times (k*cand<=target),
                     then recurse to next index. Same candidate may be reused.
                     Time: O(N^(T/M + 1)) where N=|candidates|, T=target, M=min(candidates).
                     Space: O(T/M) recursion depth.

2. combinationSum2 - Sort candidates, DFS picking each element at most once,
                     skip duplicates at the same recursion level via
                     (i > idx and candidates[i] == candidates[i-1]).
                     Time: O(2^n * target) worst-case (copy of combination into result).
                     Space: O(target) stack + O(2^n) result.

3. combinationSum3 - DFS over digits 1..9 picking k distinct numbers summing to n,
                     each digit used at most once, ascending order.
                     Time: O(k * 9! / (9-k)!) with upper bound O(9^k).
                     Space: O(k) recursion depth.
"""

from typing import List


# https://leetcode.com/problems/combination-sum/
# n-ary tree, the maximum number of nodes of T/M height is N^(T/M+1)
def _helper(candidates: List[int], target: int, idx: int,
            curr: List[int], res: List[List[int]]) -> None:
    if target == 0:
        res.append(curr[:])
        return

    n = len(candidates)
    if target < 0 or idx >= n:
        return

    multiplier = 0
    while multiplier * candidates[idx] <= target:
        for _ in range(multiplier):
            curr.append(candidates[idx])
        _helper(candidates, target - multiplier * candidates[idx], idx + 1, curr, res)
        for _ in range(multiplier):
            curr.pop()
        multiplier += 1


def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    res: List[List[int]] = []
    curr: List[int] = []
    _helper(candidates, target, 0, curr, res)
    return res


# https://leetcode.com/problems/combination-sum-ii/
# n: number of candidates
# Time: O(2^n * target) - target is the longest combination length, must copy into result.
# Space:
#   a. Stack: O(target)
#   b. Result: O(2^n)
def _dfs2(candidates: List[int], idx: int, curr: List[int],
          sum_state: List[int], target: int, res: List[List[int]]) -> None:
    if sum_state[0] == target:
        res.append(curr[:])
        return

    n = len(candidates)
    if idx >= n or sum_state[0] > target:
        return

    for i in range(idx, n):
        # This optimization prevents using a set for dedup.
        if i > idx and candidates[i] == candidates[i - 1]:
            continue
        curr.append(candidates[i])
        sum_state[0] += candidates[i]
        _dfs2(candidates, i + 1, curr, sum_state, target, res)
        sum_state[0] -= candidates[i]
        curr.pop()


def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:
    # sort to dedup duplicates caused by order.
    candidates.sort()
    res: List[List[int]] = []
    curr: List[int] = []
    sum_state = [0]  # mimic C++ int& sum
    _dfs2(candidates, 0, curr, sum_state, target, res)
    return res


# https://leetcode.com/problems/combination-sum-iii
# Time:
#   Upper bound: O(9^k)
#   Per exploration path: O(9 * 8 * 7 * ... * (10 - k)) = 9! / (9 - k)!
#   Overall: O(k * 9! / (9 - k)!)
# Space: O(k)
def _dfs(k: int, n: int, curr: List[int], res: List[List[int]], idx: int) -> None:
    if k == 0 and n == 0:
        res.append(curr[:])
        return

    for i in range(idx, 10):
        if i > n:
            break
        curr.append(i)
        _dfs(k - 1, n - i, curr, res, i + 1)
        curr.pop()


def combinationSum3(k: int, n: int) -> List[List[int]]:
    if k == 0 or n == 0:
        return []

    res: List[List[int]] = []
    curr: List[int] = []
    _dfs(k, n, curr, res, 1)
    return res


if __name__ == "__main__":
    candidates = [2, 3, 6, 7]
    res = combinationSum(candidates, 7)
    for row in res:
        print(", ".join(str(x) for x in row) + ", ")
