```cpp
// https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length

/*
Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.
Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.

Ex1:
Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowel letters.

Ex2:
Input: s = "aeiou", k = 2
Output: 2
Explanation: Any substring of length 2 contains 2 vowels.

Ex3:
Input: s = "leetcode", k = 3
Output: 2
Explanation: "lee", "eet" and "ode" contain 2 vowels.

*/

#include <string>
#include <iostream>
#include <cassert>

using namespace std;

bool isVowel(char c) {
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
}

// Time complexity: O(n), Space complexity: O(1)
int maxVowels(string s, int k) {
    if (s.empty()) {
        return 0;
    }

    int n = s.size();
    int l = 0, r = 0;
    int res = 0;
    int cnt = 0;

    while (r < n) {
        if (isVowel(s[r])) {
            cnt++;
            res = max(res, cnt);
        }

        if (r-l+1 == k) {
            if (isVowel(s[l])) {
                cnt--;
            }
            l++;
        }

        r++;
    }

    return res;
}

int main() {
    assert(maxVowels("abciiidef", 3) == 3);
    assert(maxVowels("aeiou", 2) == 2);
    assert(maxVowels("leetcode", 3) == 2);
}```
