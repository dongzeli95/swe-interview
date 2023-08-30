```cpp
// https://leetcode.com/problems/removing-stars-from-a-string

/*
You are given a string s, which contains stars *.
In one operation, you can:

Choose a star in s.
Remove the closest non-star character to its left, as well as remove the star itself.
Return the string after all stars have been removed.

Note:

The input will be generated such that the operation is always possible.
It can be shown that the resulting string will always be unique.

Ex1:
Input: s = "leet**cod*e"
Output: "lecoe"
Explanation: Performing the removals from left to right:
- The closest character to the 1st star is 't' in "leet**cod*e". s becomes "lee*cod*e".
- The closest character to the 2nd star is 'e' in "lee*cod*e". s becomes "lecod*e".
- The closest character to the 3rd star is 'd' in "lecod*e". s becomes "lecoe".
There are no more stars, so we return "lecoe".

Ex2:
Input: s = "erase*****"
Output: ""
Explanation: The entire string is removed, so we return an empty string.

*/

#include <cassert>
#include <string>
#include <stack>

using namespace std;

// Time: O(N), Space: O(N)
string removeStars(string s) {
    if (s.empty()) {
        return "";
    }

    string res = "";
    stack<char> st;
    int n = s.size();

    for (int i = 0; i < n; i++) {
        if (s[i] == '*' && !st.empty()) {
            st.pop();
        } else {
            st.push(s[i]);
        }
    }

    while (!st.empty()) {
        char c = st.top();
        res.push_back(c);
        st.pop();
    }

    reverse(res.begin(), res.end());
    return res;
}

int main() {
    string s1 = "leet**cod*e";
    assert(removeStars(s1) == "lecoe");

    string s2 = "erase*****";
    assert(removeStars(s2) == "");

    return 0;
}```
