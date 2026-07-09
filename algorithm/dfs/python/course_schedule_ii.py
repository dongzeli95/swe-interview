"""
Course Schedule II (LeetCode 210)
https://leetcode.com/problems/course-schedule-ii

Given numCourses and a list of prerequisite pairs [a, b] (b must be taken before a),
return an ordering of courses that finishes all courses, or [] if impossible.

Approaches:
    1. DFS-based topological sort using a 3-state visited array
       (0 = unvisited, 1 = visiting, 2 = processed).
       Time:  O(V + E)
       Space: O(V + E)
"""

from collections import defaultdict
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        visited = [0] * numCourses
        res: List[int] = []

        # Create graph: edge from prerequisite -> course
        for p in prerequisites:
            graph[p[1]].append(p[0])

        def dfs(course: int) -> bool:
            if visited[course] == 1:  # cycle detected
                return False
            if visited[course] == 2:  # already processed
                return True

            visited[course] = 1

            for next_course in graph[course]:
                if not dfs(next_course):
                    return False

            visited[course] = 2
            res.append(course)

            return True

        for i in range(numCourses):
            if not dfs(i):
                return []  # return empty array if cycle is detected

        res.reverse()
        return res


if __name__ == "__main__":
    sol = Solution()

    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    res = sol.findOrder(4, prerequisites)
    for x in res:
        print(x)

    prerequisites = [[1, 0], [0, 1]]
    res = sol.findOrder(2, prerequisites)
    expected: List[int] = []
    assert res == expected
