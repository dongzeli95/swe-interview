# https://leetcode.com/problems/validate-binary-search-tree/

# Given the root of a binary tree, determine if it is a valid binary search tree (BST).

# A valid BST is defined as follows:

# The left subtree
#  of a node contains only nodes with keys less than the node's key.
# The right subtree of a node contains only nodes with keys greater than the node's key.
# Both the left and right subtrees must also be binary search trees.

# Ex1:
# Input: root = [2,1,3]
# Output: true

# Ex2:
# Input: root = [5,1,4,null,null,3,6]
# Output: false
# Explanation: The root node's value is 5 but its right child's value is 4.

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def isValid(root, mn, mx):
    if root == None:
        return True
    
    if mn is not None and root.val <= mn:
        return False

    if mx is not None and root.val >= mx:
        return False
    
    if root.left != None:
        if isValid(root.left, mn, root.val) == False:
            return False
        
    if root.right != None:
        if isValid(root.right, root.val, mx) == False:
            return False

    return True

def isValidBST(root):
    """
    :type root: TreeNode
    :rtype: bool
    """

    return isValid(root, None, None)


def main():
    # test case
    # Ex1: True
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    print(isValidBST(root))

    # Ex2: False
    root = TreeNode(5)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.right.left = TreeNode(3)
    root.right.right = TreeNode(6)
    print(isValidBST(root))

if __name__ == "__main__":
    main()