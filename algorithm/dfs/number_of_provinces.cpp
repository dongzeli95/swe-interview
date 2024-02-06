// https://leetcode.com/problems/number-of-provinces

/*
There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.
A province is a group of directly or indirectly connected cities and no other cities outside of the group.
You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.
Return the total number of provinces.

Ex1:
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2

Ex2:
Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3

*/

#include <vector>
#include <cassert>
#include <unordered_set>
#include <unordered_map>

using namespace std;

// Time: O(N^2), we need n^2 time to construct graph, and also dense graph can have N^2 number of edges
// Space: O(N^2)
void dfs(int curr, unordered_map<int, vector<int>>& graph, unordered_set<int>& visited) {
    for (int next : graph[curr]) {
        if (visited.count(next)) continue;
        visited.insert(next);
        dfs(next, graph, visited);
    }
}

int findCircleNum(vector<vector<int>>& isConnected) {
    if (isConnected.empty() || isConnected[0].empty()) {
        return 0;
    }

    unordered_map<int, vector<int>> graph;
    
    int n = isConnected.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (isConnected[i][j] == 1) {
                graph[i].push_back(j);
                graph[j].push_back(i);
            }
        }
    }

    int res = 0;
    unordered_set<int> visited;
    for (int i = 0; i < n; i++) {
        if (visited.count(i)) continue;
        visited.insert(i);
        dfs(i, graph, visited);
        res++;
    }

    return res;
}

// Time: O(N^2), Space: O(N)
void dfs(vector<vector<int>>& isConnected, int curr, unordered_set<int>& visited) {
    for (int i = 0; i < isConnected[curr].size(); i++) {
        int neighbor = i;
        if (visited.count(neighbor) || isConnected[curr][neighbor] == 0) continue;
        visited.insert(neighbor);
        dfs(isConnected, neighbor, visited);
    }
}

int findCircleNum(vector<vector<int>>& isConnected) {
    int n = isConnected.size();
    int res = 0;
    unordered_set<int> visited;

    for (int i = 0; i < n; i++) {
        if (visited.count(i)) {
            continue;
        }
        visited.insert(i);
        dfs(isConnected, i, visited);
        res++;
    }

    return res;
}

int main() {
    vector<vector<int>> isConnected1 = {{1,1,0},{1,1,0},{0,0,1}};
    assert(findCircleNum(isConnected1) == 2);

    vector<vector<int>> isConnected2 = {{1,0,0},{0,1,0},{0,0,1}};
    assert(findCircleNum(isConnected2) == 3);

    return 0;
}