// https://leetcode.com/problems/asteroid-collision

/*

We are given an array asteroids of integers representing asteroids in a row.
For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.
Find out the state of the asteroids after all collisions. 
If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

Ex1:
Input: asteroids = [5,10,-5]
Output: [5,10]
Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.

Ex2:
Input: asteroids = [8,-8]
Output: []
Explanation: The 8 and -8 collide exploding each other.

Ex3:
Input: asteroids = [10,2,-5]
Output: [10]
Explanation: The 2 and -5 collide resulting in -5. The 10 and -5 collide resulting in 10.

*/

#include <cassert>
#include <iostream>
#include <vector>
#include <stack>

using namespace std;

// Time: O(n), Space: O(n)
vector<int> asteroidCollision(vector<int>& asteroids) {
    if (asteroids.empty()) {
        return {};
    }

    vector<int> res;
    int n = asteroids.size();
    for (int i = 0; i < n; i++) {
        if (res.empty()) {
            res.push_back(asteroids[i]);
        } else {
            bool needInsert = false;
            while (!res.empty()) {
                int d1 = res.back() > 0 ? 1 : -1;
                int d2 = asteroids[i] > 0 ? 1 : -1;
                if (d1 == 1 && d2 == -1) {
                    if (abs(res.back()) > abs(asteroids[i])) {
                        needInsert = false;
                        break;
                    }
                    if (abs(res.back()) == abs(asteroids[i])) {
                        res.pop_back();
                        needInsert = false;
                        break;
                    }

                    if (abs(res.back()) < abs(asteroids[i])) {
                        res.pop_back();
                        needInsert = true;
                    }
                } else {
                    res.push_back(asteroids[i]);
                    needInsert = false;
                    break;
                }
            }

            if (needInsert) {
                res.push_back(asteroids[i]);
            }
        }
    }

    return res;
}

int main() {
    vector<int> asteroids1 = {5,10,-5};
    vector<int> res1 = {5,10};
    assert(asteroidCollision(asteroids1) == res1);

    vector<int> asteroids2 = {8,-8};
    vector<int> res2 = {};
    assert(asteroidCollision(asteroids2) == res2);

    vector<int> asteroids3 = {10,2,-5};
    vector<int> res3 = {10};
    assert(asteroidCollision(asteroids3) == res3);

    return 0;
}