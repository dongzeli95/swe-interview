```cpp
// https://leetcode.com/problems/diameter-of-binary-tree/

/*
Given the root of a binary tree, return the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two nodes in a tree. 
This path may or may not pass through the root.
The length of a path between two nodes is represented by the number of edges between them.

Ex1:
Input: root = [1,2,3,4,5]
Output: 3
Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].

Ex2:
Input: root = [1,2]
Output: 1

*/

#include <iostream>

using namespace std;

class TreeNode {
public:
    TreeNode* left;
    TreeNode* right;
    int val;

    TreeNode(int v): val(v), left(nullptr), right(nullptr) {}; 
};

// Time: O(n), Space: O(1)
int helper(TreeNode* root, int& res) {
    if (!root) return -1;

    int l = 1+helper(root->left, res);
    int r = 1+helper(root->right, res);
    res = max(res, l+r);
    return max(l, r);
}

int diameter(TreeNode* root) {
    if (!root) return 0;
    int res = 0;
    helper(root, res);
    return res;
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);

    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    int res = diameter(root);
    cout << res << endl;

    TreeNode* root2 = new TreeNode(1);
    root2->left = new TreeNode(2);
    cout << diameter(root2) << endl;

    return 0;
}

```
