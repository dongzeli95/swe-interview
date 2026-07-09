// https://leetcode.com/problems/greatest-common-divisor-of-strings

/*
For two strings s and t, we say "t divides s" if and only if s = t + ... + t (i.e., t is concatenated with itself one or more times).
Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.

Ex1:
Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"

Ex2:
Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"

Ex3:
Input: str1 = "LEET", str2 = "CODE"
Output: ""

*/

#include <string>
#include <cassert>
#include <iostream>

using namespace std;

// Time complexity: O(min(m, n)*(m+n)), Space complexity: O(min(m, n))
bool validGCD(string str1, string base) {
    int m = str1.size();
    int d = base.size();

    if (m % d != 0) {
        return false;
    }

    string output = "";
    for (int i = 0; i < m/d; i++) {
        output += base;
    }

    return output == str1;
}

string gcdOfStrings(string str1, string str2) {
    int m = str1.size();
    int n = str2.size();

    string minStr = m < n ? str1 : str2;
    for (int i = min(m, n); i > 0; i--) {
        string base = minStr.substr(0, i);
        if (validGCD(str2, base) && validGCD(str1, base)) {
            return base;
        }
    }

    return "";
}

// 奇技淫巧
/*
Intuition: If str1 + str2 != str2 + str1, there is no solution.

Regarding the largest string x, why gcd of str1 and str2 size is the answer?

Consider str1 = "ABCABCABC" and str2 = "ABCABC". The lengths are 9 and 6, respectively. The GCD is 3, which corresponds to the "ABC" substring that, when repeated, can form both str1 and str2.
Let's see some other examples:
For str1 = "ABABAB" and str2 = "ABAB", the lengths are 6 and 4, respectively. The GCD is 2, which corresponds to the "AB" substring.

Proof of Correctness:
Let str1 have length m and be represented as m * x (repeated x, m times). Similarly, let str2 have length n and be n * x (repeated x, n times).
If m > n, then the GCD(m, n) must divide both m and n. Therefore, we can form a string z of length GCD(m, n) that divides both m and n, and this will be the greatest such string.
For example, let G = gcd(m, n), then m = G * k1 and n = G * k2 for some integers k1 and k2. It implies str1 can be represented as (x[0:G] * k1) and str2 can be represented as (x[0:G] * k2). Hence x[0:G] is the largest common divisor string.
*/

// Time complexity: O(m+n), Space complexity: O(m+n)
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a%b);
}

string gcdOfStringsWithMath(string str1, string str2) {
    if (str1 + str2 != str2 + str1) {
        return "";
    }

    return str1.substr(0, gcd(str1.size(), str2.size()));
}

int main() {
    string str1 = "ABCABC";
    string str2 = "ABC";
    assert(gcdOfStrings(str1, str2) == "ABC");
    assert(gcdOfStringsWithMath(str1, str2) == "ABC");

    str1 = "ABABAB";
    str2 = "ABAB";
    assert(gcdOfStrings(str1, str2) == "AB");
    assert(gcdOfStringsWithMath(str1, str2) == "AB");

    str1 = "LEET";
    str2 = "CODE";
    assert(gcdOfStrings(str1, str2) == "");
    assert(gcdOfStringsWithMath(str1, str2) == "");

    str1 = "TAUXXTAUXXTAUXXTAUXXTAUXX";
    str2 = "TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX";
    assert(gcdOfStrings(str1, str2) == "TAUXX");
    assert(gcdOfStringsWithMath(str1, str2) == "TAUXX");

    return 0;
}