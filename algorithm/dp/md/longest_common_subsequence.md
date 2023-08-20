```cpp
// https://leetcode.com/problems/longest-common-subsequence

/*
Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".
A common subsequence of two strings is a subsequence that is common to both strings.

Ex1:
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.

Ex2:
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

Ex3:
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.

*/

// dp[i][j] means longest common subsequence of text1[0..i-1] and text2[0..j-1]
// dp[i][j] = max(1 + dp[i-1][j-1], if text1[i-1] == text2[j-1], dp[i-1][j], dp[i][j-1])

#include <string>
#include <vector>
#include <cassert>
#include <iostream>

using namespace std;

//    a b c
//   00 0 0
// a 01 1 1
// b 01 2 2
// c 01 2 3

int longestCommonSubsequence(string s, string t) {
    if (s.empty() || t.empty()) {
        return 0;
    }

    int m = s.size(), n = t.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    dp[0][0] = 0;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]);

            if (s[i-1] == t[j-1]) {
                dp[i][j] = max(dp[i][j], 1+dp[i-1][j-1]);
            }
        }
    }

    return dp[m][n];
}

int main() {
    // cout << longestCommonSubsequence("abcde", "ace") << endl;
    assert(longestCommonSubsequence("abcde", "ace") == 3);
    assert(longestCommonSubsequence("abc", "abc") == 3);
    assert(longestCommonSubsequence("abc", "def") == 0);
}```
