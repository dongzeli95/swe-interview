# https://leetcode.com/problems/permutations/

# Given an array nums of distinct integers, return all the possible permutations.You can return the answer in any order.
# Example 1:
# Input: nums = [1, 2, 3]
# Output : [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

# Example 2 :
# Input : nums = [0, 1]
# Output : [[0, 1], [1, 0]]

# Example 3 :
# Input : nums = [1]
# Output : [[1]]

# Time: O(n*n!), Space: O(n)
# Giving a set of length n, the number of permutations is n!
# for each permutation, we need O(n) to copy nums
def dfs(idx, nums, res):
    if idx == len(nums):
        res.append(nums.copy())

    n = len(nums)
    for i in range(idx, n):
        nums[i], nums[idx] = nums[idx], nums[i]
        dfs(idx+1, nums, res)
        nums[i], nums[idx] = nums[idx], nums[i]

def permute(nums):
    res = []
    dfs(0, nums, res)
    return res

def main():
    res = permute([1, 2, 3])
    print(res)

    res = permute([0, 1])
    print(res)

    res = permute([1])
    print(res)

if __name__ == "__main__":
    main()
