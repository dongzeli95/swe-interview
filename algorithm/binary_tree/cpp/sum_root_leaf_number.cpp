// https://leetcode.com/problems/sum-root-to-leaf-numbers/

// You are given the root of a binary tree containing digits from 0 to 9 only.
// Each root - to - leaf path in the tree represents a number.
// For example, the root - to - leaf path 1 -> 2 -> 3 represents the number 123.
// Return the total sum of all root - to - leaf numbers.
// Test cases are generated so that the answer will fit in a 32 - bit integer.
// A leaf node is a node with no children.

//      2
//    /  \
//   3   4
//  / \
// 1   5

// 231+235+24

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

// Iterative, stack or queue.
// Time: O(n), Space: O(H)
int sumNumbersIterative(TreeNode* root) {
    if (!root) {
        return 0;
    }

    stack<pair<TreeNode*, int>> st;
    st.push({root, root->val});

    int res = 0;
    while (!st.empty()) {
        auto curr = st.top();
        st.pop();

        TreeNode* node = curr.first;

        int val = curr.second;
        if (!node->left && !node->right) {
            res += val;
        }
        if (node->left) {
            st.push({node->left, val*10 + node->left->val});
        }
        
        if (node->right) {
            st.push({node->right, val*10 + node->right->val});
        }
    }

    return res;
}

// Morris
/*
The idea of Morris algorithm is to set temporary link between the node and its predecessor.
predecessor.right = root.
If there is no link? set it and go to the left subtree.
If there is a link? break it and go to the right subtree.
*/

// Time: O(N), Space: O(1)
int sumNumbersMorris(TreeNode* root) {
    int rootToLeaf = 0, currNumber = 0;
    TreeNode* predecessor;

    while (root) {
        if (root->left) {
            // Finding the predecessor
            predecessor = root->left;
            int steps = 1;
            while (predecessor->right && predecessor->right != root) {
                predecessor = predecessor->right;
                ++steps;
            }

            // Making a temporary link and moving to the left subtree
            if (!predecessor->right) {
                currNumber = currNumber * 10 + root->val;
                predecessor->right = root;
                root = root->left;
            }
            // Breaking the temporary link and moving to the right subtree
            else {
                // If you're on a leaf, update the sum
                if (!predecessor->left) {
                    rootToLeaf += currNumber;
                }
                // Backtracking the current number
                for (int i = 0; i < steps; ++i) {
                    currNumber /= 10;
                }
                predecessor->right = nullptr;
                root = root->right;
            }
        }
        // If there is no left child, just go right
        else {
            currNumber = currNumber * 10 + root->val;
            // If you're on a leaf, update the sum
            if (!root->right) {
                rootToLeaf += currNumber;
            }
            root = root->right;
        }
    }

    return rootToLeaf;
}

// TODO: pre-order traversal, in-order traversal, post-order traversal.

// Time: O(n), Space: O(H)
void helper(TreeNode* curr, int& res, int sum) {
    if (!curr) {
        return;
    }

    sum += curr->val;
    if (!curr->left && !curr->right) {
        res += sum;
        return;
    }

    helper(curr->left, res, sum*10);
    helper(curr->right, res, sum*10);
}

int sumNumbers(TreeNode* root) {
    int res = 0;
    helper(root, res, 0);
    return res;
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    cout << sumNumbers(root) << endl;
    cout << sumNumbersIterative(root) << endl;
    cout << sumNumbersMorris(root) << endl;


    //      2
    //    /  \
    //   3   4
    //  / \
    // 1   5

    // 231+235+24
    TreeNode* root2 = new TreeNode(2);
    root2->left = new TreeNode(3);
    root2->right = new TreeNode(4);
    root2->left->left = new TreeNode(1);
    root2->left->right = new TreeNode(5);
    cout << sumNumbers(root2) << endl;
    cout << sumNumbersIterative(root2) << endl;
    cout << sumNumbersMorris(root2) << endl;

//     [5, 3, 2, 7, 0, 6, null, null, null, 0] , 6363
//      5
//     / \
//    3   2
//   / \  /
//  7  0  6
//     \
//      0
    return 0;
}