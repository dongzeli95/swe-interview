```cpp
// You are given two strings s1 and s2 of equal length.
// A string swap is an operation where you choose two indices in a string
// (not necessarily different) and swap the characters at these indices.

// Return true if it is possible to make both strings equal 
// by performing at most one string swap on exactly one of the strings.Otherwise, return false.

// Ex1:
// Input: s1 = "bank", s2 = "kanb"
// Output : true
// Explanation : For example, swap the first character with the last character of s2 to make "bank".

// Ex2:
// Input : s1 = "attack", s2 = "defend"
// Output : false
// Explanation : It is impossible to make them equal with one string swap.

// Ex3:
// Input : s1 = "kelb", s2 = "kelb"
// Output : true
// Explanation : The two strings are already equal, so no string swap operation is required.

#include <string>
#include <iostream>

using namespace std;

bool areAlmostEqual(string a, string b) {
    if (a.size() != b.size()) {
        return false;
    }

    vector<int> freq(26, 0);
    for (int i = 0; i < a.size(); i++) {
        freq[a[i] - 'a']++;
    }

    for (int i = 0; i < b.size(); i++) {
        freq[b[i] - 'a']--;
    }

    for (int i = 0; i < 26; i++) {
        if (freq[i] != 0) return false;
    }

    int diff = 0;
    for (int i = 0; i < a.size(); i++) {
        if (a[i] != b[i]) {
            diff++;
        }
    }
    return diff == 0 || diff == 2;
}

// You are given two strings of the same length s and t.
// In one step you can choose any character of t and replace it with another character.
// Return the minimum number of steps to make t an anagram of s.
// An Anagram of a string is a string that contains the same characters with a different(or the same) ordering.

// Ex1:
// Input: s = "bab", t = "aba"
// Output : 1
// Explanation : Replace the first 'a' in t with b, t = "bba" which is anagram of s.

// Ex2:
// Input : s = "leetcode", t = "practice"
// Output : 5
// Explanation : Replace 'p', 'r', 'a', 'i' and 'c' from t with proper characters to make t anagram of s.

// Ex3:
// Input : s = "anagram", t = "mangaar"
// Output : 0
// Explanation : "anagram" and "mangaar" are anagrams.

int minSteps(string s, string t) {
    int res = 0;
    unordered_map<char, int> charCnt;
    for (char c : s) ++charCnt[c];
    for (char c : t) --charCnt[c];
    for (auto a : charCnt) {
        // cout << a.first << " " << a.second << endl;
        if (a.second > 0) res += abs(a.second);
    }
    return res;
}

int main() {
    cout << minSteps("leetcode", "practice") << endl;
    return 0;
}```
