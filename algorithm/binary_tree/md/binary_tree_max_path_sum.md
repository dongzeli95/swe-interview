```cpp
// https://leetcode.com/problems/binary-tree-maximum-path-sum/

/*
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. 
A node can only appear in the sequence at most once. 
Note that the path does not need to pass through the root.
The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.

Ex1:
Input: root = [1,2,3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

Ex2:
Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

*/

#include <vector>
#include <iostream>
#include <cassert>
#include <algorithm>

using namespace std;

class TreeNode {
public:
    TreeNode(int v) {
        val = v;
        left = nullptr;
        right = nullptr;
    }

    int val;
    TreeNode* left;
    TreeNode* right;
};

int helper(TreeNode*curr, int& res) {
    if (!curr) {
        return 0;
    }

    int l = helper(curr->left, res);
    int r = helper(curr->right, res);
    res = max(res, curr->val);
    res = max(res, curr->val + l);
    res = max(res, curr->val + r);
    res = max(res, curr->val + l + r);

    return max(curr->val, max(curr->val+l, curr->val+ r));
}

// Time: O(n), Space: O(n)
int maxPathSum(TreeNode* root) {
    if (!root) return 0;
    int res = INT_MIN;
    helper(root, res);
    return res;
}

int helper2(TreeNode* curr, int& res, vector<int>& path, vector<int>& maxPath) {
    if (!curr) return 0;

    vector<int> leftPath, rightPath;
    int l = max(0, helper2(curr->left, res, leftPath, maxPath));
    int r = max(0, helper2(curr->right, res, rightPath, maxPath));
    int currMax = curr->val + l + r;

    if (currMax > res) {
        res = currMax;
        maxPath.clear();
        maxPath.insert(maxPath.end(), leftPath.rbegin(), leftPath.rend());
        maxPath.push_back(curr->val);
        maxPath.insert(maxPath.end(), rightPath.begin(), rightPath.end());
    }

    // Determine the maximum sum path that can continue through the parent node
    path = (l > r) ? leftPath : rightPath;
    path.push_back(curr->val);

    return curr->val + max(l, r);
}

// Time: O(n), Space: O(n)
vector<int> maxPathSum2(TreeNode* root, int& maxSum) {
    vector<int> path, maxPath;
    maxSum = INT_MIN;
    if (root) {
        helper2(root, maxSum, path, maxPath);
    }
    return maxPath;
}

int main() {
    // TreeNode* root = new TreeNode(1);
    // root->left = new TreeNode(2);
    // root->right = new TreeNode(3);
    // // cout << maxPathSum(root) << endl;
    // assert(maxPathSum(root) == 6);

    // root = new TreeNode(-10);
    // root->left = new TreeNode(9);
    // root->right = new TreeNode(20);
    // root->right->left = new TreeNode(15);
    // root->right->right = new TreeNode(7);
    // assert(maxPathSum(root) == 42);


    TreeNode* root = new TreeNode(-10);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);

    int maxSum = 0;
    vector<int> path = maxPathSum2(root, maxSum);

    cout << "Max Path Sum: " << maxSum << endl;
    cout << "Path: ";
    for (int val : path) {
        cout << val << " ";
    }
    cout << endl;
    return 0;
}

```
