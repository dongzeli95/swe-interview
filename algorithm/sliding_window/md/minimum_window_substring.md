```cpp
// https://leetcode.com/problems/minimum-window-substring/

/*
Given two strings s and t of lengths m and n respectively, return the minimum window
substring of s such that every character in t (including duplicates) is included in the window. 
If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

Ex1:
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Ex2:
Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.

Ex3:
Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.

*/

#include <string>
#include <iostream>
#include <unordered_map>

using namespace std;

// Time: O(n)
string minWindow(string s, string t) {
    if (s.empty()) {
        return "";
    }

    int m = s.size(), n = t.size();
    unordered_map<char, int> char_map;
    for (char c : t) char_map[c]++;
    int total = char_map.size();
    int left = 0, right = 0;
    int match = 0;
    string res = "";

    while (right < m) {
        if (char_map.count(s[right])) {
            char_map[s[right]]--;
            // We only count a match when num of a specific char 
            // equals between s and t.
            if (char_map[s[right]] == 0) {
                match++;
            }
        }

        while (left < m && match == total) {
            if (res.empty() || right-left+1 < res.size()) {
                res = s.substr(left, right-left+1);
            }

            if (char_map.count(s[left])) {
                // If already equal, this char is matched before.
                // We need to decrement match since we are getting rid of this char.
                if (char_map[s[left]] == 0) {
                    match--;
                }
                char_map[s[left]]++;
            }
            left++;
        }

        right++;
    }

    return res;
}

int main() {
    string s = "ADOBECODEBANC";
    string t = "ABC";
    cout << minWindow(s, t) << endl;

    s = "a";
    t = "a";
    cout << minWindow(s, t) << endl;

    s = "a";
    t = "aa";
    cout << minWindow(s, t) << endl;

    s = "bba";
    t = "ab";
    cout << minWindow(s, t) << endl;

    return 0;
}```
