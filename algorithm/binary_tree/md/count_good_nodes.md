```cpp
// https://leetcode.com/problems/count-good-nodes-in-binary-tree

/*
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.
Return the number of good nodes in the binary tree.

Ex1:
Input: root = [3,1,4,3,null,1,5]
Output: 4
Explanation: Nodes in blue are good.
Root Node (3) is always a good node.
Node 4 -> (3,4) is the maximum value in the path starting from the root.
Node 5 -> (3,4,5) is the maximum value in the path
Node 3 -> (3,1,3) is the maximum value in the path.

Ex2:
Input: root = [3,3,null,4,2]
Output: 3
Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.

Ex3:
Input: root = [1]
Output: 1
Explanation: Root is considered as good.

*/

#include <cassert>

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
void dfs(TreeNode* curr, int mx, int& res) {
    if (!curr) {
        return;
    }

    int nextMx = mx;
    if (curr->val >= mx) {
        nextMx = curr->val;
        res++;
    }

    dfs(curr->left, nextMx, res);
    dfs(curr->right, nextMx, res);
}

int goodNodes(TreeNode* root) {
    if (!root) {
        return 0;
    }

    int res = 0;
    int mx = root->val;
    dfs(root, mx, res);
    return res;
}

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(1);
    root->right = new TreeNode(4);
    root->left->left = new TreeNode(3);
    root->right->left = new TreeNode(1);
    root->right->right = new TreeNode(5);
    assert(goodNodes(root) == 4);

    root = new TreeNode(3);
    root->left = new TreeNode(3);
    root->left->right = new TreeNode(2);
    root->left->left = new TreeNode(4);
    assert(goodNodes(root) == 3);

    root = new TreeNode(1);
    assert(goodNodes(root) == 1);

    return 0;
}

```
