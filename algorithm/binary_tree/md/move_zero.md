```cpp
// 要求只交换值，0只能移到substree，交换完成后，0不能有非0的node在subtree

/*
     1                                                              1
  /     \                                                          /  \
0       2                                                       3     2
 /        /\                 swap之后                         /          / \
3      0   0                                               0        4     0
       /\                                                              /  \
     4   5                                                          0     5
*/

#include <iostream>
#include <cassert>

using namespace std;

class TreeNode {
public:
    TreeNode* left;
    TreeNode* right;
    int val;

    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

void swap(TreeNode* root) {
    if (!root) return;

    bool needSwap = root->val == 0;
    if (root->left) {
        if (needSwap) {
            root->val = root->left->val;
            root->left->val = 0;
            needSwap = false;
        }

        swap(root->left);
    }

    if (root->right) {
        if (needSwap) {
            root->val = root->right->val;
            root->right->val = 0;
        }

        swap(root->right);
    }
}

TreeNode* swapZero(TreeNode* root) {
    if (!root) {
        return nullptr;
    }

    swap(root);
    return root;
}

void printTree(TreeNode* root) {
    if (!root) return;

    printTree(root->left);
    cout << root->val << " ";
    printTree(root->right);
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(0);
    root->right = new TreeNode(2);
    root->left->left = new TreeNode(3);
    root->right = new TreeNode(2);
    root->right->left = new TreeNode(0);
    root->right->right = new TreeNode(0);
    root->right->left->left = new TreeNode(4);
    root->right->left->right = new TreeNode(5);

    printTree(root);

    TreeNode* res = swapZero(root);
    printTree(res);

    return 0;
}```
