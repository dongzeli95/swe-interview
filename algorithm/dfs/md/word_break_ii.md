```cpp
// https://leetcode.com/problems/word-break-ii/

// Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid dictionary word.
// Return all such possible sentences in any order.
// Note that the same word in the dictionary may be reused multiple times in the segmentation.

// Ex1:
// Input: s = "catsanddog", wordDict = ["cat", "cats", "and", "sand", "dog"]
// Output : ["cats and dog", "cat sand dog"]

// Ex2:
// Input : s = "pineapplepenapple", wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]
// Output : ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]
// Explanation : Note that you are allowed to reuse a dictionary word.

// Ex3:
// Input : s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
// Output : []

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <iostream>
#include <cassert>

using namespace std;

// Why we need memorization?
// For example: s = "aabb", dict: ["a", "b", "aa", "bb"]
// In this case "bb" substring will be evaluated twice: once after "a a" and another one after "aa"
// For memorization helps eliminate those duplicate calculations.
// Time complexity without memorization: O(2^n)
// Time complexity with memorization: O(n^3), where n is the length of the string
// we have N^2 substring and for each substring we have to check if it is in the dictionary
// For each list of strings we have to copy it, so it is N^3

// Space: Stack: O(n), Heap: O(n^3)?
vector<string> dfsWithMemo(string& s, int idx, unordered_set<string>& dict,
    unordered_map<int, vector<string>>& cache) {
    // Base case
    if (idx == s.size()) {
        return {""};
    }

    if (cache.count(idx)) {
        return cache[idx];
    }

    int n = s.size();
    vector<string> res;
    for (int i = idx; i < n; i++) {
        string str = s.substr(idx, i - idx + 1);
        if (!dict.count(str)) continue;
        vector<string> sub = dfsWithMemo(s, i + 1, dict, cache);
        for (string i : sub) {
            string newStr = str;
            newStr += (i.empty()) ? "" : " " + i;
            res.push_back(newStr);
        }
    }

    cache[idx] = res;
    return res;
}

vector<string> wordBreak2(string s, vector<string>& dict) {
    if (s.empty()) {
        return {};
    }

    unordered_set<string> d;
    for (string s : dict) {
        d.insert(s);
    }

    unordered_map<int, vector<string>> cache;

    return dfsWithMemo(s, 0, d, cache);
}

void dfs(string& s, int idx, unordered_set<string>& dict,
        vector<vector<string>>& res,
        vector<string>& curr) {
    // Base case
    if (idx == s.size()) {
        res.push_back(curr);
        return;
    }

    int n = s.size();
    for (int i = idx; i < n; i++) {
        string str = s.substr(idx, i-idx+1);
        if (!dict.count(str)) continue;
        curr.push_back(str);
        dfs(s, i+1, dict, res, curr);
        curr.pop_back();
    }
}

vector<string> wordBreak(string s, vector<string>& dict) {
    if (s.empty()) {
        return {};
    }

    unordered_set<string> d;
    vector<vector<string>> res;
    vector<string> curr;

    for (string s : dict) {
        d.insert(s);
    }

    dfs(s, 0, d, res, curr);

    vector<string> output;
    for (vector<string>& v : res) {
        string curr = "";
        for (int i = 0; i < v.size(); i++) {
            if (!curr.empty()) curr += " ";
            curr += v[i];
        }
        output.push_back(curr);
    }
    return output;
}

int main() {
    vector<string> dict1 = {"cat", "cats", "and", "sand", "dog"};
    vector<string> res1 = {"cats and dog", "cat sand dog"};
    vector<string> output1 = wordBreak2("catsanddog", dict1);
    for (string i : output1) cout << i << endl;
    // assert(wordBreak("catsanddog", dict1) == res1);

    vector<string> dict2 = {"apple", "pen", "applepen", "pine", "pineapple"};
    vector<string> res2 = {"pine apple pen apple", "pineapple pen apple", "pine applepen apple"};
    vector<string> output2 = wordBreak2("pineapplepenapple", dict2);
    for (string i : output2) cout << i << endl;

    vector<string> dict3 = {"cats", "dog", "sand", "and", "cat"};
    vector<string> res3 = {};
    assert(wordBreak2("catsandog", dict3) == res3);

    return 0;
}```
