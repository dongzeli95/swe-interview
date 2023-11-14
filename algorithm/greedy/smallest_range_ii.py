# https://leetcode.com/problems/smallest-range-ii/

# You are given an integer array nums and an integer k.
# For each index i where 0 <= i < nums.length, change nums[i] to be either nums[i] + k or nums[i] - k.
# The score of nums is the difference between the maximum and minimum elements in nums.
# Return the minimum score of nums after changing the values at each index.

# Ex1:
# Input: nums = [1], k = 0
# Output: 0
# Explanation: The score is max(nums) - min(nums) = 1 - 1 = 0.

# Ex2:
# Input: nums = [0,10], k = 2
# Output: 6
# Explanation: Change nums to be [2, 8]. The score is max(nums) - min(nums) = 8 - 2 = 6.

# Ex3:
# Input: nums = [1,3,6], k = 3
# Output: 3
# Explanation: Change nums to be [4, 6, 3]. The score is max(nums) - min(nums) = 6 - 3 = 3.

# [4, 3, 3]
# Intuition: Split the array into 2 parts, the first part is added by k, the second part is subtracted by k.
# For the first part, the min value is the first element + k, the max value is the last element + k.
# For the second part, the min value is the first element - k, the max value is the last element - k.
# The min value for entire array is the min value of the first part and the second part.
# The max value for entire array is the max value of the first part and the second part.
# The result is the difference between the max and min value.
def smallestRangeII(nums, k):
    mn = min(nums)+k
    mx = max(nums)-k

    nums.sort()

    n = len(nums)
    res = max(nums)-min(nums)
    for i in range(0, n-1):
        high = max(nums[i]+k, mx)
        low = min(nums[i+1]-k, mn)
        res = min(res, high-low)

    return res
        

def main():
    # test
    # Ex1: 0 
    nums = [1]
    k = 0
    print(smallestRangeII(nums, k))

    # Ex2: 6
    nums = [0,10]
    k = 2
    print(smallestRangeII(nums, k))

    # Ex3: 3
    nums = [1,3,6]
    k = 3
    print(smallestRangeII(nums, k))

if __name__ == "__main__":
    main()