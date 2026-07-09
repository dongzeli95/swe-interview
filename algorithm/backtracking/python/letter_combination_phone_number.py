"""
Letter Combinations of a Phone Number
https://leetcode.com/problems/letter-combinations-of-a-phone-number

Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent.

Approaches:
    1. letter_combination (DFS / backtracking)
       Time: O(4^n), Space: O(n) call stack (result excluded).
    2. letter_combination_bfs (BFS / iterative build-up)
       Time: O(4^n), Space: O(4^n).
"""

from typing import List


mapping = {
    '2': "abc",
    '3': "def",
    '4': "ghi",
    '5': "jkl",
    '6': "mno",
    '7': "pqrs",
    '8': "tuv",
    '9': "wxyz",
}


def _dfs(idx: int, digits: str, res: List[str], curr: List[str]) -> None:
    if idx == len(digits):
        res.append("".join(curr))
        return

    for c in mapping[digits[idx]]:
        curr.append(c)
        _dfs(idx + 1, digits, res, curr)
        curr.pop()


# Method 1: DFS
# Time: O(4^n), Space: O(n), where n = len(digits)
# We have up to 4 letters for each digit, and we have n digits.
# Space: O(n) because of the call stack.
# The result list space if counted, is O(4^n).
def letter_combination(digits: str) -> List[str]:
    if not digits:
        return []

    res: List[str] = []
    _dfs(0, digits, res, [])
    return res


# Method 2: BFS
# Time: O(4^n), Space: O(4^n)
def letter_combination_bfs(digits: str) -> List[str]:
    if not digits:
        return []

    res: List[str] = [""]

    for digit in digits:
        temp: List[str] = []
        for s in res:
            for c in mapping[digit]:
                temp.append(s + c)
        res = temp

    return res


if __name__ == "__main__":
    res = letter_combination("23")
    expected = ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert res == expected
    res = letter_combination_bfs("23")
    assert res == expected

    res = letter_combination("")
    expected = []
    assert res == expected
    res = letter_combination_bfs("")
    assert res == expected

    res = letter_combination("2")
    expected = ["a", "b", "c"]
    assert res == expected
    res = letter_combination_bfs("2")
    assert res == expected
