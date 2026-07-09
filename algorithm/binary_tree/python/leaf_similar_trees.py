"""
Leaf-Similar Trees
https://leetcode.com/problems/leaf-similar-trees

Consider all the leaves of a binary tree, from left to right order, the values
of those leaves form a leaf value sequence. Two binary trees are considered
leaf-similar if their leaf value sequence is the same. Return True iff the two
given trees with head nodes root1 and root2 are leaf-similar.

Approaches:
    1. DFS collect leaves into two lists, then compare.
       Time: O(m + n), Space: O(m + n)
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(m+n), Space: O(m+n)
def dfs(curr: Optional[TreeNode], res: List[int]) -> None:
    if not curr:
        return

    if not curr.left and not curr.right:
        res.append(curr.val)

    dfs(curr.left, res)
    dfs(curr.right, res)


def leafSimilar(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
    res1: List[int] = []
    res2: List[int] = []
    dfs(root1, res1)
    dfs(root2, res2)

    return res1 == res2


if __name__ == "__main__":
    # Tree for root1 in Example 1
    root1 = TreeNode(3)
    root1.left = TreeNode(5)
    root1.right = TreeNode(1)

    root1.left.left = TreeNode(6)
    root1.left.right = TreeNode(2)
    root1.left.right.left = TreeNode(7)
    root1.left.right.right = TreeNode(4)

    root1.right.left = TreeNode(9)
    root1.right.right = TreeNode(8)

    # Tree for root2 in Example 1
    root2 = TreeNode(3)
    root2.left = TreeNode(5)
    root2.right = TreeNode(1)

    root2.left.left = TreeNode(6)
    root2.left.right = TreeNode(7)

    root2.right.left = TreeNode(4)
    root2.right.right = TreeNode(2)
    root2.right.right.left = TreeNode(9)
    root2.right.right.right = TreeNode(8)

    assert leafSimilar(root1, root2) is True

    # Trees for Example 2
    root1 = TreeNode(1)
    root1.left = TreeNode(3)
    root1.right = TreeNode(2)

    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    assert leafSimilar(root1, root2) is False
