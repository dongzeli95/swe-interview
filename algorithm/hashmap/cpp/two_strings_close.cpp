// https://leetcode.com/problems/determine-if-two-strings-are-close

/*
Two strings are considered close if you can attain one from the other using the following operations:

Operation 1: Swap any two existing characters.
For example, abcde -> aecdb
Operation 2: Transform every occurrence of one existing character into another existing character, and do the same with the other character.
For example, aacabb -> bbcbaa (all a's turn into b's, and all b's turn into a's)
You can use the operations on either string as many times as necessary.

Given two strings, word1 and word2, return true if word1 and word2 are close, and false otherwise.

Ex1:
Input: word1 = "abc", word2 = "bca"
Output: true
Explanation: You can attain word2 from word1 in 2 operations.
Apply Operation 1: "abc" -> "acb"
Apply Operation 1: "acb" -> "bca"

Ex2:
Input: word1 = "a", word2 = "aa"
Output: false
Explanation: It is impossible to attain word2 from word1, or vice versa, in any number of operations.

Ex3:
Input: word1 = "cabbba", word2 = "abbccc"
Output: true
Explanation: You can attain word2 from word1 in 3 operations.
Apply Operation 1: "cabbba" -> "caabbb"
Apply Operation 2: "caabbb" -> "baaccc"
Apply Operation 2: "baaccc" -> "abbccc"

*/

#include <string>
#include <unordered_map>
#include <vector>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(1)
// TODO: bit operation method
bool closeStrings(string word1, string word2) {
    if (word1.size() != word2.size()) {
        return false;
    }

    vector<int> m1(26, 0);
    vector<int> m2(26, 0);

    int n = word1.size();
    for (int i = 0; i < n; i++) {
        m1[word1[i]-'a']++;
        m2[word2[i]-'a']++;
    }

    for (int i = 0; i < 26; i++) {
        if (m1[i] != 0 && m2[i] == 0) return false;
        if (m2[i] != 0 && m1[i] == 0) return false;
    }

    sort(m1.begin(), m1.end());
    sort(m2.begin(), m2.end());

    for (int i = 0; i < 26; i++) {
        if (m1[i] != m2[i]) return false;
    }

    return true;
}

int main() {
    assert(closeStrings("abc", "bca") == true);
    assert(closeStrings("a", "aa") == false);
    assert(closeStrings("cabbba", "abbccc") == true);

    // a: 2, b: 3, c: 1
    // a: 1, b: 2, c: 3

    return 0;
}