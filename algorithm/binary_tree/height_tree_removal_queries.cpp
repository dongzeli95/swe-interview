// https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/description/

/*
You are given the root of a binary tree with n nodes. Each node is assigned a unique value from 1 to n. 
You are also given an array queries of size m.

You have to perform m independent queries on the tree where in the ith query you do the following:

Remove the subtree rooted at the node with the value queries[i] from the tree. It is guaranteed that queries[i] will not be equal to the value of the root.
Return an array answer of size m where answer[i] is the height of the tree after performing the ith query.

Note:

The queries are independent, so the tree returns to its initial state after each query.
The height of a tree is the number of edges in the longest simple path from the root to some node in the tree.

Ex1:
Input: root = [1,3,4,2,null,6,5,null,null,null,null,null,7], queries = [4]
Output: [2]
Explanation: The diagram above shows the tree after removing the subtree rooted at node with value 4.
The height of the tree is 2 (The path 1 -> 3 -> 2).

Ex2:
Input: root = [5,8,9,2,1,3,7,4,6], queries = [3,2,4,8]
Output: [3,2,3,2]
Explanation: We have the following queries:
- Removing the subtree rooted at node with value 3. The height of the tree becomes 3 (The path 5 -> 8 -> 2 -> 4).
- Removing the subtree rooted at node with value 2. The height of the tree becomes 2 (The path 5 -> 8 -> 1).
- Removing the subtree rooted at node with value 4. The height of the tree becomes 3 (The path 5 -> 8 -> 2 -> 6).
- Removing the subtree rooted at node with value 8. The height of the tree becomes 2 (The path 5 -> 9 -> 3).

*/

// /**
//  * Definition for a binary tree node.
//  * struct TreeNode {
//  *     int val;
//  *     TreeNode *left;
//  *     TreeNode *right;
//  *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
//  *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
//  *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
//  * };
//  */
 // https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/solutions/2769465/c-height-and-depth-easy-solution/

#include <unordered_map>

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
unordered_map<int, int> lhs;
unordered_map<int, int> rhs;
unordered_map<int, int> queryResult;

int height(TreeNode* root) {
    if (!root) {
        return -1;
    }

    int l = height(root->left);
    int r = height(root->right);
    lhs[root->val] = l;
    rhs[root->val] = r;
    int res = 1 + max(l, r);
    return res;
}

// solving the height of tree for removing each node.
void solve(TreeNode* root, int depth, int mx) {
    if (!root) return;

    queryResult[root->val] = mx + 1;
    solve(root->left, depth + 1, max(mx, rhs[root->val] + depth));
    solve(root->right, depth + 1, max(mx, lhs[root->val] + depth));
}

vector<int> treeQueries(TreeNode* root, vector<int>& queries) {
    if (queries.empty()) {
        return {};
    }

    height(root);
    solve(root->left, 1, rhs[root->val]);
    solve(root->right, 1, lhs[root->val]);

    vector<int> res;
    for (int i = 0; i < queries.size(); i++) {
        res.push_back(queryResult[queries[i]]);
    }
    return res;
}

// Brute force
// Time: O(q*n), Space: O(n)
class Solution {
public:
    unordered_map<int, int> heights;
    unordered_map<int, pair<TreeNode*, bool>> parents;

    void assignParents(TreeNode* root, TreeNode* parent, bool isRight) {
        if (!root) {
            return;
        }
        parents[root->val] = make_pair(parent, isRight);
        assignParents(root->left, root, false);
        assignParents(root->right, root, true);
    }

    int height(TreeNode* root) {
        if (!root) {
            return -1;
        }

        int l = height(root->left);
        int r = height(root->right);
        int res = 1 + max(l, r);
        return res;
    }

    vector<int> treeQueries(TreeNode* root, vector<int>& queries) {
        if (queries.empty()) {
            return {};
        }

        TreeNode* rootParent = new TreeNode(-1);
        assignParents(root, rootParent, false);
        height(root);

        // check heights
        // for (auto i: heights) {
        //     cout << i.first << " heights: " << i.second << endl;
        // }

        vector<int> res;
        // Handle queries.
        for (int i = 0; i < queries.size(); i++) {
            int v = queries[i];
            pair<TreeNode*, bool> p = parents[v];
            TreeNode* parent = p.first;
            bool isRight = p.second;

            // Handle the root
            if (parent == rootParent) {
                res.push_back(0);
                continue;
            }

            if (heights.count(v)) {
                res.push_back(heights[v]);
                continue;
            }

            TreeNode* tmp = nullptr;
            if (isRight) {
                tmp = parent->right;
                parent->right = nullptr;
            }
            else {
                tmp = parent->left;
                parent->left = nullptr;
            }

            int h = height(root);
            res.push_back(h);
            heights[v] = h;

            // Recover the tree
            if (isRight) {
                parent->right = tmp;
            }
            else {
                parent->left = tmp;
            }
        }

        return res;
    }
};