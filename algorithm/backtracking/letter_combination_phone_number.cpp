// https://leetcode.com/problems/letter-combinations-of-a-phone-number

/* 
Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.
A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

Ex1:
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Ex2:
Input: digits = ""
Output: []


Ex3:
Input: digits = "2"
Output: ["a","b","c"]

*/

#include <vector>
#include <unordered_map>
#include <iostream>
#include <cassert>

using namespace std;

unordered_map<char, string> mapping {{'2', "abc"},
                                    {'3', "def"},
                                    {'4', "ghi"},
                                    {'5', "jkl"},
                                    {'6', "mno"},
                                    {'7', "pqrs"},
                                    {'8', "tuv"},
                                    {'9', "wxyz"}};

void dfs(int idx, string& digits, vector<string>& res, string curr) {
    if (idx == digits.size()) {
        res.push_back(curr);
        return;
    }

    for (char c: mapping[digits[idx]]) {
        curr.push_back(c);
        dfs(idx+1, digits, res, curr);
        curr.pop_back();
    }
}

// Method 1: DFS
// Time: O(4^n), Space: O(n), where n = digits.size()
// We have 4 letters for each digit, and we have n digits.
// Space: O(n) because of the call stack.
// The result vector space if counted, is O(4^n).
vector<string> letterCombination(string digits) {
    if (digits.empty()) {
        return {};
    }

    vector<string> res;
    dfs(0, digits, res, "");
    return res;
}

// Method 2: BFS
// Time: O(4^n), Space: O(4^n)
vector<string> letterCombinationBFS(string digits) {
    if (digits.empty()) {
        return {};
    }

    vector<string> res;
    res.push_back("");

    for (char digit: digits) {
        vector<string> temp;
        for (string s: res) {
            for (char c: mapping[digit]) {
                temp.push_back(s+c);
            }
        }
        res = temp;
    }

    return res;
}

int main() {
    vector<string> res = letterCombination("23");
    vector<string> expected = {"ad","ae","af","bd","be","bf","cd","ce","cf"};
    assert(res == expected);
    res = letterCombinationBFS("23");
    assert(res == expected);

    res = letterCombination("");
    expected = {};
    assert(res == expected);
    res = letterCombinationBFS("");
    assert(res == expected);

    res = letterCombination("2");
    expected = {"a","b","c"};
    assert(res == expected);
    res = letterCombinationBFS("2");
    assert(res == expected);
}
