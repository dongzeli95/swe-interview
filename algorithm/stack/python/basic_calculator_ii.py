"""
Basic Calculator II
https://leetcode.com/problems/basic-calculator-ii/

Given a string s which represents an expression, evaluate this expression
and return its value. Integer division truncates toward zero.

Approaches:
    1. calculate  - Stack-based evaluation. Time: O(n), Space: O(n).
    2. calculate2 - Running result with two accumulators. Time: O(n), Space: O(1).
"""


# Time: O(n), Space: O(n)
def calculate(s: str) -> int:
    res = 0
    num = 0
    n = len(s)

    op = '+'
    st = []
    for i in range(n):
        c = s[i]
        if '0' <= c <= '9':
            num = num * 10 + (ord(c) - ord('0'))
        if i == n - 1 or (c < '0' and c != ' '):
            if op == '+':
                st.append(num)
            elif op == '-':
                st.append(-num)
            else:
                top = st.pop()
                if op == '*':
                    tmp = top * num
                else:
                    # Truncate toward zero (C++ integer division semantics)
                    tmp = int(top / num)
                st.append(tmp)
            op = c
            num = 0

    while st:
        res += st.pop()

    return res


# Time: O(n), Space: O(1)
def calculate2(s: str) -> int:
    res = 0
    cur_res = 0
    num = 0
    n = len(s)
    op = '+'
    for i in range(n):
        c = s[i]
        if '0' <= c <= '9':
            num = num * 10 + ord(c) - ord('0')
        if c in ('+', '-', '*', '/') or i == n - 1:
            if op == '+':
                cur_res += num
            elif op == '-':
                cur_res -= num
            elif op == '*':
                cur_res *= num
            elif op == '/':
                # Truncate toward zero (C++ integer division semantics)
                cur_res = int(cur_res / num)
            if c in ('+', '-') or i == n - 1:
                res += cur_res
                cur_res = 0
            op = c
            num = 0
    return res


if __name__ == "__main__":
    print(calculate2("3+2*2"))      # 7
    print(calculate2(" 3/2 "))      # 1
    print(calculate2(" 3+5 / 2"))   # 5
    print(calculate2("1-1+1"))      # 1
