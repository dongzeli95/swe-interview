```cpp
// Preorder traversal
#include <vector>
#include <iostream>
#include <stack>

using namespace std;

class TreeNode {
public:
    TreeNode* left;
    TreeNode* right;
    int val;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

void preorderIterative(TreeNode* root) {
    if (!root) {
        return;
    }

    stack<TreeNode*> st;
    st.push(root);

    while (!st.empty()) {
        TreeNode* curr = st.top();
        st.pop();

        cout << curr->val << endl;

        if (curr->right) {
            st.push(curr->right);
        }

        if (curr->left) {
            st.push(curr->left);
        }
    }
}

void inorderIterative(TreeNode* root) {
    stack<TreeNode*> st;
    TreeNode* curr = root;

    while (curr || !st.empty()) {
        while (curr) {
            st.push(curr);
            curr = curr->left;
        }

        curr = st.top();
        st.pop();
        cout << curr->val << endl;

        curr = curr->right;
    }
}

// [3, 4, 2, ]
void postorderIterative(TreeNode* root) {
    if (!root) return;

    stack<TreeNode*> s;
    s.push(root);
    TreeNode* head = root;
    while (!s.empty()) {
        TreeNode* t = s.top();
        if ((!t->left && !t->right) || t->left == head || t->right == head) {
            cout << t->val << endl;
            s.pop();
            head = t;
        }
        else {
            if (t->right) s.push(t->right);
            if (t->left) s.push(t->left);
        }
    }
}

// [1, 3, 2, 5, 4]

//         1
//       /  \
//      2    3
//     /\    /\
//    4  5

// 1, 2, 4, 5, 3

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);

    TreeNode* root2 = new TreeNode(3);
    root2->left = new TreeNode(2);
    root2->right = new TreeNode(4);
    root2->right->left = new TreeNode(1);

    // preorderIterative(root);
    // cout << endl << endl;

    // inorderIterative(root); // 4 2, 5, 1, 3
    // cout << endl << endl;

    // postorderIterative(root); // 4, 5, 2, 3, 1
    // cout << endl << endl;

    postorderIterative(root2);
    cout << endl << endl;

    return 0;
}```
