```python
# https://leetcode.com/problems/maximum-product-of-three-numbers/

# Given an integer array nums, find three numbers whose product is maximum and return the maximum product.
# Example 1:
# Input: nums = [1,2,3]
# Output: 6

# Example 2:
# Input: nums = [1,2,3,4]
# Output: 24

# Example 3:
# Input: nums = [-1,-2,-3]
# Output: -6

# [1, -2, -3, -2] -> 6

# [-3, -2, -2, 1]

# Time: O(nlogn)
def maximumProduct(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    # 1. Sort the array
    # 2. Get the max of the product of the first 3 elements and the product of the last 3 elements
    # 3. Get the max of the product of the first 2 elements and the last element
    # 4. Get the max of the product of the last 2 elements and the first element
    # 5. Return the max of 2, 3, 4
    nums.sort()
    return max(nums[0] * nums[1] * nums[-1], nums[-1] * nums[-2] * nums[-3])

def maximumProduct2(nums):
    if len(nums) == 0:
        return 0

    mn = min(nums)
    mx = max(nums)
    min1 = mx
    min2 = mx
    max1 = mn
    max2 = mn
    max3 = mn

    for val in nums:
        if val < min1:
            min2 = min1
            min1 = val
        elif val < min2:
            min2 = val

        if val > max1:
            max3 = max2
            max2 = max1
            max1 = val
        elif val > max2:
            max3 = max2
            max2 = val
        elif val > max3:
            max3 = val

    return max(min1*min2*max1, max1*max2*max3)



def main():
    assert maximumProduct([1,2,3]) == 6
    assert maximumProduct2([1,2,3]) == 6
    assert maximumProduct([1,2,3,4]) == 24
    assert maximumProduct2([1,2,3,4]) == 24
    assert maximumProduct([-1,-2,-3]) == -6
    assert maximumProduct2([-1,-2,-3]) == -6
    assert maximumProduct([1, -2, -3, -2]) == 6
    assert maximumProduct2([1, -2, -3, -2]) == 6

if __name__ == "__main__":
    main()```
