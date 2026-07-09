"""
Delete Node in a BST — https://leetcode.com/problems/delete-node-in-a-bst

Given a root node reference of a BST and a key, delete the node with the given
key in the BST. Return the (possibly updated) root of the BST.

Approaches:
1. Recursive delete using successor/predecessor swap
   Time: O(H), Space: O(H)  (H = log N balanced, N unbalanced)
"""


class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.left = None
        self.right = None


def successor(root: TreeNode) -> int:
    root = root.right
    while root.left:
        root = root.left
    return root.val


def predecessor(root: TreeNode) -> int:
    root = root.left
    while root.right:
        root = root.right
    return root.val


# Time complexity: O(H), Space complexity: O(H)
# H is the height of the tree, which is O(logN) for balanced tree, O(N) for unbalanced tree
def deleteNode(root, key: int):
    if not root:
        return None

    if root.val == key:
        if not root.left and not root.right:
            return None
        elif root.right:
            root.val = successor(root)
            root.right = deleteNode(root.right, root.val)
        else:
            root.val = predecessor(root)
            root.left = deleteNode(root.left, root.val)
    elif root.val > key:
        root.left = deleteNode(root.left, key)
    else:
        root.right = deleteNode(root.right, key)

    return root


def printTree(root) -> None:
    if not root:
        return
    printTree(root.left)
    print(root.val, end=" ")
    printTree(root.right)


if __name__ == "__main__":
    root1 = TreeNode(5)
    root1.left = TreeNode(3)
    root1.right = TreeNode(6)
    root1.left.left = TreeNode(2)
    root1.left.right = TreeNode(4)
    root1.right.right = TreeNode(7)
    res1 = deleteNode(root1, 3)
    printTree(res1)
    print()
    assert res1.val == 5
    assert res1.left.val == 4
    assert res1.right.val == 6
    assert res1.left.left.val == 2
    assert res1.left.right is None
    assert res1.right.right.val == 7

    root2 = TreeNode(5)
    root2.left = TreeNode(3)
    root2.right = TreeNode(6)
    root2.left.left = TreeNode(2)
    root2.left.right = TreeNode(4)
    root2.right.right = TreeNode(7)
    res2 = deleteNode(root2, 0)
    printTree(res2)
    print()
    assert res2.val == 5

    root3 = None
    res3 = deleteNode(root3, 0)
    assert res3 is None
