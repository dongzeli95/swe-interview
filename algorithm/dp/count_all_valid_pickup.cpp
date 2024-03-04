


// 1 + 2 + ... n = n(n+1) / 2
// dp[i] how many valid orders there are using i number
// [P1, D1]
// [P2, D2]
// P2: 3 = 3+2+1
// D2: 3

// 6 = 5+4+3+2+1 = 15*6 = 90
// dp[i] = dp[i-1]*(2*n-1+2*n-2+..1)
// n*(n+1) / 2
// n = 2*n-1
// n(2n-1)

#include <vector>

using namespace std;

// Intuition: Whenever there are existing valid sequence, for each new pickup or delivery
// you think about the valid positions to insert them:
// 1. First insert pickups, it should have 2*(n-1)+1 number of options.
// [P1, D1]
// [P2, D2]
// -> [P2, P1, D1], [P1, P2, D1], [P1, D1, P2]

// 2. Insert delivery
// if pick up is inserted at first slot, then delivery have 2 * (n - 1) + 1 options as well.
// but if pick up is inserted at second slot, then delivery have 2 * (n - 1) options, one less slot option, because
// delivery cannot be inserted at first slot, which makes it before pickup order.

// so for each previous valid sequence, we have 2*(n-1)+1 + 2*(n-1) + ... + 1 options to insert it.
// dp[i] = dp[i-1]*(2*n-1+2*n-2+..1)
// 
// Now we need to figure out how to calculate (2*n-1+2*n-2+..1)
// We have a formula 1+2+...+n = n(n+1) / 2
// now n we have is 2*n-1, the formula becomes = (2*n-1)*2*n/2 = n(2n-1)

// Time: O(n), Space: O(N) -> O(1)
int countOrders(int n) {
    vector<long> dp(n + 1, 0);
    dp[1] = 1;

    int mod = 1e9 + 7;

    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1];
        dp[i] *= i;
        dp[i] = dp[i] % mod;
        dp[i] *= (2 * i - 1);
        dp[i] = dp[i] % mod;
    }

    return dp[n];
}