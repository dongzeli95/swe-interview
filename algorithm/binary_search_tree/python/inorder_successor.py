"""
Inorder Successor in BST (LeetCode 285).

Given the root of a BST and a node p, return the in-order successor of p
(the node with the smallest key strictly greater than p.val), or None.

Approaches:
    1. inorderSuccessor -- Iterative BST walk exploiting the BST property.
       Time: O(h), Space: O(1), where h is the tree height.
"""


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: "TreeNode | None" = None
        self.right: "TreeNode | None" = None


def inorderSuccessor(root: "TreeNode | None", p: "TreeNode | None") -> "TreeNode | None":
    if root is None or p is None:
        return None

    suc: "TreeNode | None" = None
    while root is not None:
        if root.val <= p.val:
            root = root.right
        else:
            suc = root
            root = root.left

    return suc
