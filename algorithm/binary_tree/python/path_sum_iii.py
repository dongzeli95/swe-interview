"""
Path Sum III - https://leetcode.com/problems/path-sum-iii

Given the root of a binary tree and an integer targetSum, return the number of
paths where the sum of the values along the path equals targetSum. The path
does not need to start or end at the root or a leaf, but it must go downwards
(parent -> child only).

Approaches:
    1. DFS with prefix-sum multiset (Counter):
       Time  O(N), Space O(N).
       At each node track the running root-to-node sum. The number of valid
       downward paths ending at the current node equals the count of previously
       seen prefix sums equal to (currSum - target). Use a Counter as a
       multiset so we can increment on entry and decrement on backtrack.
"""

from collections import Counter
from typing import Optional


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


class Solution:
    # Time: O(N), Space: O(N)
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        if not root:
            return 0

        prefix_sum: Counter = Counter()
        prefix_sum[0] = 1

        def dfs(curr: Optional[TreeNode], curr_sum: int) -> int:
            if not curr:
                return 0

            curr_sum += curr.val
            # Count all previously seen prefix sums equal to curr_sum - target.
            res = prefix_sum[curr_sum - targetSum]

            prefix_sum[curr_sum] += 1
            res += dfs(curr.left, curr_sum)
            res += dfs(curr.right, curr_sum)
            prefix_sum[curr_sum] -= 1
            if prefix_sum[curr_sum] == 0:
                del prefix_sum[curr_sum]

            return res

        return dfs(root, 0)


if __name__ == "__main__":
    # Test case 1: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(-3)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(2)
    root.left.left.left = TreeNode(3)
    root.left.left.right = TreeNode(-2)
    root.left.right.right = TreeNode(1)
    root.right.right = TreeNode(11)

    assert Solution().pathSum(root, 8) == 3

    # Test case 2: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.right.left = TreeNode(13)

    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)

    root.right.right = TreeNode(4)
    root.right.right.left = TreeNode(5)
    root.right.right.right = TreeNode(1)

    assert Solution().pathSum(root, 22) == 3
