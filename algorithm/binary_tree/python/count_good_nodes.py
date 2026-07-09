"""
Count Good Nodes in Binary Tree
https://leetcode.com/problems/count-good-nodes-in-binary-tree

Given a binary tree root, a node X is "good" if in the path from root to X
there are no nodes with a value greater than X. Return the number of good
nodes in the binary tree.

Approaches:
1. DFS carrying the running max down the path.
   Time: O(N), Space: O(N) for recursion stack.
"""

from typing import Optional


class TreeNode:
    def __init__(self, v: int) -> None:
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(N), Space: O(N)
def dfs(curr: Optional[TreeNode], mx: int, res: list) -> None:
    if not curr:
        return

    next_mx = mx
    if curr.val >= mx:
        next_mx = curr.val
        res[0] += 1

    dfs(curr.left, next_mx, res)
    dfs(curr.right, next_mx, res)


def goodNodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    res = [0]
    mx = root.val
    dfs(root, mx, res)
    return res[0]


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.left = TreeNode(3)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(5)
    assert goodNodes(root) == 4

    root = TreeNode(3)
    root.left = TreeNode(3)
    root.left.right = TreeNode(2)
    root.left.left = TreeNode(4)
    assert goodNodes(root) == 3

    root = TreeNode(1)
    assert goodNodes(root) == 1
