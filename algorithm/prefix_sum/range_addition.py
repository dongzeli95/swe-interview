# https://leetcode.com/problems/range-addition/

# You are given an integer length and an array updates where updates[i] = [startIdxi, endIdxi, inci].
# You have an array arr of length length with all zeros, and you have some operation to apply on arr. 
# In the ith operation, you should increment all the elements arr[startIdxi], arr[startIdxi + 1], ..., arr[endIdxi] by inci.
# Return arr after applying all the updates.

# Ex1:
# Input: length = 5, updates = [[1,3,2],[2,4,3],[0,2,-2]]
# Output: [-2,0,3,5,3]

# Ex2:
# Input: length = 10, updates = [[2,4,6],[5,6,8],[1,9,-4]]
# Output: [0,-4,2,2,2,4,4,-4,-4,-4]

# Brute Force
# M updates, N
# Time: O(M*N)

# Update boundaries of update range so that we can leverage prefix sum
# to carry out the final output of the array.
# Time: O(L + M), Space: O(L)
def rangeAddition(length, updates):
    nums = [0 for _ in range(0, length)]
    for u in updates:
        val = u[2]
        nums[u[0]] += val

        if u[1]+1 < length:
            nums[u[1]+1] -= val

    sum = 0
    for i in range(0, length):
        sum += nums[i]
        nums[i] = sum

    return nums


def main():
    # Ex1: [-2,0,3,5,3]
    length = 5
    updates = [[1,3,2],[2,4,3],[0,2,-2]]
    print(rangeAddition(length, updates))

    # Ex2: [0,-4,2,2,2,4,4,-4,-4,-4]
    length = 10
    updates = [[2,4,6],[5,6,8],[1,9,-4]]
    print(rangeAddition(length, updates))

if __name__ == "__main__":
    main()

# 0 0 0 0 0
# 0 2 0 0 -2
# 0 2 3 0 -2
# -2 2 3 2 -2
# -2 0 3 5 3