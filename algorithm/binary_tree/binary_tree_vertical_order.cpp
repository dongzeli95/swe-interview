// https://leetcode.com/problems/binary-tree-vertical-order-traversal/description/

/*
Given the root of a binary tree, return the vertical order traversal of its nodes' values. 
(i.e., from top to bottom, column by column).
If two nodes are in the same row and column, the order should be from left to right.

Ex1:
Input: root = [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]

Ex2:
Input: root = [3,9,8,4,0,1,7]
Output: [[4],[9],[3,0,1],[8],[7]]

Ex3:
Input: root = [3,9,8,4,0,1,7,null,null,null,2,5]
Output: [[4],[9,5],[3,0,1],[8,2],[7]]

*/

#include <vector>
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

// Time: O(n), Space: O(N)
vector<vector<int>> verticalOrder(TreeNode* root) {
    if (!root) {
        return {};
    }

    queue<pair<TreeNode*, int>> q;
    unordered_map<int, vector<int>> m;
    q.push({root, 0});

    int mn = INT_MAX, mx = INT_MIN;
    while (!q.empty()) {
        int s = q.size();
        for (int i = 0; i < s; i++) {
            pair<TreeNode*, int> curr = q.front();
            q.pop();

            TreeNode* n = curr.first;
            int vertical = curr.second;
            mn = min(vertical, mn);
            mx = max(vertical, mx);

            if (m.count(vertical)) {
                m[vertical].push_back(n->val);
            } else {
                m[vertical] = {n->val};
            }

            if (n->left) q.push({n->left, vertical-1});
            if (n->right) q.push({n->right, vertical+1});
        }
    }

    vector<vector<int>> res;
    for (int i = mn; i <= mx; i++) {
        res.push_back(m[i]);
    }

    return res;
}

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    vector<vector<int>> res = verticalOrder(root);
    for (vector<int> nums: res) {
        for (int i = 0; i < nums.size(); i++) {
            cout << nums[i] << " ";
        }
        cout << endl;
    }

    TreeNode* root2 = new TreeNode(3);
    root2->left = new TreeNode(9);
    root2->right = new TreeNode(8);
    root2->left->left = new TreeNode(4);
    root2->left->right = new TreeNode(0);
    root2->right->left = new TreeNode(1);
    root2->right->right = new TreeNode(7);
    vector<vector<int>> res2 = verticalOrder(root2);
    for (vector<int> nums : res2) {
        for (int i = 0; i < nums.size(); i++) {
            cout << nums[i] << " ";
        }
        cout << endl;
    }

    return 0;
}