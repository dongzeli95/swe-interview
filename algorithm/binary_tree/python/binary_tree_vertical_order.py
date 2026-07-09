"""
Binary Tree Vertical Order Traversal
https://leetcode.com/problems/binary-tree-vertical-order-traversal/description/

Given the root of a binary tree, return the vertical order traversal of its
nodes' values (from top to bottom, column by column). If two nodes are in the
same row and column, the order should be from left to right.

Approaches:
    1. verticalOrder: BFS with (node, column) pairs, tracking min/max column.
       Time: O(n), Space: O(n)
"""

from collections import defaultdict, deque
from typing import List, Optional


class TreeNode:
    def __init__(self, v: int):
        self.val: int = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(n), Space: O(n)
def verticalOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    q: deque = deque()
    m: dict = defaultdict(list)
    q.append((root, 0))

    mn, mx = float("inf"), float("-inf")
    while q:
        s = len(q)
        for _ in range(s):
            n, vertical = q.popleft()
            mn = min(vertical, mn)
            mx = max(vertical, mx)

            m[vertical].append(n.val)

            if n.left:
                q.append((n.left, vertical - 1))
            if n.right:
                q.append((n.right, vertical + 1))

    res: List[List[int]] = []
    for i in range(int(mn), int(mx) + 1):
        res.append(m[i])

    return res


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    res = verticalOrder(root)
    for nums in res:
        print(" ".join(str(x) for x in nums))

    root2 = TreeNode(3)
    root2.left = TreeNode(9)
    root2.right = TreeNode(8)
    root2.left.left = TreeNode(4)
    root2.left.right = TreeNode(0)
    root2.right.left = TreeNode(1)
    root2.right.right = TreeNode(7)
    res2 = verticalOrder(root2)
    for nums in res2:
        print(" ".join(str(x) for x in nums))
