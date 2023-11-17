// https://leetcode.com/problems/decode-ways/

// A message containing letters from A - Z can be encoded into numbers using the following mapping :

// 'A' -> "1"
// 'B' -> "2"
// ...
// 'Z' -> "26"
// To decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above(there may be multiple ways).
// For example, "11106" can be mapped into :

// "AAJF" with the grouping(1 1 10 6)
// "KJF" with the grouping(11 10 6)
// Note that the grouping(1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06".

// Given a string s containing only digits, return the number of ways to decode it.
// The test cases are generated so that the answer fits in a 32 - bit integer.

// Ex1:
// Input: s = "12"
// Output : 2
// Explanation : "12" could be decoded as "AB" (1 2) or "L" (12).

// Ex2:
// Input : s = "226"
// Output : 3
// Explanation : "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

// Ex3:
// Input : s = "06"
// Output : 0
// Explanation : "06" cannot be mapped to "F" because of the leading zero("6" is different from "06").

#include <vector>
#include <string>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(n)
int numOfDecodes(string s) {
    if (s.empty()) {
        return 0;
    }

    int n = s.size();
    vector<int> dp (n+1, 0);
    dp[0] = 1;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= 26; j++) {
            string curr = to_string(j);
            int len = curr.size();
            if (i-len >= 0 && s.substr(i-len, len) == curr) {
                dp[i] += dp[i-len];
            }
        }
    }

    return dp[n];
}

// Time: O(n), Space: O(1)
int numOfDecodesConstantMemory(string s) {
    if (s.empty()) {
        return 0;
    }

    int n = s.size();
    int prev2 = 0, prev1 = 1;

    for (int i = 1; i <= n; i++) {
        int numOfWays = 0;
        for (int j = 1; j <= 26; j++) {
            string curr = to_string(j);
            int len = curr.size();
            if (i - len >= 0 && s.substr(i - len, len) == curr) {
                numOfWays += (len == 2) ? prev2 : prev1;
            }
        }

        prev2 = prev1;
        prev1 = numOfWays;
    }

    return prev1;
}

int main() {
    // test 
    // assert(numOfDecodes("12") == 2);
    // assert(numOfDecodes("226") == 3);
    // assert(numOfDecodes("06") == 0);

    assert(numOfDecodesConstantMemory("12") == 2);
    assert(numOfDecodesConstantMemory("226") == 3);
    assert(numOfDecodesConstantMemory("06") == 0);

    return 0;
}