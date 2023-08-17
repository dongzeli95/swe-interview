```cpp
// https://leetcode.com/problems/is-subsequence

/* 
Given two strings s and t, return true if s is a subsequence of t, or false otherwise.
A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. 
(i.e., "ace" is a subsequence of "abcde" while "aec" is not).

Ex1:
Input: s = "abc", t = "ahbgdc"
Output: true

Ex2:
Input: s = "axc", t = "ahbgdc"
Output: false

*/

#include <string>
#include <cassert>

using namespace std;

// Time complexity: O(n), Space complexity: O(1)
// n is minimum of s.size() and t.size()
bool isSubsequence(string s, string t) {
    if (s.empty()) {
        return true;
    }

    int m = s.size(), n = t.size();
    int i = 0, j = 0;

    while (i < m && j < n) {
        if (s[i] == t[j]) {
            i++;
        }

        j++;
    }

    return i == m;
}

int main() {
    assert(isSubsequence("abc", "ahbgdc") == true);
    assert(isSubsequence("axc", "ahbgdc") == false);
}
```
