// https://leetcode.com/problems/find-the-highest-altitude

/*
There is a biker going on a road trip. The road trip consists of n + 1 points at different altitudes. The biker starts his trip on point 0 with altitude equal 0.
You are given an integer array gain of length n where gain[i] is the net gain in altitude between points i​​​​​​ and i + 1 for all (0 <= i < n). Return the highest altitude of a point.

Ex1:
Input: gain = [-5,1,5,0,-7]
Output: 1
Explanation: The altitudes are [0,-5,-4,1,1,-6]. The highest is 1.

Ex2:
Input: gain = [-4,-3,-2,-1,4,3,2]
Output: 0
Explanation: The altitudes are [0,-4,-7,-9,-10,-6,-3,-1]. The highest is 0.
*/

#include <vector>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(1)
int largestAltitude(vector<int>& gain) {
    int res = 0;
    int sum = 0;
    int n = gain.size();

    for (int i = 0; i < n; i++) {
        sum += gain[i];
        res = max(res, sum);
    }

    return res;
}

int main() {
    vector<int> gain1 = {-5,1,5,0,-7};
    assert(largestAltitude(gain1) == 1);

    vector<int> gain2 = {-4,-3,-2,-1,4,3,2};
    assert(largestAltitude(gain2) == 0);

    return 0;
}