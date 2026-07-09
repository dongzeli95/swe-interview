"""
Binary Tree Right Side View
https://leetcode.com/problems/binary-tree-right-side-view

Given the root of a binary tree, imagine yourself standing on the right side of it,
return the values of the nodes you can see ordered from top to bottom.

Approaches:
    1. BFS level-order traversal, take the last node of each level.
       Time: O(N), Space: O(N)
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(N), Space: O(N)
def rightSideView(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []

    res: List[int] = []
    q: deque[TreeNode] = deque()
    q.append(root)

    while q:
        s = len(q)
        for i in range(s):
            curr = q.popleft()

            if i == s - 1:
                res.append(curr.val)

            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)

    return res


if __name__ == "__main__":
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.right = TreeNode(5)
    root1.right.right = TreeNode(4)
    assert rightSideView(root1) == [1, 3, 4]

    root2 = TreeNode(1)
    root2.right = TreeNode(3)
    assert rightSideView(root2) == [1, 3]

    root3 = None
    assert rightSideView(root3) == []
