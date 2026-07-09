"""
Minimum Time to Finish the Race
https://leetcode.com/problems/minimum-time-to-finish-the-race/description/

Approaches:
1. minimumFinishTime: DP with tire-usage precomputation, then combine sub-laps.
   - First, for each tire compute the minimum time to run i consecutive laps
     without changing (amortized constant per tire, since we break once a
     change becomes cheaper than continuing).
   - Then combine: dp[i] = min(dp[i-j] + changeTime + dp[j]) for 1 <= j < i.
   - Time: O(max(numLaps^2, tires)), Space: O(numLaps).
"""

from typing import List
import sys


# Intuition:
# We compute for all laps without changing tires.
# And then we break laps in the middle and try to find minimum by changing tires.
#
# dp[i] = minimum time to run i laps
# dp[i] = min(dp[i-j] + changeTime + dp[j]), 1 <= j <= i
#
# Time: O(max(numLaps^2, tires)), Space: O(numLaps)
def minimumFinishTime(tires: List[List[int]], changeTime: int, numLaps: int) -> int:
    dp = [sys.maxsize] * (numLaps + 1)

    for j in range(len(tires)):
        f = tires[j][0]
        r = tires[j][1]
        curr_r = 1
        lapseTime = 0
        dp[0] = 0

        # This is amortized constant time complexity
        for i in range(1, numLaps + 1):
            lapseTime += f * curr_r
            dp[i] = min(dp[i], lapseTime)
            if lapseTime > f + changeTime:
                break
            curr_r *= r

    for i in range(1, numLaps + 1):
        for j in range(1, i):
            dp[i] = min(dp[i], dp[i - j] + changeTime + dp[j])

    return dp[numLaps]
