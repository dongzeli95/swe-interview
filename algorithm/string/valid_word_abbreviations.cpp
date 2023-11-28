// https://leetcode.com/problems/valid-word-abbreviation/

/*
A string can be abbreviated by replacing any number of non-adjacent, non-empty substrings with their lengths. 
The lengths should not have leading zeros.

For example, a string such as "substitution" could be abbreviated as (but not limited to):

"s10n" ("s ubstitutio n")
"sub4u4" ("sub stit u tion")
"12" ("substitution")
"su3i1u2on" ("su bst i t u ti on")
"substitution" (no substrings replaced)
The following are not valid abbreviations:

"s55n" ("s ubsti tutio n", the replaced substrings are adjacent)
"s010n" (has leading zeros)
"s0ubstitution" (replaces an empty substring)
Given a string word and an abbreviation abbr, return whether the string matches the given abbreviation.

A substring is a contiguous non-empty sequence of characters within a string.

Ex1:
Input: word = "internationalization", abbr = "i12iz4n"
Output: true
Explanation: The word "internationalization" can be abbreviated as "i12iz4n" ("i nternational iz atio n").

Ex2:
Input: word = "apple", abbr = "a2e"
Output: false
Explanation: The word "apple" cannot be abbreviated as "a2e".

*/

#include <string>
#include <iostream>

using namespace std;

bool isnum(char c) {
    return c >= '0' && c <= '9';
}

bool isValid(string abbreviation, string word) {
    int m = word.size();
    int n = abbreviation.size();
    // cout << "m: " << m << " n:" << n << endl;
    if (n > m) {
        return false;
    }

    int i = 0;
    int j = 0;
    while (i < n) {
        if (j >= m) {
            return false;
        }

        // cout << "abbreviation: " << string(abbreviation[i], 1) << endl;

        if (isnum(abbreviation[i])) {
            // cout << "i: " << i << endl;
            if (abbreviation[i] == '0') {
                return false;
            }

            int idx = i+1;
            while (idx < n && isnum(abbreviation[idx])) {
                idx++;
            }

            // cout << word.substr(i, num) << endl;
            int num = stoi(abbreviation.substr(i, idx-i));
            // cout << "num: " << num << endl;
            i = idx;
            j += num;
        }

        if ((i >= n && j < m) || (i < n && j >= m)) {
            return false;
        }

        if (j < m && i < n && word[j] != abbreviation[i]) {
            return false;
        }

        i++;
        j++;
    }

    return true;
}

int main() {

    // "s10n" ("s ubstitutio n")
    //     "sub4u4" ("sub stit u tion")
    //     "12" ("substitution")
    //     "su3i1u2on" ("su bst i t u ti on")
    //     "substitution" (no substrings replaced)
    //     The following are not valid abbreviations :

    // "s55n" ("s ubsti tutio n", the replaced substrings are adjacent)
    //     "s010n" (has leading zeros)
    //     "s0ubstitution" (replaces an empty substring)
    cout << isValid("s10n", "substitution") << endl; // 1
    cout << isValid("12", "substitution") << endl; // 1
    cout << isValid("sub4u4", "substitution") << endl; // 1
    cout << isValid("su3i1u2on", "substitution") << endl; // 1
    cout << isValid("substitution", "substitution") << endl; // 1

    cout << isValid("s55n", "substitution") << endl; // 0
    cout << isValid("s010n", "substitution") << endl; // 0
    cout << isValid("s0ubstitution", "substitution") << endl; // 0

    // Input: word = "internationalization", abbr = "i12iz4n"
    cout << isValid("i12iz4n", "internationalization") << endl; // 1
    // Input: word = "apple", abbr = "a2e"
    cout << isValid("a2e", "apple") << endl; // 0
    return 0;
}