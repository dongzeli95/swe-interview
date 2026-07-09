"""
Longest ZigZag Path in a Binary Tree
https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree

Approaches:
1. DFS returning (left_zigzag, right_zigzag) per node; track global max.
   Time: O(N), Space: O(N)
"""

from typing import Optional, Tuple


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(N), Space: O(N)
def dfs(curr: Optional[TreeNode], res: list) -> Tuple[int, int]:
    if not curr:
        return (0, 0)

    l = dfs(curr.left, res)
    r = dfs(curr.right, res)

    left = 0
    right = 0
    if curr.left:
        left = 1 + l[1]
    if curr.right:
        right = 1 + r[0]

    res[0] = max(res[0], left)
    res[0] = max(res[0], right)

    return (left, right)


def longestZigZag(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    res = [0]
    dfs(root, res)
    return res[0]


if __name__ == "__main__":
    # [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]
    # Test case 1
    n1 = TreeNode(1)
    n2 = TreeNode(1)
    n3 = TreeNode(1)
    n4 = TreeNode(1)
    n5 = TreeNode(1)
    n6 = TreeNode(1)
    n7 = TreeNode(1)
    n8 = TreeNode(1)
    n1.right = n2
    n2.left = n3
    n2.right = n4
    n4.left = n5
    n4.right = n6
    n5.right = n7
    n7.right = n8

    assert longestZigZag(n1) == 3

    # Test case 2
    n9 = TreeNode(1)
    n10 = TreeNode(1)
    n11 = TreeNode(1)
    n12 = TreeNode(1)
    n13 = TreeNode(1)
    n14 = TreeNode(1)
    n15 = TreeNode(1)

    n9.left = n10
    n9.right = n11
    n10.right = n12
    n12.left = n13
    n12.right = n14
    n13.right = n15

    assert longestZigZag(n9) == 4
