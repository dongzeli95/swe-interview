// https://leetcode.com/problems/daily-temperatures

/*
Given an array of integers temperatures represents the daily temperatures, 
return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. 
If there is no future day for which this is possible, keep answer[i] == 0 instead.

Ex1:
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]

Ex2:
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]

Ex3:
Input: temperatures = [30,60,90]
Output: [1,1,0]
*/

#include <vector>
#include <stack>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(n), Space: O(n)
//
// Although there is a while loop inside the for loop, the number of elements in the stack is at most n
// and if that's the actual case, for n-1 iterations in for loop, the while loop will be executed once.

// In other words, the stack only visit each elemtent once in all iterations of for loop.
// So the time complexity is O(n).
vector<int> dailyTemperatures(vector<int>& temp) {
    if (temp.empty()) {
        return {};
    }

    int n = temp.size();
    stack<int> st;
    st.push(0);

    vector<int> res (n, 0);

    for (int i = 1; i < n; i++) {
        while (!st.empty() && temp[i] > temp[st.top()]) {
            int curr = st.top();
            res[curr] = i-curr;
            st.pop();
        }

        st.push(i);
    }

    return res;
}

int main() {
    vector<int> temp1 = {73,74,75,71,69,72,76,73};
    vector<int> res1 = {1,1,4,2,1,1,0,0};
    for (int i = 0; i < res1.size(); i++) {
        assert(dailyTemperatures(temp1)[i] == res1[i]);
    }

    vector<int> temp2 = {30,40,50,60};
    vector<int> res2 = {1,1,1,0};
    for (int i = 0; i < res2.size(); i++) {
        assert(dailyTemperatures(temp2)[i] == res2[i]);
    }

    vector<int> temp3 = {30,60,90};
    vector<int> res3 = {1,1,0};
    assert(dailyTemperatures(temp3) == res3);

    return 0;
}