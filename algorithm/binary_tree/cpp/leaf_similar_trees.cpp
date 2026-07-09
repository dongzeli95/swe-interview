// https://leetcode.com/problems/leaf-similar-trees

/*
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.
For example, in the given tree above, the leaf value sequence is (6, 7, 4, 9, 8).
Two binary trees are considered leaf-similar if their leaf value sequence is the same.
Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.

Ex1:
Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true

Ex2:
Input: root1 = [1,2,3], root2 = [1,3,2]
Output: false

*/

#include <cassert>
#include <vector>

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

// Time: O(m+n), Space: O(m+n)
void dfs(TreeNode* curr, vector<int>& res) {
    if (!curr) {
        return;
    }

    if (!curr->left && !curr->right) {
        res.push_back(curr->val);
    }

    dfs(curr->left, res);
    dfs(curr->right, res);
}

bool leafSimilar(TreeNode* root1, TreeNode* root2) {
    vector<int> res1;
    vector<int> res2;
    dfs(root1, res1);
    dfs(root2, res2);

    return res1 == res2;
}

int main() {
    TreeNode* root1 = new TreeNode(3);
    root1->left = new TreeNode(5);
    root1->right = new TreeNode(1);

    root1->left->left = new TreeNode(6);
    root1->left->right = new TreeNode(2);
    root1->left->right->left = new TreeNode(7);
    root1->left->right->right = new TreeNode(4);

    root1->right->left = new TreeNode(9);
    root1->right->right = new TreeNode(8);


    // Tree for root2 in Example 1
    TreeNode* root2 = new TreeNode(3);
    root2->left = new TreeNode(5);
    root2->right = new TreeNode(1);

    root2->left->left = new TreeNode(6);
    root2->left->right = new TreeNode(7);

    root2->right->left = new TreeNode(4);
    root2->right->right = new TreeNode(2);
    root2->right->right->left = new TreeNode(9);
    root2->right->right->right = new TreeNode(8);

    assert(leafSimilar(root1, root2) == true);

    // Tree for root2 in Example 2
    root1 = new TreeNode(1);
    root1->left = new TreeNode(3);
    root1->right = new TreeNode(2);

    root2 = new TreeNode(1);
    root2->left = new TreeNode(2);
    root2->right = new TreeNode(3);
    assert(leafSimilar(root1, root2) == false);

    return 0;
}