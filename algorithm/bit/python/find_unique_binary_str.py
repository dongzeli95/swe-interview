"""
LeetCode 1980: Find Unique Binary String
https://leetcode.com/problems/find-unique-binary-string/

Given an array of strings nums containing n unique binary strings each of
length n, return a binary string of length n that does not appear in nums.

Approaches (mirroring the C++ file 1-to-1):
    1. HashTable  — insert every string parsed as int into a set, then scan
       0..n for a missing integer and format it back to a binary string.
       Time: O(n^2)  Space: O(n)
    2. Bit / Bitmask on popcount — track which "count of ones" values appear
       via a bitmask, then emit a string whose one-count is missing.
       Time: O(n^2)  Space: O(1)
    3. Cantor's diagonal argument — flip nums[i][i] for each i so the answer
       differs from every input in at least one position.
       Time: O(n)    Space: O(1)
"""

from typing import List


# Method 1: HashTable
# Time: O(n^2), int(..., 2) is O(n)
# Space: O(n) integer hash set.
class Solution:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        integers = {int(num, 2) for num in nums}

        n = len(nums)
        for num in range(n + 1):
            if num not in integers:
                # Format as a binary string of width n (equivalent to
                # bitset<16>(num).to_string().substr(16 - n) in C++).
                return format(num, "0{}b".format(n))

        return ""


# Method 2: Bit
# Time: O(n^2), Space: O(1)
# count takes O(n)
class Solution2:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        # Initialize a variable to serve as a bitmask where each bit represents
        # the count of '1's in the binary strings seen so far.
        bitmask = 0
        n = len(nums)

        # Loop through the binary strings.
        for s in nums:
            # Count the number of '1's in the current string.
            count_ones = s.count("1")
            # Set the corresponding bit in the bitmask.
            bitmask |= 1 << count_ones

        # Loop to find a binary string with a different count of '1's.
        for i in range(n):
            # Check if the current count of '1's is not represented in the
            # bitmask. Shift right by i and test the least significant bit.
            if ((bitmask >> i) & 1) == 0:
                # If not set, we found our number. Return a binary string with
                # 'i' ones followed by enough zeros to match the input length.
                return "1" * i + "0" * (len(nums) - i)

        # The loop above is guaranteed to return: there are 2^N possible
        # binary strings of length N, and only N distinct popcounts appear in
        # the input, leaving at least one popcount value unrepresented.
        return ""


# Method 3: Cantor's diagonal argument.
#
# For each index i, look at nums[i][i]. Set ans[i] to the opposite of that
# character. Then ans differs from nums[i] in position i for every i, so it
# cannot equal any string in nums.
#
# Time: O(n), Space: O(1)
class Solution3:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        ans = []
        for i in range(len(nums)):
            curr = nums[i][i]
            ans.append("1" if curr == "0" else "0")

        return "".join(ans)
