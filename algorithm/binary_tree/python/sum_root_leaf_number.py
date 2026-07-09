"""
Sum Root to Leaf Numbers
https://leetcode.com/problems/sum-root-to-leaf-numbers/

You are given the root of a binary tree containing digits from 0 to 9 only.
Each root-to-leaf path in the tree represents a number.
For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.
Return the total sum of all root-to-leaf numbers.

Approaches:
1. sumNumbersIterative: DFS with an explicit stack. Time O(n), Space O(H).
2. sumNumbersMorris: Morris traversal with temporary threading. Time O(n), Space O(1).
3. sumNumbers: Recursive pre-order helper. Time O(n), Space O(H).
"""


class TreeNode:
    def __init__(self, v):
        self.val = v
        self.left = None
        self.right = None


# Iterative, stack or queue.
# Time: O(n), Space: O(H)
def sumNumbersIterative(root):
    if not root:
        return 0

    st = [(root, root.val)]

    res = 0
    while st:
        node, val = st.pop()

        if not node.left and not node.right:
            res += val
        if node.left:
            st.append((node.left, val * 10 + node.left.val))

        if node.right:
            st.append((node.right, val * 10 + node.right.val))

    return res


# Morris
#
# The idea of Morris algorithm is to set temporary link between the node and its predecessor.
# predecessor.right = root.
# If there is no link? set it and go to the left subtree.
# If there is a link? break it and go to the right subtree.
#
# Time: O(N), Space: O(1)
def sumNumbersMorris(root):
    rootToLeaf = 0
    currNumber = 0

    while root:
        if root.left:
            # Finding the predecessor
            predecessor = root.left
            steps = 1
            while predecessor.right and predecessor.right is not root:
                predecessor = predecessor.right
                steps += 1

            # Making a temporary link and moving to the left subtree
            if not predecessor.right:
                currNumber = currNumber * 10 + root.val
                predecessor.right = root
                root = root.left
            # Breaking the temporary link and moving to the right subtree
            else:
                # If you're on a leaf, update the sum
                if not predecessor.left:
                    rootToLeaf += currNumber
                # Backtracking the current number
                for _ in range(steps):
                    currNumber //= 10
                predecessor.right = None
                root = root.right
        # If there is no left child, just go right
        else:
            currNumber = currNumber * 10 + root.val
            # If you're on a leaf, update the sum
            if not root.right:
                rootToLeaf += currNumber
            root = root.right

    return rootToLeaf


# TODO: pre-order traversal, in-order traversal, post-order traversal.

# Time: O(n), Space: O(H)
def helper(curr, res, sum_):
    if not curr:
        return

    sum_ += curr.val
    if not curr.left and not curr.right:
        res[0] += sum_
        return

    helper(curr.left, res, sum_ * 10)
    helper(curr.right, res, sum_ * 10)


def sumNumbers(root):
    res = [0]
    helper(root, res, 0)
    return res[0]


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    print(sumNumbers(root))
    print(sumNumbersIterative(root))
    print(sumNumbersMorris(root))

    #      2
    #    /  \
    #   3   4
    #  / \
    # 1   5

    # 231+235+24
    root2 = TreeNode(2)
    root2.left = TreeNode(3)
    root2.right = TreeNode(4)
    root2.left.left = TreeNode(1)
    root2.left.right = TreeNode(5)
    print(sumNumbers(root2))
    print(sumNumbersIterative(root2))
    print(sumNumbersMorris(root2))

    #     [5, 3, 2, 7, 0, 6, null, null, null, 0] , 6363
    #      5
    #     / \
    #    3   2
    #   / \  /
    #  7  0  6
    #     \
    #      0
