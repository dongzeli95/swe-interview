// https://leetcode.com/problems/binary-tree-maximum-path-sum/description/

// A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them.
// A node can only appear in the sequence at most once.
// Note that the path does not need to pass through the root.

// The path sum of a path is the sum of the node's values in the path.
// Given the root of a binary tree, return the maximum path sum of any non - empty path.

// Ex1:
// Input: root = [1, 2, 3]
// Output : 6
// Explanation : The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

// Ex2:
// Input : root = [-10, 9, 20, null, null, 15, 7]
// Output : 42
// Explanation : The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

#include <iostream>
#include <algorithm>
#include <cassert>

using namespace std;

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

// Time: O(n), Space: O(n)
int helper(TreeNode* curr, int& res) {
    if (!curr) {
        return 0;
    }

    int l = helper(curr->left, res);
    int r = helper(curr->right, res);
    res = max(res, curr->val);
    res = max(res, curr->val + l);
    res = max(res, curr->val + r);
    res = max(res, curr->val + l + r);

    return max(curr->val, max(curr->val + l, curr->val + r));
}

int maxPathSum(TreeNode* root) {
    if (!root) return 0;
    int res = INT_MIN;
    helper(root, res);
    return res;
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    assert(maxPathSum(root) == 6);

    root = new TreeNode(-10);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    assert(maxPathSum(root) == 42);

    return 0;
}