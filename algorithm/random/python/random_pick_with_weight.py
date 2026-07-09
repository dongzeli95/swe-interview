"""
LeetCode 528 - Random Pick with Weight
https://leetcode.com/problems/random-pick-with-weight/

Given a 0-indexed array of positive integers w where w[i] describes the weight
of the ith index, implement pickIndex() which randomly picks an index in the
range [0, len(w) - 1] with probability w[i] / sum(w).

Approaches:
    1. Solution  - Prefix sum + binary search.
                   Init: O(n) time, O(n) space.
                   pickIndex: O(log n) time, O(1) extra space.
    2. Solution2 - Segment tree (supports Follow-up 2: delete picked index).
                   Init: O(n) time, O(n) space.
                   pickIndex: O(log n) time for both query and update.
"""

import random
from bisect import bisect_right
from typing import List


class Solution:
    def __init__(self, w: List[int]):
        # Build prefix sums so that prefix_sum[i] = w[0] + ... + w[i].
        self.prefix_sum: List[int] = []
        prefix_sum = 0
        for weight in w:
            prefix_sum += weight
            self.prefix_sum.append(prefix_sum)
        # total sum
        self.total_sum = self.prefix_sum[-1]

    # Time: O(log n), Space: O(n)
    def pickIndex(self) -> int:
        # random number in [0, total_sum)
        random_num = random.randint(0, self.total_sum - 1)
        # binary search (equivalent to C++ std::upper_bound)
        return bisect_right(self.prefix_sum, random_num)


# Follow up 2: For each index we pick, we delete it from the array.
# Time: O(log n), Space: O(n)
# Segment Tree
class Solution2:
    def __init__(self, w: List[int]):
        self.arr: List[int] = list(w)
        n = len(w)
        self.segTree: List[int] = [0] * (4 * n)
        self.build(1, 0, n - 1)

    def build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.segTree[node] = self.arr[start]
            return

        mid = (start + end) // 2
        self.build(2 * node, start, mid)
        self.build(2 * node + 1, mid + 1, end)
        self.segTree[node] = self.segTree[2 * node] + self.segTree[2 * node + 1]

    def update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self.arr[idx] += val
            self.segTree[node] += val
            return

        mid = (start + end) // 2
        if idx <= mid:
            self.update(2 * node, start, mid, idx, val)
        else:
            self.update(2 * node + 1, mid + 1, end, idx, val)

        self.segTree[node] = self.segTree[2 * node] + self.segTree[2 * node + 1]

    def query(self, node: int, start: int, end: int, val: int, res: int) -> int:
        """Mirror of the C++ query(). Returns the updated `res` since Python
        cannot pass primitives by reference the way C++ does."""
        print(f"start: {start} end: {end} sum: {self.segTree[node]}")
        # If out of boundary, return best index found so far.
        if start > end or self.segTree[node] == 0:
            return res

        # If it's a leaf node, check if it's the best index found so far.
        if start == end:
            if self.segTree[node] <= val and self.arr[start] != 0:
                res = max(res, start)
            return res

        mid = (start + end) // 2
        if self.arr[mid] != 0:
            res = max(res, mid)

        # If the right child has enough weight, search right; else go left.
        if self.segTree[2 * node + 1] >= val:
            res = self.query(2 * node + 1, mid + 1, end, val, res)
        else:
            res = self.query(2 * node, start, mid, val, res)

        return res

    def pickIndex(self) -> int:
        if self.segTree[1] == 0:
            return -1

        # random number in [0, total_sum)
        random_num = random.randint(0, self.segTree[1] - 1)
        # query using segment tree.
        idx = self.query(1, 0, len(self.arr) - 1, random_num, -1)
        # update segment tree along with original array.
        delta = self.arr[idx]
        self.update(1, 0, len(self.arr) - 1, idx, -delta)
        self.print_state()
        return idx

    def print_state(self) -> None:
        print("segment tree")
        print(" ".join(str(x) for x in self.segTree))

        print("array")
        print(" ".join(str(x) for x in self.arr))


if __name__ == "__main__":
    w = [1, 3, 5, 7, 9, 11]
    # solution = Solution(w)
    # print(solution.pickIndex())
    # print(solution.pickIndex())
    # print(solution.pickIndex())
    # print(solution.pickIndex())
    # print(solution.pickIndex())
    # print(solution.pickIndex())

    seg_solution = Solution2(w)
    print(seg_solution.pickIndex())
    print(seg_solution.pickIndex())
    print(seg_solution.pickIndex())
    print(seg_solution.pickIndex())
    print(seg_solution.pickIndex())
    print(seg_solution.pickIndex())
    # print(seg_solution.pickIndex())
