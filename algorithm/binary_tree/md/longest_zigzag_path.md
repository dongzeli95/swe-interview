```cpp
// https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree

/*
You are given the root of a binary tree.

A ZigZag path for a binary tree is defined as follow:

Choose any node in the binary tree and a direction (right or left).
If the current direction is right, move to the right child of the current node; otherwise, move to the left child.
Change the direction from right to left or from left to right.
Repeat the second and third steps until you can't move in the tree.
Zigzag length is defined as the number of nodes visited - 1. (A single node has a length of 0).

Return the longest ZigZag path contained in that tree.

Ex1:
Input: root = [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]
Output: 3
Explanation: Longest ZigZag path in blue nodes (right -> left -> right).

Ex2:
Input: root = [1,1,1,null,1,null,null,1,1,null,1]
Output: 4
Explanation: Longest ZigZag path in blue nodes (left -> right -> left -> right).

Ex3:
Input: root = [1]
Output: 0
*/

#include <cassert>
#include <tuple>
#include <algorithm>
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

// Time: O(N), Space: O(N)
pair<int, int> dfs(TreeNode* curr, int& res) {
    if (!curr) {
        return {0, 0};
    }

    pair<int, int> l = dfs(curr->left, res);
    pair<int, int> r = dfs(curr->right, res);

    int left = 0, right = 0;
    if (curr->left) {
        left = 1+l.second;
    }
    if (curr->right) {
        right = 1+r.first;
    }

    res = max(res, left);
    res = max(res, right);

    return {left, right};
}

int longestZigZag(TreeNode* root) {
    if (!root) {
        return 0;
    }

    int res = 0;
    dfs(root, res);
    return res;
}

int main() {
    // [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]
    // Test case 1
    TreeNode* n1 = new TreeNode(1);
    TreeNode* n2 = new TreeNode(1);
    TreeNode* n3 = new TreeNode(1);
    TreeNode* n4 = new TreeNode(1);
    TreeNode* n5 = new TreeNode(1);
    TreeNode* n6 = new TreeNode(1);
    TreeNode* n7 = new TreeNode(1);
    TreeNode* n8 = new TreeNode(1);
    n1->right = n2;
    n2->left = n3;
    n2->right = n4;
    n4->left = n5;
    n4->right = n6;
    n5->right = n7;
    n7->right = n8;

    assert(longestZigZag(n1) == 3);

    // Test case 2
    TreeNode* n9 = new TreeNode(1);
    TreeNode* n10 = new TreeNode(1);
    TreeNode* n11 = new TreeNode(1);
    TreeNode* n12 = new TreeNode(1);
    TreeNode* n13 = new TreeNode(1);
    TreeNode* n14 = new TreeNode(1);
    TreeNode* n15 = new TreeNode(1);

    n9->left = n10;
    n9->right = n11;
    n10->right = n12;
    n12->left = n13;
    n12->right = n14;
    n13->right = n15;

    assert(longestZigZag(n9) == 4);
}```
