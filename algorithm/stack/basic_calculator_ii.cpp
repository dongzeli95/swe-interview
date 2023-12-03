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

int cal(int a, int b, char op) {
    if (op == '+') {
        return a+b;
    } else if (op == '-') {
        return a-b;
    } else if (op == '*') {
        return a*b;
    } else {
        return a/b;
    }
}

bool isdigit(char c) {
    return c >= '0' && c <= '9';
}

bool ismuldiv(char c) {
    return c == '*' || c == '/';
}

// Time: O(n), Space: O(n)
int calculate(string s) {
    if (s.empty()) {
        return 0;
    }

    vector<int> st;

    int n = s.size();
    int a = 0, b = 0;
    char c = '#';

    int i = 0;
    while (i < n) {
        if (s[i] == ' ') {
            i++;
            continue;
        }

        if (isdigit(s[i])) {
            string num = "";
            while (i < n && isdigit(s[i])) {
                num.push_back(s[i]);
                i++;
            }

            i--;

            if (c == '#') {
                st.push_back(stoi(num));
            } else {
                b = stoi(num);
                int res = cal(a, b, c);
                st.push_back(res);
            }
        } else if (ismuldiv(s[i])) {
            a = st.back();
            st.pop_back();
            c = s[i];
        } else {
            st.push_back(s[i]);
        }
        i++;
    }

    reverse(st.begin(), st.end());

    while (st.size() >= 3) {
        int b = st.back();
        st.pop_back();
        char c = st.back();
        st.pop_back();
        int a = st.back();
        st.pop_back();

        cout << "a: " << a << " b:" << b << endl;
        int res = cal(a, b, c);
        st.push_back(res);
    }

    return st.back();
}

int main() {
    // cout << calculate("3+2*2") << endl; // 7
    // cout << calculate(" 3/2 ") << endl; // 1
    // cout << calculate(" 3+5 / 2") << endl; // 5

    cout << calculate("1-1+1") << endl; // -1
    return 0;
}