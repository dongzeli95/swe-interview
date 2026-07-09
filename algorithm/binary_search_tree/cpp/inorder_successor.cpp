// https://leetcode.com/problems/inorder-successor-in-bst/description/

/*
Given the root of a binary search tree and a node p in it, 
return the in-order successor of that node in the BST. 
If the given node has no in-order successor in the tree, return null.

The successor of a node p is the node with the smallest key greater than p.val.

Ex1:
Input: root = [2,1,3], p = 1
Output: 2
Explanation: 1's in-order successor node is 2. Note that both p and the return value is of TreeNode type.

Ex2:
Input: root = [5,3,6,2,4,null,null,1], p = 6
Output: null
Explanation: There is no in-order successor of the current node, so the answer is null.

*/

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* inorderSuccessor(TreeNode* root, TreeNode* p) {
    if (root == nullptr || p == nullptr) return nullptr;

    TreeNode* suc = nullptr;
    while (root != nullptr) {
        if (root->val <= p->val) {
            root = root->right;
        }
        else {
            suc = root;
            root = root->left;
        }
    }

    return suc;
}