// https://leetcode.com/problems/network-delay-time/

/*
You are given a network of n nodes, labeled from 1 to n. 
You are also given times, 
a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, 
vi is the target node, and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. 
Return the minimum time it takes for all the n nodes to receive the signal. 
If it is impossible for all the n nodes to receive the signal, return -1.

Ex1:
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2

Ex2:
Input: times = [[1,2,1]], n = 2, k = 1
Output: 1

Ex3:
Input: times = [[1,2,1]], n = 2, k = 2
Output: -1
*/

#include <vector>
#include <unordered_map>
#include <queue>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(N + ELogN), Space: O(N + E)
int networkDelayTime(vector<vector<int>>& times, int n, int k) {
    if (n <= 1) return 0;
    // Construct a graph
    unordered_map<int, vector<pair<int, int>>> graph;
    unordered_map<int, int> minDist;
    int m = times.size();
    for (int i = 0; i < m; i++) {
        int s = times[i][0];
        int d = times[i][1];
        int t = times[i][2];
        graph[s].push_back({d, t});
    }

    auto cmp = [&minDist](int a, int b) {
        int aNum = INT_MAX, bNum = INT_MAX;
        if (minDist.count(a)) {
            aNum = minDist[a];
        }
        if (minDist.count(b)) {
            bNum = minDist[b];
        }

        return aNum > bNum;
    };

    priority_queue<int, vector<int>, decltype(cmp)> pq(cmp);
    pq.push(k);
    minDist[k] = 0;
    while (!pq.empty()) {
        int curr = pq.top();
        pq.pop();

        for (auto neighbor: graph[curr]) {
            int d = neighbor.first;
            int t = neighbor.second;
            // Don't even explore if the distance is the same.
            if (minDist.count(d) && minDist[curr] + t >= minDist[d]) continue;
            pq.push(d);
            minDist[d] = minDist[curr] + t;
        }
    }

    int res = 0;
    for (int i = 1; i <= n; i++) {
        if (!minDist.count(i)) {
            return -1;
        }

        res = max(res, minDist[i]);
    }

    return res;
}

int main() {
    {
        vector<vector<int>> times = {{2,1,1},{2,3,1},{3,4,1}};
        int n = 4;
        int k = 2;
        int res = networkDelayTime(times, n, k);
        assert(res == 2);
    }
    {
        vector<vector<int>> times = {{1,2,1}};
        int n = 2;
        int k = 1;
        int res = networkDelayTime(times, n, k);
        assert(res == 1);
    }
    {
        vector<vector<int>> times = {{1,2,1}};
        int n = 2;
        int k = 2;
        int res = networkDelayTime(times, n, k);
        assert(res == -1);
    }
    return 0;
}