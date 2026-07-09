"""
Maximum Depth of Binary Tree
https://leetcode.com/problems/maximum-depth-of-binary-tree

Given the root of a binary tree, return its maximum depth.

Approaches:
    1. Recursive DFS -- Time: O(n), Space: O(h) where h is tree height.
"""


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left = None
        self.right = None


def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0

    if not root.left and not root.right:
        return 1

    return 1 + max(maxDepth(root.left), maxDepth(root.right))


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)

    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
