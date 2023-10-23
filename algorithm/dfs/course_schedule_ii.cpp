/*
https://leetcode.com/problems/course-schedule-ii

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
Example 2:

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
Example 3:

Input: numCourses = 1, prerequisites = []
Output: [0]

*/

#include <vector>
#include <cassert>
#include <iostream>

using namespace std;

bool dfs(int course, vector<vector<int>>& graph, vector<int>& visited, vector<int>& res) {
    if (visited[course] == 1) return false;  // cycle detected
    if (visited[course] == 2) return true;   // already processed

    visited[course] = 1;

    for (int nextCourse : graph[course]) {
        if (!dfs(nextCourse, graph, visited, res)) {
            return false;
        }
    }

    visited[course] = 2;
    res.push_back(course);

    return true;
}

vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
    vector<vector<int>> graph;
    vector<int> visited; 
    vector<int> res;
    graph.resize(numCourses);
    visited.resize(numCourses, 0);

    // Create graph
    for (auto& p : prerequisites) {
        graph[p[1]].push_back(p[0]);
    }

    for (int i = 0; i < numCourses; i++) {
        if (!dfs(i, graph, visited, res)) {
            return {};  // return empty array if cycle is detected
        }
    }

    reverse(res.begin(), res.end());
    return res;
}

int main() {
    vector<vector<int>> prerequisites = { {1, 0}, {2, 0}, {3, 1}, {3, 2} };
    vector<int> res = findOrder(4, prerequisites);
    vector<int> expected = { 0, 1, 2, 3 };

    for (int i = 0; i < res.size(); i++) {
        cout << res[i] << endl;
    }

    prerequisites = { {1, 0}, {0, 1} };
    res = findOrder(2, prerequisites);
    expected = {};
    assert(res == expected);
    return 0;
}