\n```python\n
# https://leetcode.com/problems/find-the-duplicate-number/

# Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
# There is only one repeated number in nums, return this repeated number.
# You must solve the problem without modifying the array nums and uses only constant extra space.

# Ex1:
# Input: nums = [1,3,4,2,2]
# Output: 2

# Ex2:
# Input: nums = [3,1,3,4,2]
# Output: 3

class Solution:
    def findDuplicate(self, nums):
        # Phase 1
        slow = nums[0]
        fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        # Phase 2
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow


# 0001
# 0011
# 0100
# 0010
# 0010

# 0110

# 0001
# 0010
# 0011
# 0100
# 0100

# 0111


def main():
    # test
    # Ex1: 2
    nums = [1,3,4,2,2]
    print(Solution().findDuplicate(nums))

    # Ex2: 3
    nums = [3,1,3,4,2]
    print(Solution().findDuplicate(nums))

if __name__ == "__main__":
    main()```
