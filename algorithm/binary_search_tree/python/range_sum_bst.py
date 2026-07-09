"""
Range Sum of BST — https://leetcode.com/problems/range-sum-of-bst/

Given the root node of a binary search tree and two integers low and high,
return the sum of values of all nodes with a value in the inclusive range
[low, high].

Approaches:
    1. Recursive DFS traversal — visit every node, add to accumulator when
       value falls within [low, high]. Time O(n), Space O(h) recursion stack.
"""

from typing import Optional


class TreeNode:
    def __init__(self, v: int):
        self.val: int = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def helper(root: Optional[TreeNode], res: list, low: int, high: int) -> None:
    if not root:
        return

    if low <= root.val <= high:
        res[0] += root.val

    helper(root.left, res, low, high)
    helper(root.right, res, low, high)


def rangeSumBST(root: Optional[TreeNode], low: int, high: int) -> int:
    res = [0]
    helper(root, res, low, high)
    return res[0]
