```cpp
// https://leetcode.com/problems/delete-node-in-a-bst

/* 
Given a root node reference of a BST and a key, delete the node with the given key in the BST. 
Return the root node reference (possibly updated) of the BST.
Basically, the deletion can be divided into two stages:

1. Search for a node to remove.
2. If the node is found, delete the node.

Ex1:
Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
Explanation: Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7], shown in the above BST.
Please notice that another valid answer is [5,2,6,null,4,null,7] and it's also accepted.

Ex2:
Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: The tree does not contain a node with value = 0.

Ex3:
Input: root = [], key = 0
Output: []

*/

#include <cassert>
#include <iostream>

using namespace std;

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

int successor(TreeNode* root) {
    root = root->right;
    while (root->left) {
        root = root->left;
    }

    return root->val;
}
int predecessor(TreeNode* root) {
    root = root->left;
    while (root->right) {
        root = root->right;
    }

    return root->val;
}

// Time complexity: O(H), Space complexity: O(H)
// H is the height of the tree, which is O(logN) for balanced tree, O(N) for unbalanced tree
TreeNode* deleteNode(TreeNode* root, int key) {
    if (!root) {
        return nullptr;
    }

    if (root->val == key) {
        if (!root->left && !root->right) {
            return nullptr;
        } else if (root->right) {
            root->val = successor(root);
            root->right = deleteNode(root->right, root->val);
        } else {
            root->val = predecessor(root);
            root->left = deleteNode(root->left, root->val);
        }
    } else if (root->val > key) {
        root->left = deleteNode(root->left, key);
    } else {
        root->right = deleteNode(root->right, key);
    }

    return root;
}

void printTree(TreeNode* root) {
    if (!root) {
        return;
    }

    printTree(root->left);
    cout << root->val << " ";
    printTree(root->right);
}

int main() {
    TreeNode* root1 = new TreeNode(5);
    root1->left = new TreeNode(3);
    root1->right = new TreeNode(6);
    root1->left->left = new TreeNode(2);
    root1->left->right = new TreeNode(4);
    root1->right->right = new TreeNode(7);
    TreeNode* res1 = deleteNode(root1, 3);
    printTree(res1);
    assert(res1->val == 5);
    assert(res1->left->val == 4);
    assert(res1->right->val == 6);
    assert(res1->left->left->val == 2);
    assert(res1->left->right == nullptr);
    assert(res1->right->right->val == 7);

    TreeNode* root2 = new TreeNode(5);
    root2->left = new TreeNode(3);
    root2->right = new TreeNode(6);
    root2->left->left = new TreeNode(2);
    root2->left->right = new TreeNode(4);
    root2->right->right = new TreeNode(7);
    TreeNode* res2 = deleteNode(root2, 0);
    printTree(res2);
    assert(res2->val == 5);

    TreeNode* root3 = nullptr;
    TreeNode* res3 = deleteNode(root3, 0);
    assert(res3 == nullptr);

    return 0;
}```
