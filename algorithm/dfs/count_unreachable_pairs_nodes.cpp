// https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/

/*

You are given an integer n. There is an undirected graph with n nodes, numbered from 0 to n - 1. 
You are given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
Return the number of pairs of different nodes that are unreachable from each other.

Input: n = 3, edges = [[0,1],[0,2],[1,2]]
Output: 0
Explanation: There are no pairs of nodes that are unreachable from each other. Therefore, we return 0.

Input: n = 7, edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]
Output: 14
Explanation: There are 14 pairs of nodes that are unreachable from each other:
[[0,1],[0,3],[0,6],[1,2],[1,3],[1,4],[1,5],[2,3],[2,6],[3,4],[3,5],[3,6],[4,6],[5,6]].
Therefore, we return 14.


 4 2 1
 4*2 + 4*1 + 2*1 = 14
4, 1, 1, 1

4*1 + 4*1 + 4*1 + 1*1+1*1 +1*1 = 15
*/

#include <cassert>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>

using namespace std;

void dfs(unordered_map<int, vector<int>>& graph, unordered_set<int>& visited, int curr, int& res) {
    res++;
    for (int i = 0; i < graph[curr].size(); i++) {
        int next = graph[curr][i];
        if (visited.count(next)) continue;
        visited.insert(next);
        dfs(graph, visited, next, res);
    }
}

// Time: O(n+e), Space: O(n+e)
long long countPairs(int n, vector<vector<int>>& edges) {
    int m = edges.size();

    unordered_map<int, vector<int>> graph;
    for (int i = 0; i < m; i++) {
        int node1 = edges[i][0];
        int node2 = edges[i][1];
        graph[node1].push_back(node2);
        graph[node2].push_back(node1);
    }

    unordered_set<int> visited;

    long long numberOfPairs = 0;
    long long remainingNodes = n;
    for (int i = 0; i < n; i++) {
        if (visited.count(i)) continue;
        visited.insert(i);
        int res = 0;
        dfs(graph, visited, i, res);

        numberOfPairs += res * (remainingNodes - res);
        remainingNodes -= res;
    }

    return numberOfPairs;
}

int main() {
    int n = 3;
    vector<vector<int>> edges = {{0,1},{0,2},{1,2}};
    assert(countPairs(n, edges) == 0);
    n = 7;
    edges = {{0,2},{0,5},{2,4},{1,6},{5,4}};
    assert(countPairs(n, edges) == 14);
    return 0;
}