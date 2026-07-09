"""
Count Nodes Equal to Average of Subtree
https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/

Given the root of a binary tree, return the number of nodes where the value of
the node is equal to the average (floor division) of the values in its subtree.

Approaches:
    1. Post-order DFS returning (sum, count) per subtree.
       Time: O(n), Space: O(n) (recursion stack).
"""

from typing import Optional, Tuple


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(n), Space: O(n)
def helper(curr: Optional[TreeNode], res: list) -> Tuple[int, int]:
    # base case
    if not curr:
        return (0, 0)

    l = helper(curr.left, res)
    r = helper(curr.right, res)
    num_of_nodes = l[1] + r[1] + 1
    total = l[0] + r[0] + curr.val
    avg = total // num_of_nodes
    if avg == curr.val:
        res[0] += 1
    return (total, num_of_nodes)


def averageOfSubtree(root: Optional[TreeNode]) -> int:
    res = [0]
    helper(root, res)
    return res[0]
