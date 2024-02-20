// https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/description/
/*
Given the root of a binary tree, return the number of nodes where the value of the node is equal to the average of the values in its subtree.

Note:

The average of n elements is the sum of the n elements divided by n and rounded down to the nearest integer.
A subtree of root is a tree consisting of root and all of its descendants.

Ex1:
Input: root = [4,8,5,0,1,null,6]
Output: 5
Explanation:
For the node with value 4: The average of its subtree is (4 + 8 + 5 + 0 + 1 + 6) / 6 = 24 / 6 = 4.
For the node with value 5: The average of its subtree is (5 + 6) / 2 = 11 / 2 = 5.
For the node with value 0: The average of its subtree is 0 / 1 = 0.
For the node with value 1: The average of its subtree is 1 / 1 = 1.
For the node with value 6: The average of its subtree is 6 / 1 = 6.

Ex2:
Input: root = [1]
Output: 1
Explanation: For the node with value 1: The average of its subtree is 1 / 1 = 1.

*/

#include <tuple>
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

// Time: O(n), Space: O(n)
pair<int, int> helper(TreeNode* curr, int& res) {
    // base case
    if (!curr) {
        return { 0, 0 };
    }

    pair<int, int> l = helper(curr->left, res);
    pair<int, int> r = helper(curr->right, res);
    int numOfNodes = l.second + r.second + 1;
    int sum = l.first + r.first + curr->val;
    int avg = sum / numOfNodes;
    if (avg == curr->val) res++;
    return { sum, numOfNodes };
}
int averageOfSubtree(TreeNode* root) {
    int res = 0;
    helper(root, res);
    return res;
}