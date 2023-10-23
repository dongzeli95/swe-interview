```cpp
// https://leetcode.com/problems/container-with-most-water/

/* 
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
Find two lines that together with the x-axis form a container, such that the container contains the most water.
Return the maximum amount of water a container can store.
Notice that you may not slant the container.

Ex1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

Ex2:
Input: height = [1,1]
Output: 1

*/

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(1)
int maxArea(vector<int>& height) {
    if (height.empty()) {
        return 0;
    }

    int l = 0;
    int r = height.size() - 1;

    int res = 0;
    while (l < r) {
        res = max(res, min(height[l], height[r]) * (r - l));
        if (height[l] <= height[r]) {
            l++;
        } else {
            r--;
        }
    }

    return res;
}

int main() {
    vector<int> height {1,8,6,2,5,4,8,3,7};
    assert(maxArea(height) == 49);

    height = {1,1};
    assert(maxArea(height) == 1);

    return 0;
}```
