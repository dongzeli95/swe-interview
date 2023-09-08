```cpp
// https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c

/*

Given 3 positives numbers a, b and c. 
Return the minimum flips required in some bits of a and b to make ( a OR b == c ). (bitwise OR operation).
Flip operation consists of change any single bit 1 to 0 or change the bit 0 to 1 in their binary representation.

Ex1:
Input: a = 2, b = 6, c = 5
Output: 3
Explanation: After flips a = 1 , b = 4 , c = 5 such that (a OR b == c)

Ex2:
Input: a = 4, b = 2, c = 7
Output: 1

Ex3:
Input: a = 1, b = 2, c = 3
Output: 0

*/

// 0110
// 0101

// 1->0 (1, 2)
// 0->1 requires 1

#include <cassert>
#include <iostream>

using namespace std;

// 0 0 1 0 (2)
// 0 1 0 1 (5)
// 0 1 1 1 (7)
// 1 0 0 0 (8) 
// 1 +1+1+1

// 1 0 0 0 (8)
// 0 0 1 1 (3)
// 1 0 1 1
// 0 1 0 1 (5)

int extractBit(int num, int pos) {
    return (num & (1 << pos)) >> pos;
}

// Time: O(n), n bits.
// Space: O(1)
int minFlips(int a, int b, int c) {
    int orRes = a | b;
    if (orRes == c) return 0;

    int pos = 0;
    int res = 0;

    // We have to use max here since the largest bit can 
    // exist in both c or orRes.
    int mx = c | orRes;
    while (mx > 0) {
        int orResBit = extractBit(orRes, pos);
        int cBit = extractBit(c, pos);
        if (orResBit != cBit) {
            if (orResBit == 0) {
                res++;
            } else {
                int aBit = extractBit(a, pos);
                int bBit = extractBit(b, pos);
                res += (aBit == bBit) ? 2 : 1;
            }
        }

        mx = mx >> 1;
        pos++;
    }

    return res;
}

int main() {
    assert(minFlips(2, 6, 5) == 3);
    assert(minFlips(4, 2, 7) == 1);
    assert(minFlips(1, 2, 3) == 0);
    assert(minFlips(8, 3, 5) == 3);
    assert(minFlips(2, 5, 8) == 4);

    return 0;
}```
