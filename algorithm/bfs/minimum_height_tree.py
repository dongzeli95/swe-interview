# https://leetcode.com/problems/minimum-height-trees/

# A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.
# Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [ai, bi] indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you select a node x as the root, the result tree has height h. Among all possible rooted trees, those with minimum height (i.e. min(h))  are called minimum height trees (MHTs).
# Return a list of all MHTs' root labels. You can return the answer in any order.
# The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

# Ex1:
# Input: n = 4, edges = [[1,0],[1,2],[1,3]]
# Output: [1]
# Explanation: As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.

# Ex2:
# Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
# Output: [3,4]

from collections import deque

def minHeightTree(n, edges):
    if n == 1:
        return [0]
    graph = {}
    indegree = {}
    visited = set()
    for e in edges:
        s = e[0]
        d = e[1]
        if s in graph:
            graph[s].append(d)
        else:
            graph[s] = [d]

        if d in graph:
            graph[d].append(s)
        else:
            graph[d] = [s]

        if s in indegree:
            indegree[s] += 1
        else:
            indegree[s] = 1

        if d in indegree:
            indegree[d] += 1
        else:
            indegree[d] = 1

    q = deque()
    for node, degree in indegree.items():
        if degree == 1:
            q.append(node)
            indegree[node] = 0

    while n-len(visited) > 2:
        s = len(q)
        for _ in range(s):
            node = q.popleft()
            visited.add(node)
            # print("node: " + str(node))
            for i in graph[node]:
                if i in visited:
                    continue

                indegree[i] -= 1
                if indegree[i] == 1:
                    q.append(i)

        # print("length of queue: " + str(len(q)))

    return list(q)

def main():
    n = 4
    edges = [(1, 0), (1, 2), (1, 3)]
    res = minHeightTree(n, edges)
    print(res)

    n = 6
    edges = [(3, 0), (3, 1), (3, 2), (3, 4), (5, 4)]
    res = minHeightTree(n, edges)
    print(res)

if __name__ == "__main__":
    main()