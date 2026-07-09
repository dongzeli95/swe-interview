// https://leetcode.com/problems/trapping-rain-water

/*
Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it can trap after raining.

Ex1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. 
In this case, 6 units of rain water (blue section) are being trapped.

Ex2:
Input: height = [4,2,0,3,2,5]
Output: 9

*/

#include <vector>
#include <stack>

using namespace std;

// Intuition: track the highest bar to its left and highest bar to its right at every position.
// Time: O(n)
// Space: O(n)
int trap(vector<int>& height) {
    int n = height.size();
    vector<int> left(n, 0);
    vector<int> right(n, 0);
    int mx = height[0];
    for (int i = 0; i < n; i++) {
        mx = max(mx, height[i]);
        left[i] = mx;
    }

    mx = height[n - 1];
    for (int i = n - 1; i >= 0; i--) {
        mx = max(mx, height[i]);
        right[i] = mx;
    }

    int res = 0;
    for (int i = 0; i < n; i++) {
        res += min(left[i], right[i]) - height[i];
    }

    return res;
}

int trap(vector<int>& height) {
    stack<int> st;
    int i = 0, res = 0, n = height.size();
    while (i < n) {
        if (st.empty() || height[i] <= height[st.top()]) {
            st.push(i++);
        }
        else {
            int t = st.top(); st.pop();
            if (st.empty()) continue;
            res += (min(height[i], height[st.top()]) - height[t]) * (i - st.top() - 1);
        }
    }
    return res;
}