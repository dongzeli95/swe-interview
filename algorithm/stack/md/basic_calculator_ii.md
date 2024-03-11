```cpp
// https://leetcode.com/problems/basic-calculator-ii/

/*
Given a string s which represents an expression, evaluate this expression and return its value.
The integer division should truncate toward zero.
You may assume that the given expression is always valid. All intermediate results will be in the range of [-231, 231 - 1].
Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

Ex1:
Input: s = "3+2*2"
Output: 7

Ex2:
Input: s = " 3/2 "
Output: 1

Ex3:
Input: s = " 3+5 / 2 "
Output: 5
*/

// 3+5 / 2 *4 -2

// [3,+,]
#include <vector>
#include <stack>
#include <string>
#include <iostream>

using namespace std;

// Time: O(n), Space: O(n)
int calculate(string s) {
    int res = 0;
    int num = 0;
    int n = s.size();

    char op = '+';
    stack<int> st;
    for (int i = 0; i < n; i++) {
        if (s[i] >= '0' && s[i] <= '9') {
            num = num * 10 + (s[i] - '0');
        }
        if (i == n-1 || (s[i] < '0' && s[i] != ' ')){
            if (op == '+') st.push(num);
            else if (op == '-') st.push(-num);
            else {
                int tmp = (op == '*') ? st.top() * num : st.top() / num;
                // cout << "st top: " << st.top() << " num: " << num << endl;
                st.pop();
                st.push(tmp);
            }
            op = s[i];
            num = 0;
        }
    }

    while (!st.empty()) {
        cout << "top: " << st.top() << endl;
        res += st.top();
        st.pop();
    }

    return res;
}

// Time: O(n), Space: O(1)
int calculate2(string s) {
    long res = 0, curRes = 0, num = 0, n = s.size();
    char op = '+';
    for (int i = 0; i < n; ++i) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + c - '0';
        }
        if (c == '+' || c == '-' || c == '*' || c == '/' || i == n - 1) {
            switch (op) {
            case '+': curRes += num; break;
            case '-': curRes -= num; break;
            case '*': curRes *= num; break;
            case '/': curRes /= num; break;
            }
            if (c == '+' || c == '-' || i == n - 1) {
                res += curRes;
                curRes = 0;
            }
            op = c;
            num = 0;
        }
    }
    return res;
}

int main() {
    cout << calculate2("3+2*2") << endl; // 7
    cout << calculate2(" 3/2 ") << endl; // 1
    cout << calculate2(" 3+5 / 2") << endl; // 5
    cout << calculate2("1-1+1") << endl; // 1
    return 0;
}```
