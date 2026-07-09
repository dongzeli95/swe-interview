"""
Binary Tree Maximum Path Sum
https://leetcode.com/problems/binary-tree-maximum-path-sum/

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes
has an edge connecting them. A node can only appear in the sequence at most once.
The path does not need to pass through the root. Return the maximum path sum of
any non-empty path.

Approaches:
1. maxPathSum:  Post-order DFS tracking a running max via an outer variable.
                Time: O(n), Space: O(n) recursion stack.
2. maxPathSum2: Post-order DFS that also reconstructs the actual path (list of
                node values) achieving the maximum sum.
                Time: O(n), Space: O(n) recursion stack + O(n) path buffers.
"""

from typing import List, Optional, Tuple


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# ---------------------------------------------------------------------------
# Approach 1: max path sum only
# Time: O(n), Space: O(n)
# ---------------------------------------------------------------------------
def _helper(curr: Optional[TreeNode], res: List[int]) -> int:
    if curr is None:
        return 0

    l = _helper(curr.left, res)
    r = _helper(curr.right, res)
    res[0] = max(res[0], curr.val)
    res[0] = max(res[0], curr.val + l)
    res[0] = max(res[0], curr.val + r)
    res[0] = max(res[0], curr.val + l + r)

    return max(curr.val, curr.val + l, curr.val + r)


def maxPathSum(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    # Emulate C++'s pass-by-reference int with a single-element list.
    res = [float("-inf")]
    _helper(root, res)
    return res[0]


# ---------------------------------------------------------------------------
# Approach 2: max path sum + reconstruct the actual path
# Time: O(n), Space: O(n)
# ---------------------------------------------------------------------------
def _helper2(
    curr: Optional[TreeNode],
    res: List[int],
    path: List[int],
    maxPath: List[int],
) -> int:
    if curr is None:
        return 0

    leftPath: List[int] = []
    rightPath: List[int] = []
    l = max(0, _helper2(curr.left, res, leftPath, maxPath))
    r = max(0, _helper2(curr.right, res, rightPath, maxPath))
    currMax = curr.val + l + r

    if currMax > res[0]:
        res[0] = currMax
        maxPath.clear()
        # Left path is currently root->leaf order relative to that subtree;
        # C++ inserts it reversed so nodes read leaf->root->right leaf.
        maxPath.extend(reversed(leftPath))
        maxPath.append(curr.val)
        maxPath.extend(rightPath)

    # Determine the maximum sum path that can continue through the parent node.
    # Note: we copy so the caller's `path` reference sees the assignment.
    if l > r:
        path[:] = leftPath
    else:
        path[:] = rightPath
    path.append(curr.val)

    return curr.val + max(l, r)


def maxPathSum2(root: Optional[TreeNode]) -> Tuple[List[int], int]:
    """Return (path_values, max_sum)."""
    path: List[int] = []
    maxPath: List[int] = []
    res = [float("-inf")]
    if root is not None:
        _helper2(root, res, path, maxPath)
    maxSum = res[0] if root is not None else 0
    return maxPath, maxSum


if __name__ == "__main__":
    # root = [-10, 9, 20, null, null, 15, 7]
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    path, maxSum = maxPathSum2(root)
    print(f"Max Path Sum: {maxSum}")
    print("Path: " + " ".join(str(v) for v in path))
