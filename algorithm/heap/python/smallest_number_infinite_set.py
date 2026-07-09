"""
Smallest Number in Infinite Set
https://leetcode.com/problems/smallest-number-in-infinite-set

Approaches:
1. SmallestInfiniteSetAddBackWithPQ - Min-heap tracks addBack candidates below currMin.
   n = number of addBack, m = number of popSmallest.
   Time: O((m+n)*log(n)), Space: O(n)
2. SmallestInfiniteSet - Two sorted sets: popSet (already popped) and backSet (added back).
   Time: O((m+n)*log(m+n)), Space: O(m+n)
"""

import heapq
from sortedcontainers import SortedSet


# Priority queue on addBack operation.
# Use a min heap to keep track of potential smallest number candidates.
#
# n: number of addBack, m: number of popSmallest
# Time complexity: O((m+n)*log(n)), Space complexity: O(n)
class SmallestInfiniteSetAddBackWithPQ:
    def __init__(self) -> None:
        self.curr_min = 1
        self.pq: list[int] = []  # min-heap
        self.exist: set[int] = set()

    def popSmallest(self) -> int:
        if not self.pq:
            res = self.curr_min
            self.curr_min += 1
            return res

        res = heapq.heappop(self.pq)
        # Don't forget to remove the number from the set.
        self.exist.discard(res)
        return res

    def addBack(self, num: int) -> None:
        # If the number is already in the set, we don't need to do anything.
        # If the number is greater than the current min, meaning we haven't popped it yet.
        if num in self.exist or num >= self.curr_min:
            return

        heapq.heappush(self.pq, num)
        self.exist.add(num)


# Two sets: popSet and backSet.
#
# n: number of addBack, m: number of popSmallest
# Time complexity: O((m+n)*log(m+n)), Space complexity: O(m+n)
class SmallestInfiniteSet:
    def __init__(self) -> None:
        self.pop_set: SortedSet = SortedSet()
        self.back_set: SortedSet = SortedSet()

    def popSmallest(self) -> int:
        if not self.pop_set and not self.back_set:
            self.pop_set.add(1)
            return 1

        if not self.back_set:
            last_pop = self.pop_set[-1]
            res = last_pop + 1
            self.pop_set.add(res)
            return res
        else:
            res = self.back_set[0]
            self.back_set.remove(res)
            self.pop_set.add(res)
            return res

    def addBack(self, num: int) -> None:
        if num not in self.pop_set:
            return

        self.back_set.add(num)
        self.pop_set.remove(num)


if __name__ == "__main__":
    s = SmallestInfiniteSet()

    s.addBack(2)
    assert s.popSmallest() == 1
    assert s.popSmallest() == 2
    assert s.popSmallest() == 3
    s.addBack(1)
    assert s.popSmallest() == 1
    assert s.popSmallest() == 4
    assert s.popSmallest() == 5

    s_pq = SmallestInfiniteSetAddBackWithPQ()
    s_pq.addBack(2)
    assert s_pq.popSmallest() == 1
    assert s_pq.popSmallest() == 2
    assert s_pq.popSmallest() == 3
    s_pq.addBack(1)
    assert s_pq.popSmallest() == 1
    assert s_pq.popSmallest() == 4
    assert s_pq.popSmallest() == 5

    print("All tests passed")
