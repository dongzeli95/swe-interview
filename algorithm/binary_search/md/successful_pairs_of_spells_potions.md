```cpp
// https://leetcode.com/problems/successful-pairs-of-spells-and-potions

/* 
You are given two positive integer arrays spells and potions, of length n and m respectively,
where spells[i] represents the strength of the ith spell and potions[j] represents the strength of the jth potion.
You are also given an integer success. A spell and potion pair is considered successful if the product of their strengths is at least success.
Return an integer array pairs of length n where pairs[i] is the number of potions that will form a successful pair with the ith spell.

Ex1:
Input: spells = [5,1,3], potions = [1,2,3,4,5], success = 7
Output: [4,0,3]
Explanation:
- 0th spell: 5 * [1,2,3,4,5] = [5,10,15,20,25]. 4 pairs are successful.
- 1st spell: 1 * [1,2,3,4,5] = [1,2,3,4,5]. 0 pairs are successful.
- 2nd spell: 3 * [1,2,3,4,5] = [3,6,9,12,15]. 3 pairs are successful.
Thus, [4,0,3] is returned.

Ex2:
Input: spells = [3,1,2], potions = [8,5,8], success = 16
Output: [2,0,2]
Explanation:
- 0th spell: 3 * [8,5,8] = [24,15,24]. 2 pairs are successful.
- 1st spell: 1 * [8,5,8] = [8,5,8]. 0 pairs are successful.
- 2nd spell: 2 * [8,5,8] = [16,10,16]. 2 pairs are successful.
Thus, [2,0,2] is returned.

*/

// nlogn, mlogn
// mlogm, nlogm

#include <vector>
#include <iostream>
#include <cassert>
#include <algorithm>

using namespace std;

// Time: O(nlogm), Space: O(1), where n = spells.size(), m = potions.size()
// Large number overflow.
vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
    if (spells.empty() || potions.empty()) {
        return {};
    }

    int n = spells.size();
    int m = potions.size();

    sort(potions.begin(), potions.end());

    vector<int> res(n, 0);
    for (int i = 0; i < n; i++) {

        int l = 0;
        int r = m-1;
        int idx = -1;
        // Find the index of the first element that is greater than or equal to success / spells[i].
        while (l <= r) {
            int mid = l + (r-l) / 2;
            long long product = spells[i] * potions[mid];
            if (product < success) {
                l = mid+1;
            } else {
                idx = mid;
                r = mid-1;
            }
        }

        res[i] = (idx == -1) ? 0 : m-idx;
    }

    return res;
}

// TODO: How to fix the overflow problem?
// TOOD: Time: O(m+n), Space: O(1), https://leetcode.com/problems/successful-pairs-of-spells-and-potions/solutions/3370088/c-prefix-sum-o-m-n-time-o-1-space/?envType=study-plan-v2&envId=leetcode-75

int main() {
    vector<int> spells = {5,1,3};
    vector<int> potions = {1,2,3,4,5};
    vector<int> res = successfulPairs(spells, potions, 7);
    vector<int> expected = {4,0,3};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }

    spells = {3,1,2};
    potions = {8,5,8};
    res = successfulPairs(spells, potions, 16);
    expected = {2,0,2};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }

    spells = {1, 2, 3, 4, 5, 6, 7};
    potions = {1, 2, 3, 4, 5, 6, 7};
    res = successfulPairs(spells, potions, 25);
    expected = {0, 0, 0, 1, 3, 3, 4};
    for (int i = 0; i < res.size(); i++) {
        assert(res[i] == expected[i]);
    }


}```
