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

# Pattern: Topological-source-style BFS on undirected tree (leaf-peeling)
# Trigger: "undirected tree, find root(s) that minimize height" → peel leaves toward center(s)
#
# Time:  O(n) — n-1 edges built in O(n); each node enqueued/popped once; each edge decremented twice.
# Space: O(n) — adjacency list (2*(n-1) entries) + branches array + queue, all O(n).
def minHeightTree(n, edges):
    if n == 1:
        return [0]
    graph: list[list[int]] = [[] for i in range(0, n)]
    # construct the graph
    for pair in edges:
        x = pair[0]
        y = pair[1]
        graph[x].append(y)
        graph[y].append(x)

    branches: list[int] = [len(i) for i in graph]
    queue: deque[int] = deque({i for i in range(len(branches)) if branches[i] == 1})
    remaining: int = n
    while remaining > 2:
        s = len(queue)
        remaining -= s
        for i in range(0, s):
            curr = queue.popleft()
            for j in graph[curr]:
                branches[j] -= 1
                if branches[j] == 1:
                    queue.append(j)

    return list(queue)

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