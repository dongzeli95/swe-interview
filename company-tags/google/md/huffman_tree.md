```cpp
/*

构建霍夫曼树，input是一个mapping, key是char, value是指char所对应编码的位数
假如我们有一套编码：e用0代替，b用10代替，z用11代替，那么我们的输入为
{e:1, b:2, z:2}
这个tree应该构建为, 如果两个char的编码长度相同，那么字母小的放在左侧，只考虑对a-z和A-Z进行编码
   *
  / \
e   *
    /  \
   b   z
问该如何构建这个tree

ZIP encodes data using binary prefix trees (aka Huffman trees):
1.Values can only appear at the leaves of the tree
2.To decode a file, we read bits from the file, use them to follow a path in the tree to a leaf, which determines a value:
    a.We start at the root of the tree
    b.When encountering a 0 bit, we descend to the left child, and when encountering a 1 bit we descend to the right child
    c.When reaching a leaf, we emit the value stored in the leaf

To save the tree efficiently in ZIP files, we save a mapping from byte-value to bit-length. For example:
{'b': 2, 'e': 1, 'z': 2 }

To make sure the mapping only represents a single tree, the tree must satisfy the following properties:
    1.Short paths (in the tree) are to the left of long paths
    2.Within the same length, smaller values appear to the left of larger values (so 'b' to the left of 'z', etc.)
The main question: Given the encoding (byte->length mapping), construct a valid tree. Analyze the runtime complexity.
*/

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <map>

using namespace std;

struct TreeNode {
    char data;
    TreeNode* left, * right;
    TreeNode(char data) {
        this->data = data;
        this->left = this->right = nullptr;
    }
};

// Function to build the Huffman tree
TreeNode* buildTree(map<char, int>& encoding) {
    // Create a priority queue to store live nodes of the Huffman tree
    auto compare = [&](TreeNode* a, TreeNode* b) -> bool {
        if (encoding[a->data] == encoding[b->data]) {
            return a->data > b->data; // small char first
        }
        return encoding[a->data] < encoding[b->data]; // longer encoding first
    };

    priority_queue<TreeNode*, vector<TreeNode*>, decltype(compare)> pq(compare);

    // Create a leaf node for each character and add it to the priority queue
    for (auto& pair : encoding) {
        pq.push(new TreeNode(pair.first));
    }

    // do till there is more than one node in the queue
    while (!pq.empty()) {
        // Remove the two nodes of the highest priority (lowest frequency) from the queue
        TreeNode* left = pq.top(); pq.pop();
        TreeNode* right = pq.top(); pq.pop();

        cout << left->data << " " << right->data << endl;

        // Create a new internal node with these two nodes as children and with a frequency equal to the sum of both nodes' frequencies.
        // Add the new node to the priority queue.
        TreeNode* node = new TreeNode('*');
        node->left = left;
        node->right = right;
        pq.push(node);
    }

    // The remaining node is the root node and the tree is complete.
    return pq.top();
}

// Function to print the tree for visualization
void printTree(TreeNode* root, string prefix = "") {
    if (root == nullptr) {
        return;
    }

    bool isLeaf = root->left == nullptr && root->right == nullptr;
    cout << prefix << (isLeaf ? "|__ " : "|-- ") << root->data << endl;

    printTree(root->left, prefix + (isLeaf ? "    " : "|   "));
    printTree(root->right, prefix + (isLeaf ? "    " : "|   "));
}

int main() {
    map<char, int> encoding = { {'e', 1}, {'b', 2}, {'z', 2} };
    TreeNode* root = buildTree(encoding);
    printTree(root);
    return 0;
}```
