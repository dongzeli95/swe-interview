// https://leetcode.com/problems/maximum-depth-of-binary-tree

/*
Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Ex1:
Input: root = [3,9,20,null,null,15,7]
Output: 3

Ex2:
Input: root = [1,null,2]
Output: 2
*/

#include <cassert>
#include <algorithm>

using namespace std;

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int v) {
        left = nullptr;
        right = nullptr;
        val = v;
    }
};

int maxDepth(TreeNode* root) {
    if (!root) {
        return 0;
    }

    if (!root->left && !root->right) {
        return 1;
    }

    return 1+max(maxDepth(root->left),
                maxDepth(root->right));
}

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);

    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);

    return 0;
}