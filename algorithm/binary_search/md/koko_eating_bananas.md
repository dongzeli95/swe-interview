```cpp
// https://leetcode.com/problems/koko-eating-bananas

/*
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. 
Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Ex1:
Input: piles = [3,6,7,11], h = 8
Output: 4

Ex2:
Input: piles = [30,11,23,4,20], h = 5
Output: 30

Ex3:
Input: piles = [30,11,23,4,20], h = 6
Output: 23

*/

// min speed: 1, max speed: max(piles)
// 27 hr -> 4 hrs

// 1, 11 -> 6
// 1, 1, 2, 2 = 6
// 1, 6 -> 1 + (6-1)/2 = 3
// 1, 2, 3, 4 = 10
// 4, 6 -> 5
// 1, 2, 2, 3 = 8

// 4, 5 -> 4

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

int getHours(vector<int>& piles, int speed) {
    int n = piles.size();

    int res = 0;
    for (int i = 0; i < n; i++) {
        res += piles[i] / speed;
        if (piles[i] % speed != 0) {
            res++;
        }
    }

    return res;
}

// Time: O(nlog(m)) where m is the max element in piles, Space: O(1)
int minEatingSpeed(vector<int>& piles, int h) {
    if (piles.empty()) {
        return 0;
    }

    int n = piles.size();
    int minSpeed = 1;
    int maxSpeed = piles[0];

    for (int i = 1; i < n; i++) {
        maxSpeed = max(maxSpeed, piles[i]);
    }

    while (minSpeed < maxSpeed) {
        int mid = minSpeed + (maxSpeed - minSpeed) / 2;
        int hours = getHours(piles, mid);
        if (hours > h) {
            minSpeed = mid+1;
        } else {
            maxSpeed = mid;
        }
    }

    return maxSpeed;
}

int main() {
    vector<int> piles = {3, 6, 7, 11};
    int h = 8;
    int res = minEatingSpeed(piles, h);
    assert(res == 4);

    piles = {30, 11, 23, 4, 20};
    h = 5;
    res = minEatingSpeed(piles, h);
    assert(res == 30);

    piles = {30, 11, 23, 4, 20};
    h = 6;
    res = minEatingSpeed(piles, h);
    assert(res == 23);

    piles = {312884470};
    h = 968709470;
    res = minEatingSpeed(piles, h);
    assert(res == 1);
}```
