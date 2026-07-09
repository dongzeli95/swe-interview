"""
Distribute Coins in Binary Tree
https://leetcode.com/problems/distribute-coins-in-binary-tree/description/

Approaches:
    1. DFS post-order returning subtree excess (coins - nodes).
       Time: O(N), Space: O(H) where H is the tree height.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # Time: O(N), Space: O(H)
    def distributeCoins(self, r: Optional[TreeNode]) -> int:
        self.moves = 0

        def traverse(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left = traverse(node.left)
            right = traverse(node.right)
            self.moves += abs(left) + abs(right)
            return node.val + left + right - 1

        traverse(r)
        return self.moves
