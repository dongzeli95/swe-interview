// https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/

/*
A parentheses string is valid if and only if:

It is the empty string,
It can be written as AB (A concatenated with B), where A and B are valid strings, or
It can be written as (A), where A is a valid string.
You are given a parentheses string s. In one move, you can insert a parenthesis at any position of the string.

For example, if s = "()))", you can insert an opening parenthesis to be "(()))" or a closing parenthesis to be "())))".
Return the minimum number of moves required to make s valid.

Ex1:
Input: s = "())"
Output: 1

Ex2:
Input: s = "((("
Output: 3

*/

// (())())

// )))(((

// right: 0, left: 0

#include <string>
#include <iostream>

using namespace std;

// Time: O(N), Space: O(N)
int minAddToMakeValid(string s) {
    if (s.empty()) {
        return 0;
    }

    string st;
    int n = s.size();
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            st.push_back(s[i]);
        } else {
            if (!st.empty() && st.back() == '(') {
                st.pop_back();
            } else {
                st.push_back(s[i]);
            }
        }
    }

    return st.size();
}

// Time: O(N), Space: O(1)
int minAddToMakeValid2(string s) {
    if (s.empty()) {
        return 0;
    }

    int left = 0, right = 0;
    int n = s.size();
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            left++;
        }
        else {
            if (left > 0) {
                left--;
            } else {
                right++;
            }
        }
    }

    return left+right;
}

int main() {
    cout << minAddToMakeValid2("())") << endl; // 1
    cout << minAddToMakeValid2("(((") << endl; // 3
    cout << minAddToMakeValid2(")))(((") << endl; // 6
    return 0;
}