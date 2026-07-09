"""
Maximum Level Sum of a Binary Tree
https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree

Given the root of a binary tree, the level of its root is 1, the level of its
children is 2, and so on. Return the smallest level x such that the sum of all
the values of nodes at level x is maximal.

Approaches:
  1. maxLevelSum: BFS level-order traversal using a queue. Time O(N), Space O(N).
"""

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(N), Space: O(N)
#
# If the tree is a complete binary tree, the last level have the most nodes.
# specifically 2^h nodes where h is the height of the tree.
# 1+2+4+8+...+2^(h) = 2^(h+1) - 1 = N
# 2^h = (N+1)/2, hence big O is O(N)
def maxLevelSum(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    res = 0
    max_sum = 0

    q: deque[TreeNode] = deque()
    q.append(root)

    level = 1
    while q:
        s = len(q)
        cur_sum = 0
        for _ in range(s):
            curr = q.popleft()
            cur_sum += curr.val

            # Push next level nodes.
            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)

        if level == 1 or cur_sum > max_sum:
            max_sum = cur_sum
            res = level

        level += 1

    return res


if __name__ == "__main__":
    root1 = TreeNode(1)
    root1.left = TreeNode(7)
    root1.right = TreeNode(0)
    root1.left.left = TreeNode(7)
    root1.left.right = TreeNode(-8)
    assert maxLevelSum(root1) == 2

    root2 = TreeNode(989)
    root2.right = TreeNode(10250)
    root2.right.left = TreeNode(98693)
    root2.right.right = TreeNode(-89388)
    root2.right.right.right = TreeNode(-32127)
    assert maxLevelSum(root2) == 2
