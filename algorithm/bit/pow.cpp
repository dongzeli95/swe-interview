// https://leetcode.com/problems/powx-n/

/*

Implement pow(x, n), which calculates x raised to the power n (i.e., xn).

Ex1:
Input: x = 2.00000, n = 10
Output: 1024.00000

Ex2:
Input: x = 2.10000, n = 3
Output: 9.26100

Ex3:
Input: x = 2.00000, n = -2
Output: 0.25000
Explanation: 2-2 = 1/22 = 1/4 = 0.25

*/

#include <cassert>
#include <iostream>
#include <unordered_map>

using namespace std;

// 1010

// 2+8 = x^2*x^8 = x^2*x^4*x^4 = x^2

unordered_map<int, double> m;

// Time: O(logn), Space: O(logn)
double powHelper(double x, int n) {
    if (n == 0) {
        return 1.0;
    }

    if (m.count(n)) {
        return m[n];
    }

    double half = powHelper(x, n/2);
    double res = n % 2 == 0 ? half * half : half * half * x;

    m[n] = res;
    return res;
}

double pow(double x, int n) {
    if (x == 1) return 1;
    long long exp = n;
    return n < 0 ? 1.0 / powHelper(x, -exp) : powHelper(x, exp);
}

int main() {
    cout << pow(2.00000, 10) << endl; // 1024
    cout << pow(2.10000, 3) << endl; // 9.261
    cout << pow(2.00000, -2) << endl; // 0.25

    cout << pow(1.00000, -2147483648) << endl;
    return 0;
}