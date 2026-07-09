// https://leetcode.com/problems/range-sum-of-bst/

/*
Given the root node of a binary search tree and two integers low and high, 
return the sum of values of all nodes with a value in the inclusive range [low, high].

Ex1:
Input: root = [10,5,15,3,7,null,18], low = 7, high = 15
Output: 32
Explanation: Nodes 7, 10, and 15 are in the range [7, 15]. 7 + 10 + 15 = 32.

Ex2:
Input: root = [10,5,15,3,7,13,18,1,null,6], low = 6, high = 10
Output: 23
Explanation: Nodes 6, 7, and 10 are in the range [6, 10]. 6 + 7 + 10 = 23.

*/

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

void helper(TreeNode* root, int& res, int &low, int &high) {
    if (!root) {
        return;
    }

    if (root->val >= low && root->val <= high) {
        res += root->val;
    }

    helper(root->left, res, low, high);
    helper(root->right, res, low, high);
}

int rangeSumBST(TreeNode* root, int low, int high) {
    int res = 0;
    helper(root, res, low, high);
    return res;
}