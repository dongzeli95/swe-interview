```cpp
// https://leetcode.com/problems/evaluate-division

/*
You are given an array of variable pairs equations and an array of real numbers values, where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. 
Each Ai or Bi is a string that represents a single variable.
You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query where you must find the answer for Cj / Dj = ?.
Return the answers to all queries. If a single answer cannot be determined, return -1.0.
Note: The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction.
Note: The variables that do not occur in the list of equations are undefined, so the answer cannot be determined for them.

Ex1:
Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
Explanation:
Given: a / b = 2.0, b / c = 3.0
queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ?
return: [6.0, 0.5, -1.0, 1.0, -1.0 ]
note: x is undefined => -1.0

Ex2:
Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
Output: [3.75000,0.40000,5.00000,0.20000]

Ex3:
Input: equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
Output: [0.50000,2.00000,-1.00000,-1.00000]

*/

#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <cassert>

using namespace std;

// M is number of quries, N is number of equations
// Time complexity: O(M*N), Space complexity: O(N)
double dfs(string curr, string dest, unordered_map<string, vector<pair<string, double>>>& graph, 
    unordered_map<string, double>& cache,
    unordered_set<string>& visited) {
    if (cache.count(curr)) {
        return cache[curr];
    }

    if (graph.count(curr) == 0) {
        return -1.0;
    }

    if (curr == dest) {
        return 1.0;
    }

    double res = -1.0;
    // If curr string doesn't exist in graph, this operation will actually insert it into graph with an empty vector
    // Be careful because we need to check if curr string exists in graph or not.
    int n = graph[curr].size();
    for (int i = 0; i < n; i++) {
        if (visited.count(graph[curr][i].first)) {
            continue;
        }

        string next = graph[curr][i].first;
        visited.insert(next);

        double val = graph[curr][i].second;
        double subVal = dfs(next, dest, graph, cache, visited);
        if (subVal != -1) {
            res = val*subVal;
            break;
        }
    }

    cache[curr] = res;
    return res;
}

vector<double> calcEquation(vector<vector<string>>& equations, 
                            vector<double>& values, 
                            vector<vector<string>>& queries) {
    vector<double> res;
    unordered_map<string, vector<pair<string, double>>> graph;
    int n = equations.size();

    for (int i = 0; i < n; i++) {
        string s1 = equations[i][0];
        string s2 = equations[i][1];
        graph[s1].push_back(make_pair(s2, values[i]));
        graph[s2].push_back(make_pair(s1, 1.0/values[i]));
    }

    unordered_map<string, double> cache;
    unordered_set<string> visited;
    for (int i = 0; i < queries.size(); i++) {
        string s1 = queries[i][0];
        string s2 = queries[i][1];
        cache.clear();
        visited.clear();
        visited.insert(s1);
        res.push_back(dfs(s1, s2, graph, cache, visited));
    }

    return res;
}

int main() {
    vector<vector<string>> equations1 = {{"a","b"},{"b","c"}};
    vector<double> values1 = {2.0,3.0};
    vector<vector<string>> quries1 = {{"a","c"},{"b","a"},{"a","e"},{"a","a"},{"x","x"}};
    vector<double> res1 = {6.00000,0.50000,-1.00000,1.00000,-1.00000};
    assert(calcEquation(equations1, values1, quries1) == res1);

    vector<vector<string>> equations2 = {{"a","b"},{"b","c"},{"bc","cd"}};
    vector<double> values2 = {1.5, 2.5, 5.0};
    vector<vector<string>> quries2 = {{"a","c"},{"c","b"},{"bc","cd"},{"cd","bc"}};
    vector<double> res2 = {3.75000,0.40000,5.00000,0.20000};
    assert(calcEquation(equations2, values2, quries2) == res2);

    vector<vector<string>> equations3 = {{"a","b"}};
    vector<double> values3 = {0.5};
    vector<vector<string>> quries3 = {{"a","b"},{"b","a"},{"a","c"},{"x","y"}};
    vector<double> res3 = {0.50000,2.00000,-1.00000,-1.00000};
    assert(calcEquation(equations3, values3, quries3) == res3);

    vector<vector<string>> equations4 = { {"x1","x2"} };
    vector<double> values4 = { 3.0 };
    vector<vector<string>> quries4 = { {"x9","x2"},{"x9","x9"} };
    vector<double> res4 = { -1.0, -1.0 };
    assert(calcEquation(equations4, values4, quries4) == res4);
    return 0;
}```
