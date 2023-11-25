```cpp
// https://leetcode.com/problems/buildings-with-an-ocean-view/

/*
There are n buildings in a line. 
You are given an integer array heights of size n that represents the heights of the buildings in the line.

The ocean is to the right of the buildings. 
A building has an ocean view if the building can see the ocean without obstructions. 
Formally, a building has an ocean view if all the buildings to its right have a smaller height.

Return a list of indices (0-indexed) of buildings that have an ocean view, sorted in increasing order.

Ex1:
Input: heights = [4,2,3,1]
Output: [0,2,3]
Explanation: Building 1 (0-indexed) does not have an ocean view because building 2 is taller.

Ex2:
Input: heights = [4,3,2,1]
Output: [0,1,2,3]
Explanation: All the buildings have an ocean view.

Ex3:
Input: heights = [1,3,2,4]
Output: [3]
Explanation: Only building 3 has an ocean view.

*/

#include <vector>
#include <iostream>

using namespace std;

vector<int> findBuildings(vector<int>& heights) {
    if (heights.empty()) {
        return {};
    }

    vector<int> res;
    int n = heights.size();
    for (int i = 0; i < n; i++) {
        while (!res.empty() && heights[i] >= heights[res.back()]) {
            res.pop_back();
        }

        res.push_back(i);
    }

    return res;
}

int main() {
    vector<int> h1 = {4, 2, 3, 1};
    vector<int> res1 = findBuildings(h1);
    for (int i : res1) cout << i << " ";
    cout << endl;

    vector<int> h2 = { 4, 3, 2, 1 };
    vector<int> res2 = findBuildings(h2);
    for (int i : res2) cout << i << " ";
    cout << endl;

    vector<int> h3 = { 1, 3, 2, 4};
    vector<int> res3 = findBuildings(h3);
    for (int i : res3) cout << i << " ";
    cout << endl;

    return 0;
}```
