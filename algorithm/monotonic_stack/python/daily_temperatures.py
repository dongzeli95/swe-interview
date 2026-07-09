"""
Daily Temperatures — https://leetcode.com/problems/daily-temperatures

Given an array of integers `temperatures` representing daily temperatures,
return an array `answer` such that `answer[i]` is the number of days you have
to wait after the ith day to get a warmer temperature. If there is no future
day for which this is possible, `answer[i]` stays 0.

Approaches:
    1. Monotonic decreasing stack — Time: O(n), Space: O(n).
       Although a while loop sits inside the for loop, each index is pushed
       and popped from the stack at most once across all iterations, so the
       total work is linear.
"""

from typing import List


def dailyTemperatures(temp: List[int]) -> List[int]:
    if not temp:
        return []

    n = len(temp)
    st: List[int] = [0]
    res = [0] * n

    for i in range(1, n):
        while st and temp[i] > temp[st[-1]]:
            curr = st.pop()
            res[curr] = i - curr

        st.append(i)

    return res


if __name__ == "__main__":
    temp1 = [73, 74, 75, 71, 69, 72, 76, 73]
    res1 = [1, 1, 4, 2, 1, 1, 0, 0]
    for i in range(len(res1)):
        assert dailyTemperatures(temp1)[i] == res1[i]

    temp2 = [30, 40, 50, 60]
    res2 = [1, 1, 1, 0]
    for i in range(len(res2)):
        assert dailyTemperatures(temp2)[i] == res2[i]

    temp3 = [30, 60, 90]
    res3 = [1, 1, 0]
    assert dailyTemperatures(temp3) == res3
