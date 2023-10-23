// https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero

/*

There are n cities numbered from 0 to n - 1 and n - 1 roads such that there is only one way to travel between two different cities (this network form a tree). 
Last year, The ministry of transport decided to orient the roads in one direction because they are too narrow.

Roads are represented by connections where connections[i] = [ai, bi] represents a road from city ai to city bi.
This year, there will be a big event in the capital (city 0), and many people want to travel to this city.

Your task consists of reorienting some roads such that each city can visit the city 0. Return the minimum number of edges changed.
It's guaranteed that each city can reach city 0 after reorder.

Ex1:
Input: n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
Output: 3
Explanation: Change the direction of edges show in red such that each node can reach the node 0 (capital).

Ex2:
Input: n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]
Output: 2
Explanation: Change the direction of edges show in red such that each node can reach the node 0 (capital).

Ex3:
Input: n = 3, connections = [[1,0],[2,0]]
Output: 0

*/

#include <vector>
#include <cassert>
#include <unordered_map>
#include <iostream>

using namespace std;

// Time complexity: O(N), Space complexity: O(N)
int dfs(int i, unordered_map<int, vector<pair<int, int>>> &graph, vector<bool>& visited) {
    if (visited[i]) {
        return 0;
    }

    visited[i] = true;
    int count = 0;
    for (int j = 0; j < graph[i].size(); j++) {
        if (!visited[graph[i][j].first]) {
            count += graph[i][j].second;
            count += dfs(graph[i][j].first, graph, visited);
        }
    }

    return count;
}

int minReorder(int n, vector<vector<int>>& connections) {
    if (n == 0 || connections.empty()) {
        return 0;
    }

    unordered_map<int, vector<pair<int, int>>> graph;
    vector<bool> visited(n, false);

    for (int i = 0; i < n-1; i++) {
        graph[connections[i][0]].push_back({connections[i][1], 1});
        graph[connections[i][1]].push_back({connections[i][0], 0});
    }

    return dfs(0, graph, visited);
}

int main() {
    vector<vector<int>> connections1 = {{0,1},{1,3},{2,3},{4,0},{4,5}};
    assert(minReorder(6, connections1) == 3);

    vector<vector<int>> connections2 = {{1,0},{1,2},{3,2},{3,4}};
    assert(minReorder(5, connections2) == 2);

    vector<vector<int>> connections3 = {{1,0},{2,0}};
    assert(minReorder(3, connections3) == 0);

    return 0;
}