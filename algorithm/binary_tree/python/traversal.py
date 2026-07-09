"""Binary Tree Iterative Traversals.

Approaches (mirrors traversal.cpp 1-to-1):
    1. preorder_iterative  - Iterative preorder using an explicit stack. O(n) time, O(h) space.
    2. inorder_iterative   - Iterative inorder using an explicit stack. O(n) time, O(h) space.
    3. postorder_iterative - Iterative postorder using a stack with a 'head' pointer
                             tracking the last visited node. O(n) time, O(h) space.
"""

from typing import Optional


class TreeNode:
    def __init__(self, v: int):
        self.val: int = v
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def preorder_iterative(root: Optional[TreeNode]) -> None:
    if not root:
        return

    st = [root]

    while st:
        curr = st.pop()

        print(curr.val)

        if curr.right:
            st.append(curr.right)

        if curr.left:
            st.append(curr.left)


def inorder_iterative(root: Optional[TreeNode]) -> None:
    st: list[TreeNode] = []
    curr = root

    while curr or st:
        while curr:
            st.append(curr)
            curr = curr.left

        curr = st.pop()
        print(curr.val)

        curr = curr.right


# [3, 4, 2, ]
def postorder_iterative(root: Optional[TreeNode]) -> None:
    if not root:
        return

    s = [root]
    head = root
    while s:
        t = s[-1]
        if (not t.left and not t.right) or t.left is head or t.right is head:
            print(t.val)
            s.pop()
            head = t
        else:
            if t.right:
                s.append(t.right)
            if t.left:
                s.append(t.left)


# [1, 3, 2, 5, 4]

#         1
#       /  \
#      2    3
#     /\    /\
#    4  5

# 1, 2, 4, 5, 3


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    root2 = TreeNode(3)
    root2.left = TreeNode(2)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(1)

    # preorder_iterative(root)
    # print()
    # print()

    # inorder_iterative(root)  # 4 2, 5, 1, 3
    # print()
    # print()

    # postorder_iterative(root)  # 4, 5, 2, 3, 1
    # print()
    # print()

    postorder_iterative(root2)
    print()
    print()
