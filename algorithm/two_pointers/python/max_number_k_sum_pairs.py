"""
Max Number of K-Sum Pairs
https://leetcode.com/problems/max-number-of-k-sum-pairs

You are given an integer array nums and an integer k. In one operation, you can
pick two numbers from the array whose sum equals k and remove them from the
array. Return the maximum number of operations you can perform on the array.

Approaches:
1. maxOperations           - Hash map counting. Time O(n), Space O(n).
2. maxOperationsTwoPointer - Sort + two pointers. Time O(n log n), Space O(1).
"""

from collections import defaultdict
from typing import List


# Time complexity: O(n), Space complexity: O(n)
def maxOperations(nums: List[int], k: int) -> int:
    if not nums:
        return 0

    m = defaultdict(int)
    for x in nums:
        m[x] += 1

    res = 0
    # Snapshot keys because we mutate m during iteration.
    for val in list(m.keys()):
        cnt = m[val]
        if cnt <= 0:
            continue

        if (k - val) in m and m[k - val] > 0:
            if k - val == val:
                res += cnt // 2
                m[k - val] = 0
            else:
                res += min(cnt, m[k - val])
                # Don't forget to clear all values to 0.
                m[k - val] = 0
                m[val] = 0

    return res


# Two pointers
# Time complexity: O(n log n), Space complexity: O(1)
def maxOperationsTwoPointer(nums: List[int], k: int) -> int:
    if not nums:
        return 0

    nums.sort()
    res = 0
    n = len(nums)

    l, r = 0, n - 1

    while l < r:
        s = nums[l] + nums[r]
        if s > k:
            r -= 1
        elif s < k:
            l += 1
        else:
            res += 1
            l += 1
            r -= 1

    return res


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    k = 5
    assert maxOperations(list(nums), k) == 2
    assert maxOperationsTwoPointer(list(nums), k) == 2

    nums = [3, 1, 3, 4, 3]
    k = 6
    assert maxOperations(list(nums), k) == 1
    assert maxOperationsTwoPointer(list(nums), k) == 1

    nums = [2, 2, 2, 3, 1, 1, 4, 1]
    k = 4
    assert maxOperations(list(nums), k) == 2
    assert maxOperationsTwoPointer(list(nums), k) == 2

    nums = [2, 5, 4, 4, 1, 3, 4, 4, 1, 4, 4, 1, 2, 1, 2, 2, 3, 2, 4, 2]
    k = 3
    assert maxOperations(list(nums), k) == 4
    assert maxOperationsTwoPointer(list(nums), k) == 4

    print("All tests passed.")
