// https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/

/*
Given a string s of '(' , ')' and lowercase English characters.

Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting parentheses string is valid and return any valid string.

Formally, a parentheses string is valid if and only if:

It is the empty string, contains only lowercase characters, or
It can be written as AB (A concatenated with B), where A and B are valid strings, or
It can be written as (A), where A is a valid string.

Ex1:
Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"
Explanation: "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.

Ex2:
Input: s = "a)b(c)d"
Output: "ab(c)d"

Ex3:
Input: s = "))(("
Output: ""
Explanation: An empty string is also valid.
*/

#include <string>
#include <stack>
#include <iostream>

using namespace std;

string minRemoveToMakeValid(string s) {
    if (s.empty()) {
        return "";
    }

    stack<int> st;
    int n = s.size();
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            st.push(i);
        } else if (s[i] == ')') {
            if (!st.empty() && s[st.top()] == '(') {
                st.pop();
            } else {
                st.push(i);
            }
        }
    }

    string res;
    for (int i = n-1; i >= 0; i--) {
        if (!st.empty() && i == st.top()) {
            st.pop();
            continue;
        }
        res.push_back(s[i]);
    }

    reverse(res.begin(), res.end());
    return res;
}

string minRemoveToMakeValidWithoutStack(string s) {
    string res;
    int left = 0, right = 0;
    for (char c : s) {
        if (c == ')') ++right;
    }
    for (char c : s) {
        if (c == '(') {
            if (left == right) continue;
            ++left;
        }
        else if (c == ')') {
            --right;
            if (left == 0) continue;
            --left;
        }
        res += c;
    }
    return res;
}

int main() {
    cout << minRemoveToMakeValid("lee(t(c)o)de)") << endl;
    cout << minRemoveToMakeValid("a)b(c)d") << endl;
    cout << minRemoveToMakeValid("))((") << endl;

    return 0;
}