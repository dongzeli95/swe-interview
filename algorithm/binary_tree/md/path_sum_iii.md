```cpp
// https://leetcode.com/problems/path-sum-iii

/*
Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum.
The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).

Ex1:
Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
Output: 3
Explanation: The paths that sum to 8 are shown.

Ex2:
Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: 3

*/

#include <cassert>
#include <set>
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
void dfs(TreeNode* curr, multiset<long long>& prefixSum, int& target, long long& currSum, int& res) {
    if (!curr) {
        return;
    }

    currSum += curr->val;
    if (prefixSum.count(currSum-target)) {
        // Need to count all the occurences.
        res += prefixSum.count(currSum - target);
    }

    prefixSum.insert(currSum);
    dfs(curr->left, prefixSum, target, currSum, res);
    dfs(curr->right, prefixSum, target, currSum, res);
    prefixSum.erase(prefixSum.find(currSum));

    currSum -= curr->val;
}

int pathSum(TreeNode* root, int targetSum) {
    if (!root) {
        return 0;
    }

    multiset<long long> prefixSum;
    prefixSum.insert(0);
    long long currSum = 0;
    int res = 0;
    dfs(root, prefixSum, targetSum, currSum, res);
    return res;
}

int main() {
    TreeNode* root = new TreeNode(10);
    root->left = new TreeNode(5);
    root->right = new TreeNode(-3);
    root->left->left = new TreeNode(3);
    root->left->right = new TreeNode(2);
    root->left->left->left = new TreeNode(3);
    root->left->left->right = new TreeNode(-2);
    root->left->right->right = new TreeNode(1);
    root->right->right = new TreeNode(11);

    assert(pathSum(root, 8) == 3);

    // Test case 2: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
    root = new TreeNode(5);
    root->left = new TreeNode(4);
    root->right = new TreeNode(8);
    root->left->left = new TreeNode(11);
    root->right->left = new TreeNode(13);

    root->left->left->left = new TreeNode(7);
    root->left->left->right = new TreeNode(2);

    root->right->right = new TreeNode(4);
    root->right->right->left = new TreeNode(5);
    root->right->right->right = new TreeNode(1);

    assert(pathSum(root, 22) == 3);
    return 0;
}```
