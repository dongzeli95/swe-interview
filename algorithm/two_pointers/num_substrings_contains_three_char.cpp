// https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/

/*
Given a string s consisting only of characters a, b and c.
Return the number of substrings containing at least one occurrence of all these characters a, b and c.

Ex1:
Input: s = "abcabc"
Output: 10
Explanation: The substrings containing at least one occurrence of the characters a, b and c are 
"abc", "abca", "abcab", "abcabc", "bca", "bcab", "bcabc", "cab", "cabc" and "abc" (again).

Ex2:
Input: s = "aaacb"
Output: 3
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "aaacb", "aacb" and "acb".

Ex3:
Input: s = "abc"
Output: 1

*/

#include <string>
#include <vector>
#include <iostream>

using namespace std;

// Time: O(n), Space: O(1)
int numberOfSubstrings(string s) {
    if (s.empty()) {
        return 0;
    }

    vector<int> char_map(3, 1);
    int n = s.size();

    int left = 0, right = 0;
    int match = 0;
    int res = 0;
    while (right < n) {
        if (--char_map[s[right]-'a'] == 0) {
            match++;
        }
        
        while (left < n && match == 3) {
            res += (n-right);
            if (char_map[s[left]-'a']++ == 0) {
                match--;
            }
            left++;
        }

        right++;
    }

    return res;
}

// abcabc
// left: 0, right: 0, match = 1
// left: 0, right: 1, match = 2
// left: 0, right: 2, match = 3

int main() {
    string s = "abcabc";
    cout << numberOfSubstrings(s) << endl;

    s = "aaacb";
    cout << numberOfSubstrings(s) << endl;

    s = "abc";
    cout << numberOfSubstrings(s) << endl;

    return 0;
}