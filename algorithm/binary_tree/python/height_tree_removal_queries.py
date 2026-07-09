"""
Height of Binary Tree After Subtree Removal Queries
LeetCode: https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/

Given the root of a binary tree with unique values 1..n and a list of queries,
for each query q return the height of the tree after removing the subtree
rooted at the node with value q. Queries are independent.

Approaches:
    1. tree_queries (module-level): Optimized single-pass precompute.
       - height() computes each node's subtree height and stores per-node
         left/right subtree heights in `lhs` / `rhs`.
       - solve() DFS carries the best achievable height when a node's subtree
         is removed by combining the current depth with the sibling's height.
       Time: O(n + q), Space: O(n).

    2. Solution (class): Brute-force. For each query, detach the subtree from
       its parent, recompute the tree height, then re-attach. Memoizes on the
       removed node value.
       Time: O(q * n), Space: O(n).
"""

from collections import defaultdict
from typing import List, Optional, Tuple


class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# Approach 1: Optimized O(n) using precomputed sibling heights.
# Time: O(n + q), Space: O(n)
# ---------------------------------------------------------------------------
lhs: dict = defaultdict(int)
rhs: dict = defaultdict(int)
queryResult: dict = defaultdict(int)


def height(root: Optional[TreeNode]) -> int:
    if root is None:
        return -1

    l = height(root.left)
    r = height(root.right)
    lhs[root.val] = l
    rhs[root.val] = r
    return 1 + max(l, r)


def solve(root: Optional[TreeNode], depth: int, mx: int) -> None:
    """Fill queryResult[node.val] = height of tree if node's subtree removed."""
    if root is None:
        return

    queryResult[root.val] = mx + 1
    # Going left: best alternative height uses the right sibling's height.
    solve(root.left, depth + 1, max(mx, rhs[root.val] + depth))
    # Going right: best alternative height uses the left sibling's height.
    solve(root.right, depth + 1, max(mx, lhs[root.val] + depth))


def treeQueries(root: Optional[TreeNode], queries: List[int]) -> List[int]:
    if not queries:
        return []

    height(root)
    # At depth 0 (root), removing root.left leaves rhs[root.val] as the height,
    # and removing root.right leaves lhs[root.val] as the height.
    solve(root.left, 1, rhs[root.val])
    solve(root.right, 1, lhs[root.val])

    return [queryResult[q] for q in queries]


# ---------------------------------------------------------------------------
# Approach 2: Brute force with parent map + memoization.
# Time: O(q * n), Space: O(n)
# ---------------------------------------------------------------------------
class Solution:
    def __init__(self) -> None:
        self.heights: dict = {}
        self.parents: dict = {}  # val -> (parent_node, is_right)

    def assignParents(self, root: Optional[TreeNode],
                      parent: Optional[TreeNode], isRight: bool) -> None:
        if root is None:
            return
        self.parents[root.val] = (parent, isRight)
        self.assignParents(root.left, root, False)
        self.assignParents(root.right, root, True)

    def height(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return -1
        l = self.height(root.left)
        r = self.height(root.right)
        return 1 + max(l, r)

    def treeQueries(self, root: Optional[TreeNode],
                    queries: List[int]) -> List[int]:
        if not queries:
            return []

        rootParent = TreeNode(-1)
        self.assignParents(root, rootParent, False)
        self.height(root)

        res: List[int] = []
        for v in queries:
            parent, isRight = self.parents[v]

            # Removing a direct child of the sentinel root parent => empty tree.
            if parent is rootParent:
                res.append(0)
                continue

            if v in self.heights:
                res.append(self.heights[v])
                continue

            # Detach.
            if isRight:
                tmp = parent.right
                parent.right = None
            else:
                tmp = parent.left
                parent.left = None

            h = self.height(root)
            res.append(h)
            self.heights[v] = h

            # Re-attach to restore the tree.
            if isRight:
                parent.right = tmp
            else:
                parent.left = tmp

        return res
