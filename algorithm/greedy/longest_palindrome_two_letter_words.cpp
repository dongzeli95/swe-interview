// https://leetcode.com/problems/longest-palindrome-by-concatenating-two-letter-words/description/

/*
You are given an array of strings words. 
Each element of words consists of two lowercase English letters.
Create the longest possible palindrome by selecting some elements from words and concatenating them in any order. 
Each element can be selected at most once.
Return the length of the longest palindrome that you can create. 
If it is impossible to create any palindrome, return 0.
A palindrome is a string that reads the same forward and backward.

Ex1:
Input: words = ["lc","cl","gg"]
Output: 6
Explanation: One longest palindrome is "lc" + "gg" + "cl" = "lcggcl", of length 6.
Note that "clgglc" is another longest palindrome that can be created.

Ex2:
Input: words = ["ab","ty","yt","lc","cl","ab"]
Output: 8
Explanation: One longest palindrome is "ty" + "lc" + "cl" + "yt" = "tylcclyt", of length 8.
Note that "lcyttycl" is another longest palindrome that can be created.

Ex3:
Input: words = ["cc","ll","xx"]
Output: 2
Explanation: One longest palindrome is "cc", of length 2.
Note that "ll" is another longest palindrome that can be created, and so is "xx".

*/

#include <string>

using namespace std;

bool isIdentical(string& str) {
    return str[0] == str[1];
}

string reverseWord(string& str) {
    string res = "";
    res.push_back(str[1]);
    res.push_back(str[0]);
    return res;
}

// Time: O(n), Space: O(n)
// Intuition: We need to find pairs of words to put on either side of the string.
// We can also put odd numbers of idential words in the middle of the palindrome string.
int longestPalindrome(vector<string>& words) {
    unordered_map<string, int> reversed;
    unordered_map<string, int> identical;

    int n = words.size();
    int res = 0;
    for (int i = 0; i < n; i++) {
        string rev = reverseWord(words[i]);
        if (reversed.count(rev) && reversed[rev] > 0) {
            res += 4;
            reversed[rev]--;
            if (isIdentical(words[i])) {
                identical[words[i]]--;
            }
        }
        else {
            reversed[words[i]]++;
            if (isIdentical(words[i])) {
                identical[words[i]]++;
            }
        }
    }

    int mx = 0;
    for (auto i : identical) {
        mx = max(mx, i.second);
    }

    res += mx * 2;
    return res;
}