```cpp
// Given an input string(s) and a pattern(p), implement wildcard pattern matching with support for '?' and '*' where:

// '?' Matches any single character.
// '*' Matches any sequence of characters(including the empty sequence).
// The matching should cover the entire input string(not partial).



// Example 1:

// Input: s = "aa", p = "a"
// Output : false
// Explanation : "a" does not match the entire string "aa".
// Example 2 :

//     Input : s = "aa", p = "*"
//     Output : true
//     Explanation : '*' matches any sequence.
//     Example 3 :

//     Input : s = "cb", p = "?a"
//     Output : false
//     Explanation : '?' matches 'c', but the second letter is 'a', which does not match 'b'.

#include <string>
#include <vector>
#include <iostream>

using namespace std;

bool isMatch(string s, string p) {
    int m = s.size(), n = p.size();
    vector<vector<bool>> dp(m + 1, vector<bool>(n + 1));
    dp[0][0] = true;
    for (int i = 1; i <= n; ++i) {
        if (p[i - 1] == '*') dp[0][i] = dp[0][i - 1];
    }
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (p[j - 1] == '*') {
                dp[i][j] = dp[i - 1][j] || dp[i][j - 1];
            }
            else {
                dp[i][j] = (s[i - 1] == p[j - 1] || p[j - 1] == '?') && dp[i - 1][j - 1];
            }
        }
    }
    return dp[m][n];
}

vector<int> findMatchIndices(string s, string p) {
    int m = s.size(), n = p.size();
    // dp[i][j] will store the starting index of the match if s[0..i) matches p[0..j), else -1
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, -1));
    dp[0][0] = 0;  // Empty string matches with empty pattern
    for (int i = 1; i <= n; ++i) {
        if (p[i - 1] == '*') dp[0][i] = 0;
    }
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (p[j - 1] == '*') {
                if (dp[i - 1][j] != -1 || dp[i][j - 1] != -1) {
                    dp[i][j] = (dp[i - 1][j] != -1) ? dp[i - 1][j] : dp[i][j - 1];
                }
            }
            else if (s[i - 1] == p[j - 1] || p[j - 1] == '?') {
                if (dp[i - 1][j - 1] != -1) {
                    dp[i][j] = dp[i - 1][j - 1];
                }
            }
        }
    }

    // Collecting all start indices of matches
    vector<int> matchIndices;
    for (int i = 1; i <= m; ++i) {
        if (dp[i][n] != -1) {
            matchIndices.push_back(dp[i][n]);
        }
    }
    return matchIndices;
}

int main () {
    vector<int> res = findMatchIndices("aa", "a");
    for (int i = 0; i < res.size(); i++) {
        cout << res[i] << endl;
    }

    return 0;
}```
