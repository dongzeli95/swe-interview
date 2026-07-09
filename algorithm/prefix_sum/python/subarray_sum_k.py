# https://leetcode.com/problems/subarray-sums-divisible-by-k/

# Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.
# A subarray is a contiguous part of an array.

# Ex1:
# Input: nums = [4,5,0,-2,-3,1], k = 5
# Output: 7
# Explanation: There are 7 subarrays with a sum divisible by k = 5:
# [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]

# Ex2:
# Input: nums = [5], k = 9
# Output: 0

# [0, 4, 9, 9, 7, 4, 5]
# hash map keep track of sums count.
# Time: O(n), Space: O(k)
def subarrayDivByK(nums, k):
    modMaps = {}
    sum = 0
    modMaps[0] = 1

    res = 0
    for i in nums:
        sum += i
        m = sum % k
        if m in modMaps:
            res += modMaps[sum%k]
            modMaps[m] += 1
        else:
            modMaps[sum%k] = 1

    return res

def main():
    # Ex1: 7
    nums = [4,5,0,-2,-3,1]
    k = 5
    print(subarrayDivByK(nums, k))

    # Ex2: 0
    nums = [5]
    k = 9
    print(subarrayDivByK(nums, k))

if __name__ == "__main__":
    main()