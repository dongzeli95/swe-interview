"""
Rearrange Array Elements By Sign
https://leetcode.com/problems/rearrange-array-elements-by-sign/

Approaches:
1. rearrangeArray: Split into positives and negatives, then interleave.
   Time: O(n), Space: O(n)
"""

from typing import List


# Time: O(n), Space: O(n)
def rearrangeArray(nums: List[int]) -> List[int]:
    if not nums:
        return []

    pos: List[int] = []
    negs: List[int] = []
    res: List[int] = []

    n = len(nums)
    for i in range(n):
        if nums[i] > 0:
            pos.append(nums[i])
        else:
            negs.append(nums[i])

    i1, i2 = 0, 0
    for i in range(n):
        if i % 2 == 0:
            res.append(pos[i1])
            i1 += 1
        else:
            res.append(negs[i2])
            i2 += 1

    return res


if __name__ == "__main__":
    nums = [3, 1, -2, -5, 2, -4]
    # res = rearrangeArray(nums)
    # print(" ".join(str(x) for x in res))

    nums2 = [28, -41, 22, -8, -37, 46, 35, -9, 18, -6, 19, -26, -37, -10, -9, 15, 14, 31]
    res2 = rearrangeArray(nums2)
    print(" ".join(str(x) for x in res2))
