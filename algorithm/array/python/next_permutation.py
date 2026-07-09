"""
Next Permutation (LeetCode 31)
https://leetcode.com/problems/next-permutation/

Approaches:
1. next_permutation: Find the rightmost decreasing suffix, swap the pivot with
   the smallest element in the suffix greater than the pivot, then reverse the
   suffix. Time: O(n), Space: O(1).
"""

from typing import List


# Intuition: need to find a sequence such that it keeps decreasing to the right side.
# The index before this sequence is the position we want to swap i.
# And then we would want to sort the sequence after i. reversing it is enough.
# Time: O(n), Space: O(1)
def next_permutation(nums: List[int]) -> None:
    n = len(nums)
    i, j = n - 2, n - 1
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    # reverse nums[i+1:] in place
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def _print(nums: List[int]) -> None:
    print(" ".join(str(x) for x in nums))


if __name__ == "__main__":
    nums = [3, 2, 1]
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)

    nums = [1, 1, 5]
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
    next_permutation(nums); _print(nums)
