"""
LeetCode 2013: Detect Squares
https://leetcode.com/problems/detect-squares/description/

Approaches:
1. DetectSquares (hash map of point counts + points list):
   - add: O(1)
   - count: O(n) where n is the number of add() calls; iterate all stored
     points treating each as the opposite diagonal corner p3, then multiply
     counts of the two implied corners p2=(x1,y3) and p4=(x3,y1).
"""

from collections import defaultdict
from typing import List


class DetectSquares:
    def __init__(self):
        # cntPoints[(x, y)] -> number of times point has been added
        self.cntPoints = defaultdict(int)
        # list of all added points (duplicates preserved)
        self.points: List[tuple] = []

    def add(self, point: List[int]) -> None:
        self.cntPoints[(point[0], point[1])] += 1
        self.points.append((point[0], point[1]))

    # Time: O(n)
    def count(self, point: List[int]) -> int:
        x1, y1 = point[0], point[1]
        ans = 0
        for x3, y3 in self.points:
            # Skip empty square (same x) or invalid (not on a diagonal)
            if abs(x1 - x3) == 0 or abs(x1 - x3) != abs(y1 - y3):
                continue
            ans += self.cntPoints[(x1, y3)] * self.cntPoints[(x3, y1)]
        return ans
