"""
Diameter of Binary Tree
https://leetcode.com/problems/diameter-of-binary-tree/

Given the root of a binary tree, return the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two
nodes in a tree. This path may or may not pass through the root. The length of
a path between two nodes is represented by the number of edges between them.

Approaches:
1. Post-order DFS tracking max depth per subtree and updating the running diameter.
   Time: O(n), Space: O(h) recursion stack.
"""


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left = None
        self.right = None


# Time: O(n), Space: O(h) recursion stack
def helper(root, res):
    """Returns height of the subtree rooted at `root` (leaf height = 0, None = -1).
    Updates res[0] with the maximum diameter seen so far.
    """
    if not root:
        return -1

    l = 1 + helper(root.left, res)
    r = 1 + helper(root.right, res)
    res[0] = max(res[0], l + r)
    return max(l, r)


def diameter(root) -> int:
    if not root:
        return 0
    res = [0]
    helper(root, res)
    return res[0]


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    res = diameter(root)
    print(res)

    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    print(diameter(root2))
