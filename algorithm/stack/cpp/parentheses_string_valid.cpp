// https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid/description/

/*
A parentheses string is a non-empty string consisting only of '(' and ')'. 
It is valid if any of the following conditions is true:

It is ().
It can be written as AB (A concatenated with B), where A and B are valid parentheses strings.
It can be written as (A), where A is a valid parentheses string.
You are given a parentheses string s and a string locked, both of length n. 
locked is a binary string consisting only of '0's and '1's. For each index i of locked,

If locked[i] is '1', you cannot change s[i].
But if locked[i] is '0', you can change s[i] to either '(' or ')'.
Return true if you can make s a valid parentheses string. Otherwise, return false.

Ex1:
Input: s = "))()))", locked = "010100"
Output: true
Explanation: locked[1] == '1' and locked[3] == '1', so we cannot change s[1] or s[3].
We change s[0] and s[4] to '(' while leaving s[2] and s[5] unchanged to make s valid.

Ex2:
Input: s = "()()", locked = "0000"
Output: true
Explanation: We do not need to make any changes because s is already valid.

Ex3:
Input: s = ")", locked = "0"
Output: false
Explanation: locked permits us to change s[0].
Changing s[0] to either '(' or ')' will not make s valid.

*/

#include <vector>
#include <string>

using namespace std;

// Time: (n), Space: O(n)
// Intuition: 
// 1. We can use unlocked position to offset any parantheses that's invalid on the fly.
// 2. After iterating through all the parantheses, we are left with only extra left parantheses
//    which can be offset by extra star positions.
bool canBeValid(string s, string locked) {
    int n = s.size();

    vector<int> stars;
    vector<int> ss;
    for (int i = 0; i < n; i++) {
        if (locked[i] == '0') {
            stars.push_back(i);
        } else {
            if (s[i] == '(') {
                ss.push_back(i);
            } else {
                if (!ss.empty() && s[ss.back()] == '(') {
                    ss.pop_back();
                } else if (!stars.empty()) {
                    stars.pop_back();
                } else {
                    return false;
                }
            }
        }
    }

    while (!stars.empty() && !ss.empty() && ss.back() < stars.back()) {
        stars.pop_back();
        ss.pop_back();
    }

    return ss.empty() && (stars.size() % 2 == 0);
}

// Method 2
// Intuition:
// 1. Check from left to right to make sure no orphan ')'
// 2. Check from right to left to make sure no orphan '('
// Time: O(n), Space: O(1)
bool check(string s, string locked, char op) {
    int count = 0;
    int stars = 0;
    int n = s.size();
    for (int i = 0; i < n; i++) {
        if (locked[i] == '0') {
            stars++;
            continue;
        }
        // )
        if (s[i] == op) {
            if (count > 0) {
                count--;
            }
            else if (stars > 0) {
                stars--;
            }
            else {
                return false;
            }
        }
        else {
            count++;
        }
    }

    if (count > stars) return false;
    stars -= count;
    return stars % 2 == 0;
}

bool canBeValid(string s, string locked) {
    if (!check(s, locked, ')')) {
        return false;
    }
    reverse(s.begin(), s.end());
    reverse(locked.begin(), locked.end());
    return check(s, locked, '(');
}



