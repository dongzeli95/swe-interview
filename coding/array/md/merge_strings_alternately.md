```cpp
// Merge Strings Alternately.
// https://leetcode.com/problems/merge-strings-alternately

// You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. If a string is longer than the other, append the additional letters onto the end of the merged string.

// Return the merged string.

// Ex1: 
// Input: word1 = "abc", word2 = "pqr"
// Output: "apbqcr"
// Explanation: The merged string will be merged as so:
// word1:  a   b   c
// word2:    p   q   r
// merged: a p b q c r

// Ex2:
// Input: word1 = "ab", word2 = "pqrs"
// Output: "apbqrs"
// Explanation: Notice that as word2 is longer, "rs" is appended to the end.
// word1:  a   b 
// word2:    p   q   r   s
// merged: a p b q   r   s

// Ex3:
// Input: word1 = "abcd", word2 = "pq"
// Output: "apbqcd"
// Explanation: Notice that as word1 is longer, "cd" is appended to the end.
// word1:  a   b   c   d
// word2:    p   q 
// merged: a p b q c   d

#include <string>
#include <iostream>
#include <cassert>
using namespace std;

// Time complexity: O(m+n)
// Space complexity: O(1)
string mergeAlternately(string word1, string word2) {
    if (word1.empty() || word2.empty()) {
        return word1 + word2;
    }

    int i = 0, j = 0;
    int m = word1.size(), n = word2.size();

    string res = "";
    while (i < m && j < n) {
        res += word1[i++];
        res += word2[j++];
    }

    while (i < m) {
        res += word1[i++];
    }

    while (j < n) {
        res += word2[j++];
    }

    return res;
}


int main() {
    assert(mergeAlternately("abc", "pqr") == "apbqcr");
    assert(mergeAlternately("ab", "pqrs") == "apbqrs");
    assert(mergeAlternately("abcd", "pq") == "apbqcd");

    return 0;
}```
