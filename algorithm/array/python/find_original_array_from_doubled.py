"""
Find Original Array From Doubled Array
https://leetcode.com/problems/find-original-array-from-doubled-array/

An integer array `original` is transformed into a doubled array `changed` by
appending twice the value of every element in `original`, then randomly
shuffling the resulting array. Given `changed`, return `original` if
`changed` is a doubled array; otherwise return an empty array.

Approaches:
    1. Sorting + Hashmap frequency counting.
       Time: O(n log n), Space: O(n)
    2. Counting sort (frequency array indexed by value).
       Time: O(n + k) where k is the max value in `changed`.
       Space: O(k)
"""

from collections import defaultdict
from typing import List


# Method 1: Sorting + Hashmap keep track of occurrence of original.
# Time: O(n log n), Space: O(n)
def findOriginalArray(changed: List[int]) -> List[int]:
    # It can't be a doubled array if the size is odd
    if len(changed) % 2:
        return []

    # Sort in ascending order
    changed.sort()
    freq = defaultdict(int)
    # Store the frequency in the map
    for num in changed:
        freq[num] += 1

    original: List[int] = []
    for num in changed:
        # If element exists
        if freq[num]:
            freq[num] -= 1
            twice_num = num * 2
            if freq[twice_num] > 0:
                # Pair up the elements, decrement the count
                freq[twice_num] -= 1
                # Add the original number to answer
                original.append(num)
            else:
                return []

    return original


# Method 2: Counting sort
# Time: O(n + k) where k is the maximum number in changed.
# Space: O(k)
def findOriginalArrayCountingSort(changed: List[int]) -> List[int]:
    # It can't be a doubled array if the size is odd
    if len(changed) % 2:
        return []

    max_num = 0
    # Find the max element in the array
    for num in changed:
        max_num = max(max_num, num)

    freq = [0] * (2 * max_num + 1)
    # Store the frequency in the map
    for num in changed:
        freq[num] += 1

    original: List[int] = []
    num = 0
    while num <= max_num:
        # If element exists
        if freq[num]:
            freq[num] -= 1

            twice_num = num * 2
            if freq[twice_num] > 0:
                # Pair up the elements, decrement the count
                freq[twice_num] -= 1
                # Add the original number to answer
                original.append(num)
                # Re-check the same num (mirrors C++ num-- inside for-loop)
                num -= 1
            else:
                return []
        num += 1

    return original
