"""
Subarray Sums Divisible by K
https://leetcode.com/problems/subarray-sums-divisible-by-k/description/

Given an integer array nums and an integer k, return the number of non-empty
subarrays that have a sum divisible by k. A subarray is a contiguous part of
an array.

Key insight:
We want to count pairs (i, j) where i < j and (prefixSum[j] - prefixSum[i]) % k == 0.
This holds iff prefixSum[i] % k == prefixSum[j] % k.

Approaches:
    1. subarraysDivByK: Prefix sum + hash map of remainder counts.
       Time: O(n), Space: O(k)
"""

from collections import defaultdict
from typing import List


# Time: O(n), Space: O(k)
def subarraysDivByK(A: List[int], K: int) -> int:
    res = 0
    s = 0
    m = defaultdict(int)
    m[0] = 1
    for num in A:
        s = (s + num % K + K) % K
        res += m[s]
        m[s] += 1
    return res
