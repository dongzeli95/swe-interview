\n```python\n
# https://leetcode.com/problems/evaluate-reverse-polish-notation/

# You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

# Evaluate the expression. Return an integer that represents the value of the expression.

# Note that:

# The valid operators are '+', '-', '*', and '/'.
# Each operand may be an integer or another expression.
# The division between two integers always truncates toward zero.
# There will not be any division by zero.
# The input represents a valid arithmetic expression in a reverse polish notation.
# The answer and all the intermediate calculations can be represented in a 32-bit integer.


# Ex1:
# Input: tokens = ["2","1","+","3","*"]
# Output: 9
# Explanation: ((2 + 1) * 3) = 9

# Ex2:
# Input: tokens = ["4","13","5","/","+"]
# Output: 6
# Explanation: (4 + (13 / 5)) = 6

# Ex3:
# Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
# Output: 22
# Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
# = ((10 * (6 / (12 * -11))) + 17) + 5
# = ((10 * (6 / -132)) + 17) + 5
# = ((10 * 0) + 17) + 5
# = (0 + 17) + 5
# = 17 + 5
# = 22

from collections import deque

def isOperator(str):
    return str == '+' or str == '-' or str == '*' or str == '/'

def evalRPN(tokens):
    if len(tokens) == 0:
        return 0

    st = deque()
    for t in tokens:
        if isOperator(t) == False:
            st.append(int(t))
            continue

        n2 = st.pop()
        n1 = st.pop()
        if t == '+':
            st.append(n1+n2)
        elif t == '-':
            st.append(n1-n2)
        elif t == '*':
            st.append(n1*n2)
        elif t == '/':
            st.append(int(n1/n2))

    return st.pop()
        


def main():
    tokens = ["2","1","+","3","*"]
    assert evalRPN(tokens) == 9

    tokens = ["4","13","5","/","+"]
    assert evalRPN(tokens) == 6

    tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
    assert evalRPN(tokens) == 22

if __name__ == "__main__":
    main()```
