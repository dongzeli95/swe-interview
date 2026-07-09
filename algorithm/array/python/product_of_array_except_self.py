"""
Product of Array Except Self.

Given an integer array nums, return an array answer such that answer[i] is
equal to the product of all the elements of nums except nums[i].

Must run in O(n) time and without using the division operation.

Approaches:
    1. productExceptSelfTwoPassTwoArray - Two pass using two auxiliary arrays.
       Time: O(n), Space: O(n).
    2. productExceptSelfTwoPass          - Two pass using the output array only.
       Time: O(n), Space: O(1) excluding output.
    3. productExceptSelfOnePass          - One pass, updates output from both ends.
       Time: O(n), Space: O(1) excluding output.
"""

from typing import List


# Time complexity: O(n), Space complexity: O(n), Two pass
def productExceptSelfTwoPassTwoArray(nums: List[int]) -> List[int]:
    if not nums:
        return []

    n = len(nums)
    left = [1] * n
    right = [1] * n

    left[0] = nums[0]
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i]

    right[n - 1] = nums[n - 1]
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i]

    res = [1] * n
    for i in range(n):
        l = left[i - 1] if (i - 1) >= 0 else 1
        r = right[i + 1] if (i + 1) < n else 1
        res[i] = l * r

    return res


# Two pass but using same output array
# Time complexity: O(n), Space complexity: O(1) if we don't count the output array.
def productExceptSelfTwoPass(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] *= prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res


# One pass
# Time complexity: O(n), Space complexity: O(1) if we don't count the output array.
def productExceptSelfOnePass(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [1] * n
    prefix = 1
    suffix = 1

    for i in range(n):
        res[i] *= prefix
        prefix *= nums[i]

        res[n - 1 - i] *= suffix
        suffix *= nums[n - 1 - i]

    return res


if __name__ == "__main__":
    # Test two pass with two arrays
    nums = [1, 2, 3, 4]
    res = productExceptSelfTwoPassTwoArray(nums)
    expected = [24, 12, 8, 6]
    assert res == expected

    nums = [-1, 1, 0, -3, 3]
    res = productExceptSelfTwoPassTwoArray(nums)
    expected = [0, 0, 9, 0, 0]
    assert res == expected

    nums = [1, 2, 3, 4]
    res = productExceptSelfTwoPass(nums)
    expected = [24, 12, 8, 6]
    assert res == expected

    nums = [-1, 1, 0, -3, 3]
    res = productExceptSelfTwoPass(nums)
    expected = [0, 0, 9, 0, 0]
    assert res == expected

    # Test one pass
    nums = [1, 2, 3, 4]
    res = productExceptSelfOnePass(nums)
    expected = [24, 12, 8, 6]
    assert res == expected

    nums = [-1, 1, 0, -3, 3]
    res = productExceptSelfOnePass(nums)
    expected = [0, 0, 9, 0, 0]
    assert res == expected
