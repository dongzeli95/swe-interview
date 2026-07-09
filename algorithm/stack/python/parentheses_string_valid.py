"""
Check if a Parentheses String Can Be Valid
https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid/

Given a parentheses string s and a binary string locked of the same length n.
For each index i, if locked[i] == '1' the character s[i] is fixed; if '0' we may
change s[i] to '(' or ')'. Return True iff s can be made a valid parentheses
string.

Approaches:
    1. canBeValid            — Stack-based tracking of '(' positions and unlocked
                               ("star") positions. Time O(n), Space O(n).
    2. canBeValid2 / check   — Two-pass counting: sweep left-to-right ensuring no
                               orphan ')', then right-to-left ensuring no orphan
                               '('. Time O(n), Space O(1).
"""

from typing import List


# Approach 1
# Time: O(n), Space: O(n)
# Intuition:
# 1. We can use unlocked positions to offset any parenthesis that's invalid on the fly.
# 2. After iterating through all parentheses, we are left with only extra left
#    parentheses which can be offset by extra star positions to their right.
def canBeValid(s: str, locked: str) -> bool:
    n = len(s)

    stars: List[int] = []
    ss: List[int] = []
    for i in range(n):
        if locked[i] == '0':
            stars.append(i)
        else:
            if s[i] == '(':
                ss.append(i)
            else:
                if ss and s[ss[-1]] == '(':
                    ss.pop()
                elif stars:
                    stars.pop()
                else:
                    return False

    while stars and ss and ss[-1] < stars[-1]:
        stars.pop()
        ss.pop()

    return not ss and (len(stars) % 2 == 0)


# Approach 2
# Intuition:
# 1. Check from left to right to make sure no orphan ')'.
# 2. Check from right to left to make sure no orphan '('.
# Time: O(n), Space: O(1)
def check(s: str, locked: str, op: str) -> bool:
    count = 0
    stars = 0
    n = len(s)
    for i in range(n):
        if locked[i] == '0':
            stars += 1
            continue
        # op is the "closing" character in the current sweep direction
        if s[i] == op:
            if count > 0:
                count -= 1
            elif stars > 0:
                stars -= 1
            else:
                return False
        else:
            count += 1

    if count > stars:
        return False
    stars -= count
    return stars % 2 == 0


def canBeValid2(s: str, locked: str) -> bool:
    if not check(s, locked, ')'):
        return False
    s = s[::-1]
    locked = locked[::-1]
    return check(s, locked, '(')
