// https://leetcode.com/problems/valid-palindrome-ii/

/*
Given a string s, return true if the s can be palindrome after deleting at most one character from it.

Example 1:

Input: s = "aba"
Output: true
Example 2:

Input: s = "abca"
Output: true
Explanation: You could delete the character 'c'.
Example 3:

Input: s = "abc"
Output: false

*/

#include <string>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(1)
bool isValid(string s, int left, int right) {
    while (left < right) {
        if (s[left] != s[right]) return false;
        left++, right--;
    }

    return true;
}

bool validPalindrome(string s) {
    if (s.empty()) {
        return true;
    }

    int l = 0, r = s.size()-1;
    while (l < r) {
        if (s[l] != s[r]) {
            return isValid(s, l+1, r) || isValid(s, l, r-1);
        }
        l++, r--;
    }

    return true;
}

bool helper(string s, bool modified) {
    if (s.empty()) return true;
    int l = 0, r = s.size() - 1;
    while (l < r) {
        if (s[l] != s[r]) {
            string s1 = s.substr(0, l) + s.substr(l + 1);
            string s2 = s.substr(0, r) + s.substr(r + 1);
            return !modified && (helper(s1, true) || helper(s2, true));
        }
        l++;
        r--;
    }

    return true;
}
// cbbcc
// bool validPalindrome(string s) {
//     return helper(s, false);
// }

int main() {
    assert(validPalindrome("aba"));
    assert(validPalindrome("abca"));
    assert(!validPalindrome("abc"));
    assert(validPalindrome("cbbcc"));

    return 0;
}