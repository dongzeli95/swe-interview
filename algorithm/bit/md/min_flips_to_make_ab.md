```cpp
// Min flips to make the string a followed by b.
// We only have 'a', 'b' in the input string.
// Ex1:
// Input: "abba", Output: 1
// Ex2:
// Input: "bbaaa", Output: 2

// Time: O(n), Space: O(1)

#include <iostream>
#include <string>
#include <cassert>

using namespace std;

// 00000, 00001, 00011, 00111, 01111, 11111
// 0, 1, 3, 7, 15, 31

int convertStrToBit(string str) {
    int res = 0;
    for (int i = 0; i < str.size(); i++) {
        res = res*2 + (str[i] == 'a' ? 0 : 1);
    }

    return res;
}

int calculateFlips(int num) {
    int res = 0;
    while (num > 0) {
        res += num & 1;
        num = num >> 1;
    }

    return res;
}

int minFlip(string str) {
    int n = str.size();
    int res = n;

    int target = convertStrToBit(str);
    int mask = 1;
    int curr = 0;
    for (int i = 0; i < n+1; i++) {
        int flips = calculateFlips(curr ^ target);
        res = min(res, flips);
        curr = curr | mask;
        mask = mask << 1;
    }

    return res;
}

int main() {
    string str1 = "abba";
    assert(minFlip(str1) == 1);

    string str2 = "bbaaa";
    // cout << minFlip(str2) << endl;
    assert(minFlip(str2) == 2);

    string str3 = "abbaaabababaaa";
    assert(minFlip(str3) == 5);

    return 0;
}```
