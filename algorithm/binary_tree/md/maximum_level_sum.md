```cpp
// https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree

/*
Given the root of a binary tree, the level of its root is 1, the level of its children is 2, and so on.
Return the smallest level x such that the sum of all the values of nodes at level x is maximal.

Ex1:
Input: root = [1,7,0,7,-8,null,null]
Output: 2
Explanation:
Level 1 sum = 1.
Level 2 sum = 7 + 0 = 7.
Level 3 sum = 7 + -8 = -1.
So we return the level with the maximum sum which is level 2.

Ex2:
Input: root = [989,null,10250,98693,-89388,null,null,null,-32127]
Output: 2

*/

#include <cassert>
#include <queue>
#include <iostream>

using namespace std;

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

// Time: O(N), Space: O(N)
//
// If the tree is a complete binary tree, the last level have the most nodes.
// specifically 2^h nodes where h is the height of the tree.
// 1+2+4+8+...+2^(h) = 2^(h+1) - 1 = N
// 2^h = (N+1)/2, hence big O is O(N)
int maxLevelSum(TreeNode* root) {
    if (!root) {
        return 0;
    }

    int res = 0;
    int maxSum = 0;

    queue<TreeNode*> q;
    q.push(root);

    int level = 1;
    while (!q.empty()) {
        int s = q.size();
        int sum = 0;
        for (int i = 0; i < s; i++) {
            TreeNode* curr = q.front();
            q.pop();
            sum += curr->val;
            
            // Push next level nodes.
            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }

        if (level == 1 || sum > maxSum) {
            maxSum = sum;
            res = level;
        }

        level++;
    }

    return res;
}

int main() {
    TreeNode* root1 = new TreeNode(1);
    root1->left = new TreeNode(7);
    root1->right = new TreeNode(0);
    root1->left->left = new TreeNode(7);
    root1->left->right = new TreeNode(-8);
    assert(maxLevelSum(root1) == 2);

    TreeNode* root2 = new TreeNode(989);
    root2->right = new TreeNode(10250);
    root2->right->left = new TreeNode(98693);
    root2->right->right = new TreeNode(-89388);
    root2->right->right->right = new TreeNode(-32127);
    assert(maxLevelSum(root2) == 2);

    return 0;
}```
