// https://leetcode.com/problems/binary-tree-right-side-view

/*
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

Ex1:
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]

Ex2:
Input: root = [1,null,3]
Output: [1,3]

Ex3:
Input: root = []
Output: []

*/

#include <cassert>
#include <vector>
#include <queue>

using namespace std;

class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

// Time: O(N), Space: O(N)
vector<int> rightSideView(TreeNode* root) {
    if (!root) {
        return {};
    }

    vector<int> res;
    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        int s = q.size();
        for (int i = 0; i < s; i++) {
            TreeNode* curr = q.front();
            q.pop();

            if (i == s-1) {
                res.push_back(curr->val);
            }

            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }
    }

    return res;
}

int main() {
    TreeNode* root1 = new TreeNode(1);
    root1->left = new TreeNode(2);
    root1->right = new TreeNode(3);
    root1->left->right = new TreeNode(5);
    root1->right->right = new TreeNode(4);
    vector<int> res1 = {1,3,4};
    assert(rightSideView(root1) == res1);

    TreeNode* root2 = new TreeNode(1);
    root2->right = new TreeNode(3);
    vector<int> res2 = {1,3};
    assert(rightSideView(root2) == res2);

    TreeNode* root3 = nullptr;
    vector<int> res3 = {};
    assert(rightSideView(root3) == res3);

    return 0;
}