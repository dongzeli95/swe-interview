"""Move Zeros in a Binary Tree.

Problem: Swap values within the tree so that every 0 is moved down into a
subtree — after swapping, no 0 node may have any non-zero node in its subtree.
Only values are swapped (structure is untouched), and a 0 can only be moved
into its own subtree.

Approaches:
    1. Recursive top-down swap — O(n) time, O(h) space for the recursion stack.
       At each node, if the current value is 0, swap it with the first non-null
       child (left first, then right), then recurse into both children so the
       0 keeps propagating downward until it reaches a leaf slot.
"""

from typing import Optional


class TreeNode:
    def __init__(self, v: int) -> None:
        self.val = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def swap(root: Optional[TreeNode]) -> None:
    if not root:
        return

    need_swap = root.val == 0
    if root.left:
        if need_swap:
            root.val = root.left.val
            root.left.val = 0
            need_swap = False

        swap(root.left)

    if root.right:
        if need_swap:
            root.val = root.right.val
            root.right.val = 0

        swap(root.right)


def swap_zero(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    swap(root)
    return root


def print_tree(root: Optional[TreeNode]) -> None:
    if not root:
        return

    print_tree(root.left)
    print(root.val, end=" ")
    print_tree(root.right)


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(0)
    root.right = TreeNode(2)
    root.left.left = TreeNode(3)
    root.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(0)
    root.right.left.left = TreeNode(4)
    root.right.left.right = TreeNode(5)

    print_tree(root)
    print()

    res = swap_zero(root)
    print_tree(res)
    print()
