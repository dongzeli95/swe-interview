```cpp
// https://leetcode.com/problems/find-number-of-coins-to-place-in-tree-nodes/

// You are given an undirected tree with n nodes labeled from 0 to n - 1, and rooted at node 0. 
// You are given a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.

// You are also given a 0 - indexed integer array cost of length n, where cost[i] is the cost assigned to the ith node.

// You need to place some coins on every node of the tree.The number of coins to be placed at node i can be calculated as :

// If size of the subtree of node i is less than 3, place 1 coin.
// Otherwise, place an amount of coins equal to the maximum product of cost values assigned to 3 distinct nodes in the subtree of node i.
// If this product is negative, place 0 coins.
// Return an array coin of size n such that coin[i] is the number of coins placed at node i.

// Ex1:
// Input : edges = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]], cost = [1, 2, 3, 4, 5, 6]
// Output : [120, 1, 1, 1, 1, 1]
// Explanation : For node 0 place 6 * 5 * 4 = 120 coins.All other nodes are leaves with subtree of size 1, place 1 coin on each of them.

// Ex2:
// Input : edges = [[0, 1], [0, 2], [1, 3], [1, 4], [1, 5], [2, 6], [2, 7], [2, 8]], cost = [1, 4, 2, 3, 5, 7, 8, -4, 2]
// Output : [280, 140, 32, 1, 1, 1, 1, 1, 1]
// Explanation : The coins placed on each node are :
// -Place 8 * 7 * 5 = 280 coins on node 0.
// - Place 7 * 5 * 4 = 140 coins on node 1.
// - Place 8 * 2 * 2 = 32 coins on node 2.
// - All other nodes are leaves with subtree of size 1, place 1 coin on each of them.

// Ex3:
// Input : edges = [[0, 1], [0, 2]], cost = [1, 2, -2]
// Output : [0, 1, 1]
// Explanation : Node 1 and 2 are leaves with subtree of size 1, place 1 coin on each of them.
// For node 0 the only possible product of cost is 2 * 1 * -2 = -4. Hence place 0 coins on node 0.

#include <unordered_map>
#include <vector>
#include <iostream>
#include <unordered_set>

using namespace std;

class Solution {
public:
    struct Subtree {
        int pos1;
        int pos2;
        int pos3;
        int neg1;
        int neg2;
        int size;

        Subtree(int pos1,
            int pos2,
            int pos3,
            int neg1,
            int neg2, int size) :
            size(size), pos1(pos1), pos2(pos2), pos3(pos3), neg1(neg1), neg2(neg2) {}
    };
    // node 0 -> 1, 2, 3, 4, 5 
    // if len(neighbors) < 3, place 1 coin at current level.
    // go to next level, 1, 2, 3, 4, 5
    // {6, 5, 4} = 120
    void updateMax(int& pos1,
        int& pos2,
        int& pos3,
        int& neg1,
        int& neg2,
        int cost) {
        if (cost > 0) {
            if (cost >= pos1) {
                pos3 = pos2;
                pos2 = pos1;
                pos1 = cost;
            }
            else if (cost >= pos2) {
                pos3 = pos2;
                pos2 = cost;
            }
            else if (cost >= pos3) {
                pos3 = cost;
            }
        }
        else {
            if (cost <= neg1) {
                neg2 = neg1;
                neg1 = cost;
            }
            else if (cost <= neg2) {
                neg2 = cost;
            }
        }
    }

    Subtree dfs(unordered_map<int, vector<int>>& graph, int curr,
        vector<long long>& res,
        vector<int>& cost,
        unordered_set<int>& visited) {
        if (graph[curr].size() == 1 && visited.count(graph[curr][0])) {
            res[curr] = 1;
            int pos = max(cost[curr], 0);
            int neg = min(cost[curr], 0);
            Subtree subtree(pos, 0, 0, neg, 0, 1);
            return subtree;
        }

        int s = 0;
        int pos1 = 0, pos2 = 0, pos3 = 0;
        int neg1 = 0, neg2 = 0;
        for (int i = 0; i < graph[curr].size(); i++) {
            int neighbor = graph[curr][i];
            if (visited.count(neighbor)) continue;
            visited.insert(neighbor);
            Subtree subtree = dfs(graph, neighbor, res, cost, visited);
            s += subtree.size;
            updateMax(pos1, pos2, pos3, neg1, neg2, subtree.pos1);
            updateMax(pos1, pos2, pos3, neg1, neg2, subtree.pos2);
            updateMax(pos1, pos2, pos3, neg1, neg2, subtree.pos3);
            updateMax(pos1, pos2, pos3, neg1, neg2, subtree.neg1);
            updateMax(pos1, pos2, pos3, neg1, neg2, subtree.neg2);
        }

        updateMax(pos1, pos2, pos3, neg1, neg2, cost[curr]);

        if (s + 1 < 3) {
            res[curr] = 1;
        }
        else {
            long long newCost = (pos1 != 0 && pos2 != 0 && pos3 != 0) ? (long long)pos1 * pos2 * pos3 : 0;
            long long newCost2 = (neg1 != 0 && neg2 != 0 && pos1 != 0) ? (long long)pos1 * neg1 * neg2 : 0;
            long long finalCost = (newCost > newCost2) ? newCost : newCost2;
            if (finalCost < 0) {
                res[curr] = 0;
            }
            else {
                res[curr] = finalCost;
            }
        }

        Subtree subtree(pos1, pos2, pos3, neg1, neg2, s + 1);
        return subtree;
    }
    vector<long long> placedCoins(vector<vector<int>>& edges, vector<int>& cost) {
        // constructing the graph.
        unordered_map<int, vector<int>> graph;
        int n = edges.size();
        for (int i = 0; i < n; i++) {
            int s = edges[i][0];
            int e = edges[i][1];

            graph[s].push_back(e);
            graph[e].push_back(s);
        }

        vector<long long> coins(cost.size(), -1);
        unordered_set<int> visited;
        visited.insert(0);
        dfs(graph, 0, coins, cost, visited);
        return coins;
    }
};```
