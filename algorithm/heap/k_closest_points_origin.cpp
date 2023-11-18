// https://leetcode.com/problems/k-closest-points-to-origin/

/*
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, 
return the k closest points to the origin (0, 0).
The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).
You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

Ex1:
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].

Ex2:
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.

*/

#include <vector>
#include <iostream>
#include <cassert>
#include <queue>

using namespace std;

double calc(vector<int>& v){
    int diff1 = abs(v[0]);
    int diff2 = abs(v[1]);
    return sqrt(diff1*diff1 + diff2*diff2);
}

// Time: O(nlogk), Space: O(k)
vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
    if (points.empty()) {
        return {};
    }

    auto cmp = [&](vector<int>& v1, vector<int>& v2) {
        return calc(v1) < calc(v2);
    };

    priority_queue<vector<int>, vector<vector<int>>, decltype(cmp)> pq(cmp);
    for (int i = 0; i < points.size(); i++) {
        pq.push(points[i]);
        if (pq.size() > k) {
            pq.pop();
        }
    }

    vector<vector<int>> res;
    while (!pq.empty()) {
        res.push_back(pq.top());
        pq.pop();
    }

    return res;
}

// Quick Select
// Since we are expect to reduce number of elements to process by roughly half, 
// the average time complexity T(n) satisfies T(n) = O(n) + T(n/2) This solves to T(n) = O(n).
// The worst case time complexity is O(n^2) which occurs when the randomly selected pivot is the smallest
// or largest element in the current subarray. The probability of worst case reduces exponentially with length of input array.
// Time: amortized O(n), Space: O(1)
// 
int partitionPivot(vector<vector<int>>& points, int left, int right, int pivot_idx) {
    int idx = left;
    vector<int> pivot = points[pivot_idx];

    swap(points[pivot_idx], points[right]);
    for (int i = left; i < right; i++) {
        if (calc(points[i]) < calc(points[right])) {
            swap(points[idx++], points[i]);
        }
    }
    swap(points[idx], points[right]);
    return idx;
}

vector<vector<int>> kClosestWithQuickSelect(vector<vector<int>>& points, int k) {
    if (points.size() <= k) {
        return points;
    }

    int n = points.size();
    int left = 0, right = n-1;
    while (left <= right) {
        int pivot_idx = left + rand() % (right-left+1);
        int new_pivot = partitionPivot(points, left, right, pivot_idx);
        if (new_pivot == k-1) {
            return vector<vector<int>>{points.begin(), points.begin()+k};
        } else if (new_pivot > k-1) {
            right = new_pivot-1;
        } else {
            left = new_pivot+1;
        }
    }

    return {};
}

int main() {
    vector<vector<int>> points = { {1, 3}, {-2, 2} };
    vector<vector<int>> res = kClosest(points, 1);
    for (vector<int>& i : res) {
        cout << i[0] << " " << i[1] << endl;
    }
    res = kClosestWithQuickSelect(points, 1);
    for (vector<int>& i : res) {
        cout << i[0] << " " << i[1] << endl;
    }


    points = {{3, 3}, {5, -1}, {-2, 4}};
    res = kClosest(points, 2);
    for (vector<int>& i : res) {
        cout << i[0] << " " << i[1] << endl;
    }
    res = kClosestWithQuickSelect(points, 2);
    for (vector<int>& i : res) {
        cout << i[0] << " " << i[1] << endl;
    }

    vector<vector<int>> points2 {{1, 3}, {-2, 2}, {2, -2}};
    vector<vector<int>> res2 = kClosestWithQuickSelect(points2, 2);
    for (vector<int>& i : res2) {
        cout << i[0] << " " << i[1] << endl;
    }

    return 0;
}