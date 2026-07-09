// https://leetcode.com/problems/distribute-coins-in-binary-tree/description/

/*
You are given the root of a binary tree with n nodes where each node in the tree has node.val coins. 
There are n coins in total throughout the whole tree.

In one move, we may choose two adjacent nodes and move one coin from one node to another. 
A move may be from parent to child, or from child to parent.

Return the minimum number of moves required to make every node have exactly one coin.

Ex1:
Input: root = [3,0,0]
Output: 2
Explanation: From the root of the tree, we move one coin to its left child, and one coin to its right child.

Ex2:
Input: root = [0,3,0]
Output: 3
Explanation: From the left child of the root, we move two coins to the root [taking two moves]. 
Then, we move one coin from the root of the tree to the right child.

*/

/*
Intuition
If the leaf of a tree has 0 coins (an excess of -1 from what it needs), 
then we should push a coin from its parent onto the leaf. 
If it has say, 4 coins (an excess of 3), then we should push 3 coins off the leaf. 
In total, the number of moves from that leaf to or from its parent is excess = Math.abs(num_coins - 1). 
Afterwards, we never have to consider this leaf again in the rest of our calculation.

Algorithm
We can use the above fact to build our answer. 
Let dfs(node) be the excess number of coins in the subtree at or below this node: namely, 
the number of coins in the subtree, minus the number of nodes in the subtree. 
Then, the number of moves we make from this node to and from its children is abs(dfs(node.left)) + abs(dfs(node.right)). 
After, we have an excess of node.val + dfs(node.left) + dfs(node.right) - 1 coins at this node.

*/

// Time:O(N), Space: O(H) 
int traverse(TreeNode* r, int& moves) {
    if (r == nullptr) return 0;
    int left = traverse(r->left, moves), right = traverse(r->right, moves);
    moves += abs(left) + abs(right);
    return r->val + left + right - 1;
}
int distributeCoins(TreeNode* r, int moves = 0) {
    traverse(r, moves);
    return moves;
}