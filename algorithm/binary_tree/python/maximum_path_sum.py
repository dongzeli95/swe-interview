"""
Binary Tree Maximum Path Sum
https://leetcode.com/problems/binary-tree-maximum-path-sum/description/

A path in a binary tree is a sequence of nodes where each pair of adjacent
nodes has an edge connecting them. A node can appear in the sequence at
most once. The path does not need to pass through the root. Return the
maximum path sum of any non-empty path.

Approaches:
    1. Recursive DFS with a running maximum tracked via a mutable holder
       (mirrors the C++ `int& res` reference parameter).
       Time: O(n), Space: O(n) for recursion stack.
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, v: int) -> None:
        self.val: int = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(n), Space: O(n)
def helper(curr: Optional[TreeNode], res: List[int]) -> int:
    if not curr:
        return 0

    l = helper(curr.left, res)
    r = helper(curr.right, res)
    res[0] = max(res[0], curr.val)
    res[0] = max(res[0], curr.val + l)
    res[0] = max(res[0], curr.val + r)
    res[0] = max(res[0], curr.val + l + r)

    return max(curr.val, curr.val + l, curr.val + r)


def maxPathSum(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    res = [float("-inf")]
    helper(root, res)
    return res[0]


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    assert maxPathSum(root) == 6

    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert maxPathSum(root) == 42
