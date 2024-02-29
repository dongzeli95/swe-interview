```cpp
// https://leetcode.com/problems/reverse-words-in-a-string-ii/description/

/*
Given a character array s, reverse the order of the words.
A word is defined as a sequence of non-space characters. 
The words in s will be separated by a single space.
Your code must solve the problem in-place, i.e. without allocating extra space.

Ex1:
Input: s = ["t","h","e"," ","s","k","y"," ","i","s"," ","b","l","u","e"]
Output: ["b","l","u","e"," ","i","s"," ","s","k","y"," ","t","h","e"]

Ex2:
Input: s = ["a"]
Output: ["a"]

*/

#include <vector>

using namespace std;

// Time: O(n), Space: O(1)
void reverseWords(vector<char>& s) {
    reverse(s.begin(), s.end());

    // 'start' points to the beginning of the current word
    // 'end' points to the position just after the current word
    int start = 0, end = 0;
    int n = s.size();

    while (start < n) {

        // Move 'right' to the position just after the current word
        while (end < n && s[end] != ' ')
            end++;

        // Note: in C++, reverse() operates on [start, end)
        // In other words, the leftmost element is included, while the rightmost element is not
        reverse(s.begin() + start, s.begin() + end);

        // Move 'start' and 'end' to the beginning of the next word
        end++;
        start = end;
    }
}```
