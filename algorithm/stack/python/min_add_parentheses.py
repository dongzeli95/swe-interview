"""
Minimum Add to Make Parentheses Valid
https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/

Approaches:
    1. minAddToMakeValid  - Stack-based scan. Time: O(N), Space: O(N).
    2. minAddToMakeValid2 - Two counters (left/right) without a stack. Time: O(N), Space: O(1).
"""


# Time: O(N), Space: O(N)
def minAddToMakeValid(s: str) -> int:
    if not s:
        return 0

    st = []
    for ch in s:
        if ch == '(':
            st.append(ch)
        else:
            if st and st[-1] == '(':
                st.pop()
            else:
                st.append(ch)

    return len(st)


# Time: O(N), Space: O(1)
def minAddToMakeValid2(s: str) -> int:
    if not s:
        return 0

    left, right = 0, 0
    for ch in s:
        if ch == '(':
            left += 1
        else:
            if left > 0:
                left -= 1
            else:
                right += 1

    return left + right


if __name__ == "__main__":
    print(minAddToMakeValid2("()"))       # 0
    print(minAddToMakeValid2("())"))      # 1
    print(minAddToMakeValid2("((("))      # 3
    print(minAddToMakeValid2(")))((("))   # 6
