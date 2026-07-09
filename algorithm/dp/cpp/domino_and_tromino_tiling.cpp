// https://leetcode.com/problems/domino-and-tromino-tiling

/* 

You have two types of tiles: a 2 x 1 domino shape and a tromino shape. You may rotate these shapes.
Given an integer n, return the number of ways to tile an 2 x n board. Since the answer may be very large, return it modulo 109 + 7.
In a tiling, every square must be covered by a tile. 
Two tilings are different if and only if there are two 4-directionally adjacent cells on the board such that exactly one of the tilings has both squares occupied by a tile.

*/

// dp[1] = 1, dp[2] = 2, dp[3] = 5, dp[4] = dp[3] + dp[2] + 2 * dp[1] = 11 because we can put 2 trominoes in the middle of dp[3] and dp[2] and 2 dominoes in the middle of dp[2] and dp[1]

// dp[3] = dp[2] + dp[1] + 2 * dp[0]

// We can determine the number of ways to fully or partially tile a board of width kkk by considering every possible way to arrive at f(k)f(k)f(k) or p(k)p(k)p(k) by placing a domino or a tromino.Let's find f(k)f(k)f(k) together and then you can pause to practice by finding p(k)p(k)p(k) on your own. All of the ways to arrive at a fully tiled board of width kkk are as follows:

// From f(k−1)f(k - 1)f(k−1) we can add 1 vertical domino for each tiling in a fully covered board with a width of k−1k - 1k−1, as shown in the second animation.
// From f(k−2)f(k - 2)f(k−2) we can add 2 horizontal dominos for each tiling in a fully covered board with a width of k−2k - 2k−2, as shown in the third animation.
// Note that we don't need to add 2 vertical dominos to f(k−2)f(k-2)f(k−2), since f(k−1)f(k-1)f(k−1) will cover that case and it will cause duplicates if we count it again.
// From p(k−1)p(k - 1)p(k−1) we can add an L - shaped tromino for each tiling in a partially covered board with a width of k−1k - 1k−1, as shown above(in the fourth animation).
// We will multiply by p(k−1)p(k - 1)p(k−1) by 2 because for any partially covered tiling, there will be a horizontally symmetrical tiling of it.For example, the animation below shows two p(k−1)p(k - 1)p(k−1) board states that are identical when reflected over the horizontal edge of the board.Logically, there must be an equal number of ways to fully tile the board from both p(k−1)p(k - 1)p(k−1) states.So rather than count the number of ways twice, we simply multiply the number of ways from one p(k−1)p(k - 1)p(k−1) state by 2.
// Summing the ways to reach f(k)f(k)f(k) gives us the following equation :

// f(k) = f(k−1) + f(k−2) + 2∗p(k−1)f(k) = f(k - 1) + f(k - 2) + 2 * p(k - 1)f(k) = f(k−1) + f(k−2) + 2∗p(k−1)

// f[1] = 1, f[2] = 2
// p[1] = 0, p[2] = 1, p[3] = f[2] + p[1] = 2, p[4] = f[3] + p[2] + f[2] = 7

// Adding a tromino to a fully covered board of width k−2k-2k−2 (i.e. f(k−2)f(k-2)f(k−2))
// Adding a horizontal domino to a partially covered board of width k−1k - 1k−1(i.e.p(k−1)p(k - 1)p(k−1))
// Thus, we arrive at the following conclusion for p(k)p(k)p(k) :

// p(k) = p(k−1) + f(k−2)p(k) = p(k - 1) + f(k - 2)p(k) = p(k−1) + f(k−2)

#include <vector>
#include <cassert>

using namespace std;

// Time complexity: O(n), Space complexity: O(n)
int numTilings(int n) {
    if (n <= 2) {
        return n;
    }

    int MOD = 1e9 + 7;
    vector<long long> f(n + 1, 0);
    vector<long long> p(n + 1, 0);

    f[0] = 1;
    f[1] = 1;
    f[2] = 2;
    p[0] = 0;
    p[1] = 0;
    p[2] = 1;

    for (int i = 3; i <= n; ++i) {
        f[i] = (f[i - 1] + f[i - 2] + 2 * p[i - 1]) % MOD;
        p[i] = (p[i - 1] + f[i - 2]) % MOD;
    }

    return f[n];
}

int main() {
    assert(numTilings(3) == 5);
    assert(numTilings(4) == 11);
    assert(numTilings(5) == 24);
    assert(numTilings(30) == 312342182);
    return 0;
}