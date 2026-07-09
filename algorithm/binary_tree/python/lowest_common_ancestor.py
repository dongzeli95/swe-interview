"""
Lowest Common Ancestor of a Binary Tree (LeetCode 236) and LCA III (LeetCode 1650).

https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/

Approaches:
    1. lowestCommonAncestor (dfs with mutable result holder)
        - Post-order DFS returning a "found" ancestor upward while updating
          a shared result when both p and q are seen.
        - Time: O(N), Space: O(H)
    2. lca2 (clean recursive LCA)
        - Classic short recursion: if root matches p or q, return root;
          otherwise combine left/right results.
        - Time: O(N), Space: O(H)
    3. lca_iii (LCA III via parent pointers + hashmap)
        - Walk from p to root recording ancestors, then walk q upward
          until we hit a recorded ancestor.
        - Time: O(log N) balanced (O(H) general), Space: O(log N)
    4. lca_iii_trick (LCA III via two-pointer swap trick)
        - Two pointers walk upward from p and q, swapping to the other
          start when they hit None; they meet at the LCA.
        - Time: O(log N) balanced (O(H) general), Space: O(1)
"""

from typing import Optional


class TreeNode:
    def __init__(self, v: int) -> None:
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


# Time: O(N), Space: O(H)
def lowestCommonAncestor(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    if not root:
        return None

    res: list = [None]  # mutable holder to mimic C++ reference parameter

    def dfs(curr: Optional[TreeNode]) -> Optional[TreeNode]:
        if not curr:
            return None

        l = dfs(curr.left)
        r = dfs(curr.right)

        curr_res: Optional[TreeNode] = None
        if l and r:
            res[0] = curr
        elif not l and not r:
            if curr.val == p.val:
                curr_res = p
            if curr.val == q.val:
                curr_res = q
        else:
            ancestor = l if l else r

            if ancestor.val == p.val and curr.val == q.val:
                res[0] = curr
            elif ancestor.val == q.val and curr.val == p.val:
                res[0] = curr
            else:
                curr_res = ancestor

        return curr_res

    dfs(root)
    return res[0]


def lca2(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    if not root or p is root or q is root:
        return root

    left = lca2(root.left, p, q)
    right = lca2(root.right, p, q)
    if left and right:
        return root

    return left if left else right


# ---------------------------------------------------------------------------
# LCA III: nodes carry a `parent` pointer.
# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/
# ---------------------------------------------------------------------------


class Node:
    def __init__(self, val: int = 0) -> None:
        self.val = val
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.parent: Optional["Node"] = None


# Time: O(log N), Space: O(log N)
def lca_iii(p: Optional[Node], q: Optional[Node]) -> Optional[Node]:
    m: dict = {}
    while p:
        m[p.val] = p
        p = p.parent

    while q:
        if q.val in m:
            return q
        q = q.parent

    return None


# Time: O(log N), Space: O(1)
def lca_iii_trick(p: Optional[Node], q: Optional[Node]) -> Optional[Node]:
    a, b = p, q
    while a is not b:
        a = q if a is None else a.parent
        b = p if b is None else b.parent
    return a


if __name__ == "__main__":
    # Test case 1: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
    root1 = TreeNode(3)
    root1.left = TreeNode(5)
    root1.right = TreeNode(1)
    root1.left.left = TreeNode(6)
    root1.left.right = TreeNode(2)
    root1.right.left = TreeNode(0)
    root1.right.right = TreeNode(8)
    root1.left.right.left = TreeNode(7)
    root1.left.right.right = TreeNode(4)

    assert lowestCommonAncestor(root1, root1.left, root1.right).val == 3

    # Test case 2: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
    root2 = root1  # Reuse the same tree
    assert (
        lowestCommonAncestor(root2, root2.left, root2.left.right.right).val == 5
    )

    # Test case 3: root = [1,2], p = 1, q = 2
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    assert lowestCommonAncestor(root3, root3, root3.left).val == 1
