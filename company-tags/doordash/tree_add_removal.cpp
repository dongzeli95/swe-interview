// At DoorDash, menus are updated daily even hourly to keep them up-to-date. Each menu can be regarded as a tree.
// When the merchant sends us the latest menu, can we calculate how many nodes has changed?

// Assume there are no duplicate nodes with the same key.

// Output: Return the number of changed nodes in the tree.

// Example 1
// Existing Menu in our system:

// Existing tree
//                           a(1, T)
//                           /     \
//                    b(2, T)     c(3, T)
//                      / \              \
//            d(4, T) e(5, T)        f(6, T)
//
// Legend: In "a(1, T)", a is the key, 1 is the value, T is True for active status 

// New Menu sent by the Merchant:

// New tree
//                  a(1, T)
//                     |
//                  c(3, F)
//                     |
//                 f(66, T)
//
// Expected Answer: 5 Explanation: Node b, Node d, Node e are automatically set to inactive.
// The active status of Node c and the value of Node f changed as well.

// Example 2
// Existing Menu in our system:

// Existing tree
//                           a(1, T)
//                            /    \
//                    b(2, T)      c(3, T)
//                       / \           \
//             d(4, T) e(5, T)     g(7, T)
// New Menu sent by the Merchant:

// New tree
//                         a(1, T)
//                       /          \
//                 b(2, T)         c(3, T)
//                /  |    \              \
//       d(4, T) e(5, T)  f(6, T)      g(7, F)
//
// Expected Answer: 2 Explanation: Node f is a newly-added node. Node g changed from Active to inactive
// follow - up是输出变化的节点。具体可以参考这个帖子

#include <string>
#include <vector>
#include <iostream>

using namespace std;

class Node {
public:
    string key;
    int val;
    bool isActive;

    vector<Node*> children;
    Node(string k, int v): key(k), val(v), isActive(true) {}
    Node(string k, int v, bool active) : key(k), val(v), isActive(active) {}

    void addChild(Node* n) {
        children.push_back(n);
    } 
};

int count(Node* n) {
    if (!n) {
        return 0;
    }

    int res = 1;
    for (Node* child : n->children) {
        res += count(child);
    }

    return res;
} 

int findDiffNodes(Node* oldMenu, Node* newMenu) {
    // Both trees are empty, they are the same tree
    if (!oldMenu && !newMenu) {
        return 0;
    }
    // Only one of the trees is not null
    // Or if the key of both trees are different, then return
    // the node count of both trees (which could be zero or one of them)
    if ((!oldMenu && newMenu)
    || (!newMenu && oldMenu)
    || (newMenu->key != oldMenu->key)) {
        return count(oldMenu) + count(newMenu);
    }

    int res = 0;
    // If their values are different
    // Then we include the current nodes of the two trees as the only diff and then
    // compute the diff of the children
    if (oldMenu->val != newMenu->val) {
        res += 1;
    } else if (oldMenu->isActive != newMenu->isActive) {
        res += 1;
    }

    unordered_map<string, Node*> m1;
    for (Node* n : oldMenu->children) {
        m1[n->key] = n;
    }
    unordered_map<string, Node*> m2;
    for (Node* n : newMenu->children) {
        m2[n->key] = n;
    }

    for (auto i : m1) {
        if (!m2.count(i.first)) {
            res += count(i.second);
        } else {
            Node* child2 = m2[i.first];
            res += findDiffNodes(i.second, child2);
            m2.erase(i.first);
        }
    }

    for (auto i : m2) {
        res += count(i.second);
    }

    return res;
}

int main() {
    // Example 1
// Existing Menu in our system:

// Existing tree
//                           a(1, T)
//                           /     \
//                    b(2, T)     c(3, T)
//                      / \             \
//            d(4, T) e(5, T)        f(6, T)
//
// Legend: In "a(1, T)", a is the key, 1 is the value, T is True for active status 

// New Menu sent by the Merchant:

// New tree
//                  a(1, T)
//                     |
//                  c(3, F)
//                     |
//                 f(66, T)
//
// Expected Answer: 5 Explanation: Node b, Node d, Node e are automatically set to inactive.
// The active status of Node c and the value of Node f changed as well.

    Node* a = new Node("a", 1, true);
    Node* b = new Node("b", 2, true);
    Node* c = new Node("c", 3, true);
    Node* d = new Node("d", 4, true);
    Node* e = new Node("e", 5, true);
    Node* f = new Node("f", 6, true);

    // Existing tree
    a->addChild(b);
    a->addChild(c);
    b->addChild(d);
    b->addChild(e);
    c->addChild(f);

    Node* a1 = new Node("a", 1, true);
    Node* c1 = new Node("c", 3, false);
    Node* f1 = new Node("f", 66, true);

    a1->addChild(c1);
    c1->addChild(f1);

    cout << findDiffNodes(a1, a) << endl;

// Example 2
// Existing Menu in our system:

// Existing tree
//                           a(1, T)
//                            /    \
//                    b(2, T)      c(3, T)
//                       / \           \
//             d(4, T) e(5, T)     g(7, T)
// New Menu sent by the Merchant:

// New tree
//                         a(1, T)
//                       /          \
//                 b(2, T)         c(3, T)
//                /  |    \              \
//       d(4, T) e(5, T)  f(6, T)      g(7, F)
//
// Expected Answer: 2 Explanation: Node f is a newly-added node. Node g changed from Active to inactive

    Node* a3 = new Node("a", 1, true);
    Node* b3 = new Node("b", 2, true);
    Node* c3 = new Node("c", 3, true);
    Node* d3 = new Node("d", 4, true);
    Node* e3 = new Node("e", 5, true);
    Node* g3 = new Node("g", 7, true);
    a3->addChild(b3);
    a3->addChild(c3);
    b3->addChild(d3);
    b3->addChild(e3);
    c3->addChild(g3);

    Node* a4 = new Node("a", 1, true);
    Node* b4 = new Node("b", 2, true);
    Node* c4 = new Node("c", 3, true);
    Node* d4 = new Node("d", 4, true);
    Node* e4 = new Node("e", 5, true);
    Node* f4 = new Node("f", 6, true);
    Node* g4 = new Node("g", 7, false);
    a4->addChild(b4);
    a4->addChild(c4);
    b4->addChild(d4);
    b4->addChild(e4);
    b4->addChild(f4);
    c4->addChild(g4);

    cout << findDiffNodes(a4, a3) << endl;

    return 0;
}