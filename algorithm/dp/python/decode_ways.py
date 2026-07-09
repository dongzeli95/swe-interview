"""
Decode Ways
https://leetcode.com/problems/decode-ways/

A message containing letters from A-Z can be encoded into numbers using the
mapping 'A' -> "1", ..., 'Z' -> "26". Given a string of digits, return the
number of ways to decode it.

Approaches:
    1. numOfDecodes                - Bottom-up DP with a length-(n+1) table.  Time O(n), Space O(n).
    2. numOfDecodesConstantMemory  - Bottom-up DP rolling two variables.       Time O(n), Space O(1).
"""


# Time: O(n), Space: O(n)
def numOfDecodes(s: str) -> int:
    if not s:
        return 0

    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for j in range(1, 27):
            curr = str(j)
            length = len(curr)
            if i - length >= 0 and s[i - length:i] == curr:
                dp[i] += dp[i - length]

    return dp[n]


# Time: O(n), Space: O(1)
def numOfDecodesConstantMemory(s: str) -> int:
    if not s:
        return 0

    n = len(s)
    prev2, prev1 = 0, 1

    for i in range(1, n + 1):
        num_of_ways = 0
        for j in range(1, 27):
            curr = str(j)
            length = len(curr)
            if i - length >= 0 and s[i - length:i] == curr:
                num_of_ways += prev2 if length == 2 else prev1

        prev2 = prev1
        prev1 = num_of_ways

    return prev1


if __name__ == "__main__":
    # test
    # assert numOfDecodes("12") == 2
    # assert numOfDecodes("226") == 3
    # assert numOfDecodes("06") == 0

    assert numOfDecodesConstantMemory("12") == 2
    assert numOfDecodesConstantMemory("226") == 3
    assert numOfDecodesConstantMemory("06") == 0
