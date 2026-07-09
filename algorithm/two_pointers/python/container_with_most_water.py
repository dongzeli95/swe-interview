"""
Container With Most Water
https://leetcode.com/problems/container-with-most-water/

You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
Find two lines that together with the x-axis form a container, such that the
container contains the most water. Return the maximum amount of water a
container can store.

Approaches:
    1. Two pointers - Time: O(n), Space: O(1)
"""

from typing import List


# Time: O(n), Space: O(1)
def maxArea(height: List[int]) -> int:
    if not height:
        return 0

    l = 0
    r = len(height) - 1

    res = 0
    while l < r:
        res = max(res, min(height[l], height[r]) * (r - l))
        if height[l] <= height[r]:
            l += 1
        else:
            r -= 1

    return res


if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    assert maxArea(height) == 49

    height = [1, 1]
    assert maxArea(height) == 1
