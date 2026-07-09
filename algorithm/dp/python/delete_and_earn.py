"""
Delete and Earn
https://leetcode.com/problems/delete-and-earn/

You are given an integer array nums. You want to maximize the number of points
you get by performing the following operation any number of times:
Pick any nums[i] and delete it to earn nums[i] points. Afterwards, you must
delete every element equal to nums[i] - 1 and every element equal to nums[i] + 1.
Return the maximum points you can earn.

Approaches:
1. Solution.deleteAndEarn1: Brute-force DFS over the set of remaining numbers
   with memoization keyed by a string encoding of "still available" numbers.
   Time: exponential in the number of distinct values; Space: exponential.
2. Solution.deleteAndEarn: Top-down DP over the value axis (0..max(nums)).
   For each value v: choose max(sum(v) + dp(v-2), dp(v-1)).
   Time: O(n + mx), Space: O(n + mx).
"""

from collections import defaultdict
from typing import Dict, List


class Solution:
    # Approach 1: DFS with memoization on a string key over the distinct values.
    # Mirrors deleteAndEarn1 / dfs from the C++ source 1-to-1.
    def _dfs(
        self,
        m: Dict[int, List[int]],  # num -> [sum, idx_in_key]
        key: List[str],
        cache: Dict[str, int],
    ) -> int:
        key_str = "".join(key)
        if key_str in cache:
            return cache[key_str]

        total = 0
        for num, pair in list(m.items()):
            s, idx = pair[0], pair[1]
            if s == 0:
                continue

            plus_one = m[num + 1][0] if (num + 1) in m else 0
            minus_one = m[num - 1][0] if (num - 1) in m else 0

            # Save & zero-out
            m[num][0] = 0
            if (num + 1) in m:
                m[num + 1][0] = 0
            if (num - 1) in m:
                m[num - 1][0] = 0

            c = key[idx]
            key[idx] = "#"

            total = max(total, s + self._dfs(m, key, cache))

            # Restore
            if (num + 1) in m:
                m[num + 1][0] = plus_one
            if (num - 1) in m:
                m[num - 1][0] = minus_one
            m[num][0] = s
            key[idx] = c

        cache[key_str] = total
        return total

    def deleteAndEarn1(self, nums: List[int]) -> int:
        m: Dict[int, List[int]] = {}
        cache: Dict[str, int] = {}
        key: List[str] = []

        for x in nums:
            if x not in m:
                m[x] = [0, len(key)]
                key.append(str(x))
            m[x][0] += x

        return self._dfs(m, key, cache)

    # Approach 2: Top-down DP over the value axis. Time O(n + mx), Space O(n + mx).
    def _topDownDP(
        self,
        num: int,
        cache: Dict[int, int],
        m: Dict[int, int],
    ) -> int:
        if num == 0:
            return 0
        if num == 1:
            return m[1]
        if num in cache:
            return cache[num]

        res = max(
            m[num] + self._topDownDP(num - 2, cache, m),
            self._topDownDP(num - 1, cache, m),
        )
        cache[num] = res
        return res

    def deleteAndEarn(self, nums: List[int]) -> int:
        mx = 0
        m: Dict[int, int] = defaultdict(int)
        for x in nums:
            mx = max(x, mx)
            m[x] += x

        cache: Dict[int, int] = {}
        return self._topDownDP(mx, cache, m)


if __name__ == "__main__":
    sol = Solution()

    nums = [3, 4, 2]
    assert sol.deleteAndEarn(nums) == 6

    nums = [2, 2, 3, 3, 3, 4]
    assert sol.deleteAndEarn(nums) == 9

    print("All tests passed.")
