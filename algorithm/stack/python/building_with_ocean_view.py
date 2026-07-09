"""
Buildings With an Ocean View
https://leetcode.com/problems/buildings-with-an-ocean-view/

There are n buildings in a line. The ocean is to the right of the buildings.
A building has an ocean view if all the buildings to its right have a strictly
smaller height. Return the indices (sorted ascending) of buildings with an
ocean view.

Approaches:
    1. findBuildings (monotonic stack, left-to-right):
       Walk left to right, maintaining a monotonic-decreasing stack of indices.
       Whenever the current building is >= the top of the stack, pop; then push
       the current index. Time O(n), Space O(n).
"""

from typing import List


def findBuildings(heights: List[int]) -> List[int]:
    if not heights:
        return []

    res: List[int] = []
    n = len(heights)
    for i in range(n):
        while res and heights[i] >= heights[res[-1]]:
            res.pop()

        res.append(i)

    return res


if __name__ == "__main__":
    h1 = [4, 2, 3, 1]
    res1 = findBuildings(h1)
    print(" ".join(str(i) for i in res1))

    h2 = [4, 3, 2, 1]
    res2 = findBuildings(h2)
    print(" ".join(str(i) for i in res2))

    h3 = [1, 3, 2, 4]
    res3 = findBuildings(h3)
    print(" ".join(str(i) for i in res3))
