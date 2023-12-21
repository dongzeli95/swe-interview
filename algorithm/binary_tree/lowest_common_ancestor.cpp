// https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree

/*
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

Ex1:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

Ex2:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.

Ex3:
Input: root = [1,2], p = 1, q = 2
Output: 1

*/

#include <cassert>
#include <iostream>

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

// Time: O(N), Space: O(H)
TreeNode* dfs(TreeNode* curr, TreeNode* p, TreeNode* q, TreeNode*& res) {
    if (!curr) {
        return nullptr;
    }

    TreeNode* l = dfs(curr->left, p, q, res);
    TreeNode* r = dfs(curr->right, p, q, res);

    TreeNode* currRes = nullptr;
    if (l && r) {
        res = curr;
    } else if (!l && !r) {
        if (curr->val == p->val) currRes = p;
        if (curr->val == q->val) currRes = q;
    } else {
        TreeNode* ancestor = l ? l : r;

        if (ancestor->val == p->val && curr->val == q->val) {
            res = curr;
        } else if (ancestor->val == q->val && curr->val == p->val) {
            res = curr;
        } else {
            currRes = ancestor;
        }
    }

    return currRes;
}

TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root) {
        return nullptr;
    }

    TreeNode* res;
    dfs(root, p, q, res);
    return res;
}

TreeNode* lca2(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || p == root || q == root) {
        return root;
    }

    TreeNode* left = lca2(root->left, p, q);
    TreeNode* right = lca2(root->right, p, q);
    if (left && right) {
        return root;
    }

    return left ? left : right;
}

int main() {
    // Test case 1: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
    TreeNode* root1 = new TreeNode(3);
    root1->left = new TreeNode(5);
    root1->right = new TreeNode(1);
    root1->left->left = new TreeNode(6);
    root1->left->right = new TreeNode(2);
    root1->right->left = new TreeNode(0);
    root1->right->right = new TreeNode(8);
    root1->left->right->left = new TreeNode(7);
    root1->left->right->right = new TreeNode(4);

    assert(lowestCommonAncestor(root1, root1->left, root1->right)->val == 3);

    // Test case 2: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
    TreeNode* root2 = root1;  // Reuse the same tree
    assert(lowestCommonAncestor(root2, root2->left, root2->left->right->right)->val == 5);

    // Test case 3: root = [1,2], p = 1, q = 2
    TreeNode* root3 = new TreeNode(1);
    root3->left = new TreeNode(2);
    assert(lowestCommonAncestor(root3, root3, root3->left)->val == 1);

    return 0;
}