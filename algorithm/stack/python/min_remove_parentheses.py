"""
Minimum Remove to Make Valid Parentheses
https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/

Given a string s of '(', ')' and lowercase English characters, remove the
minimum number of parentheses so that the resulting string is valid.

Approaches:
1. minRemoveToMakeValid: stack of indices to mark invalid parens.
   Time O(n), Space O(n).
2. minRemoveToMakeValidWithoutStack: two-pass counting of '(' vs ')'.
   Time O(n), Space O(1) extra (excluding output).
"""


def minRemoveToMakeValid(s: str) -> str:
    if not s:
        return ""

    st = []
    n = len(s)
    for i in range(n):
        if s[i] == '(':
            st.append(i)
        elif s[i] == ')':
            if st and s[st[-1]] == '(':
                st.pop()
            else:
                st.append(i)

    res = []
    for i in range(n - 1, -1, -1):
        if st and i == st[-1]:
            st.pop()
            continue
        res.append(s[i])

    res.reverse()
    return "".join(res)


def minRemoveToMakeValidWithoutStack(s: str) -> str:
    res = []
    left, right = 0, 0
    for c in s:
        if c == ')':
            right += 1
    for c in s:
        if c == '(':
            if left == right:
                continue
            left += 1
        elif c == ')':
            right -= 1
            if left == 0:
                continue
            left -= 1
        res.append(c)
    return "".join(res)


if __name__ == "__main__":
    print(minRemoveToMakeValid("lee(t(c)o)de)"))
    print(minRemoveToMakeValid("a)b(c)d"))
    print(minRemoveToMakeValid("))(("))
