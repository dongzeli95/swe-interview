"""Segment tree implementation (range sum with point updates).

Approaches:
    1. SegmentTree: recursive 1-indexed array-backed segment tree over an
       input array. build O(n), point update O(log n), range query O(log n),
       space O(4n).
"""

from typing import List


class SegmentTree:
    def __init__(self, arr: List[int]) -> None:
        self.arr = list(arr)
        n = len(self.arr)
        self.segTree = [0] * (4 * n)
        if n > 0:
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

    def query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.segTree[node]

        mid = (start + end) // 2
        return (
            self.query(2 * node, start, mid, l, r)
            + self.query(2 * node + 1, mid + 1, end, l, r)
        )

    def print(self) -> None:
        print(" ".join(str(x) for x in self.segTree))


if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    st.print()
    # 3 + 5 + 7 = 15
    print(
        "Initial sum of range (1, 3):",
        st.query(1, 0, len(arr) - 1, 1, 3),
    )
    st.update(1, 0, len(arr) - 1, 1, 7)
    # 22
    print(
        "Updated sum of range (1, 3):",
        st.query(1, 0, len(arr) - 1, 1, 3),
    )
