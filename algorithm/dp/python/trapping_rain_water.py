"""
Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water

Given n non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.

Approaches:
    1. trap   - DP with left-max / right-max prefix arrays.  Time O(n), Space O(n).
    2. trap2  - Monotonic decreasing stack of indices.       Time O(n), Space O(n).
"""

from typing import List


# Intuition: track the highest bar to its left and highest bar to its right at every position.
# Time: O(n)
# Space: O(n)
def trap(height: List[int]) -> int:
    n = len(height)
    left = [0] * n
    right = [0] * n

    mx = height[0]
    for i in range(n):
        mx = max(mx, height[i])
        left[i] = mx

    mx = height[n - 1]
    for i in range(n - 1, -1, -1):
        mx = max(mx, height[i])
        right[i] = mx

    res = 0
    for i in range(n):
        res += min(left[i], right[i]) - height[i]

    return res


# Intuition: use a monotonic decreasing stack of indices; when a taller bar is
# seen, pop the shorter bars and add the water bounded by the new bar and the
# element now on the top of the stack.
# Time: O(n)
# Space: O(n)
def trap2(height: List[int]) -> int:
    st: List[int] = []
    i, res, n = 0, 0, len(height)
    while i < n:
        if not st or height[i] <= height[st[-1]]:
            st.append(i)
            i += 1
        else:
            t = st.pop()
            if not st:
                continue
            res += (min(height[i], height[st[-1]]) - height[t]) * (i - st[-1] - 1)
    return res
