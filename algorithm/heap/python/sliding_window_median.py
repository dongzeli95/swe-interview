"""Sliding Window Median.

Maintain the running median of the last `cap` values inserted.

Approaches:
  1. Median class using a sorted multiset with an iterator tracking the
     lower-median position, plus a deque for FIFO eviction.
     - add_value:   O(log n)
     - get_median:  O(1) (indexed access into the sorted structure)

Python note: The C++ solution uses std::multiset<int> and an iterator that
points at the (lower) median. Python's stdlib has no equivalent sorted
multiset with iterators, so we use sortedcontainers.SortedList, which
provides O(log n) add/remove and O(log n) indexed access. We track the
median position with an integer index `it` (the index of the lower
median), which mirrors the C++ iterator arithmetic 1-to-1.
"""

from collections import deque
from sortedcontainers import SortedList


class Median:
    def __init__(self, cap: int):
        self.ms = SortedList()
        self.dq: deque[int] = deque()
        self.cap = cap
        self.it = 0  # index into self.ms pointing at the (lower) median
        self.curr_pos = 0

    # O(log n)
    def add_value(self, val: int) -> None:
        # Insert the new value
        self.ms.add(val)
        self.dq.append(val)

        # Adjust the iterator for the first element
        if len(self.ms) == 1:
            self.it = 0
            return

        # Adjust the iterator if the new element is less than the current median
        if val < self.ms[self.it]:
            self.it -= 1

        # If the size exceeds the capacity, remove the oldest element
        if len(self.dq) > self.cap:
            front = self.dq.popleft()
            if front <= self.ms[self.it]:
                self.it += 1
            self.ms.remove(front)

    # Time: O(1) amortized (indexed access is O(log n) in SortedList)
    def get_median(self) -> float:
        is_odd = len(self.ms) % 2
        if is_odd:
            return float(self.ms[self.it])
        else:
            return (self.ms[self.it] + self.ms[self.it + 1]) / 2.0

    def debug(self) -> None:
        for i in self.ms:
            print(i)


# [1, 2]
# [1, 2, 3]

# [2, 3] -> 3
# [1, 2, 3] -> 2
# [1, 3]
if __name__ == "__main__":
    median = Median(2)
    median.add_value(1)
    print(median.get_median())  # 1

    median.add_value(2)
    print(median.get_median())  # 1.5

    median.add_value(3)
    print(median.get_median())  # 2.5

    median.add_value(1)
    print(median.get_median())  # 2

    median.add_value(9)
    print(median.get_median())  # 5
