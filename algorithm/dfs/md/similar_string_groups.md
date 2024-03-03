```cpp
// https://leetcode.com/problems/similar-string-groups/description/

/*
Two strings, X and Y, are considered similar if either they are identical or we can make them equivalent 
by swapping at most two letters (in distinct positions) within the string X.

For example, "tars" and "rats" are similar (swapping at positions 0 and 2), 
and "rats" and "arts" are similar, but "star" is not similar to "tars", "rats", or "arts".

Together, these form two connected groups by similarity: {"tars", "rats", "arts"} and {"star"}.  
Notice that "tars" and "arts" are in the same group even though they are not similar. 

Formally, each group is such that a word is in the group if and only if it is similar to at least one other word in the group.
We are given a list strs of strings where every string in strs is an anagram of every other string in strs. 
How many groups are there?

Ex1:
Input: strs = ["tars","rats","arts","star"]
Output: 2

Ex2:
Input: strs = ["omv","ovm"]
Output: 1

*/

#include <vector>
#include <unordered_set>
#include <string>

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

// Time: O(n^2*m), n^2 edges and m is string length for checking similar
// Space: O(n) for depth and visited set.
int numSimilarGroups(vector<string>& A) {
    int res = 0, n = A.size();
    unordered_set<string> visited;
    for (string str : A) {
        if (visited.count(str)) continue;
        ++res;
        helper(A, str, visited);
    }
    return res;
}
void helper(vector<string>& A, string& str, unordered_set<string>& visited) {
    if (visited.count(str)) return;
    visited.insert(str);
    for (string word : A) {
        if (isSimilar(word, str)) {
            helper(A, word, visited);
        }
    }
}
bool isSimilar(string& str1, string& str2) {
    for (int i = 0, cnt = 0; i < str1.size(); ++i) {
        if (str1[i] == str2[i]) continue;
        if (++cnt > 2) return false;
    }
    return true;
}```
