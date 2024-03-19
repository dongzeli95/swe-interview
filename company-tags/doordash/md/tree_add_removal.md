```cpp
// 两个树的遍历，先统计不同的节点数量，再对不同节点分类， 哪些点是添加，哪些点是更改，哪些点是删除。

// At DoorDash, menus are updated daily even hourly to keep them up - to - date.Each menu can be regarded as a tree.When the merchant sends us the latest menu, can we calculate
// how many nodes have changed / added / deleted ?

// Assume each Node structure is as below :

// class Node {
//     String key;
//     int value;
//     List children;
// }

// Assume there are no duplicate nodes with the same key.

// Output: Return the number of changed nodes in the tree.

/*
// Existing tree
//       a(1)
//     /     \
//   b(2)      c(3)
//    / \          \     
// d(4)   e(5)      f(6)

// New tree
// a(1)
//   \
//  c(3)
//    \
//   f(66)

// a(1) a is the key, 1 is the value
// For example, there are a total of 4 changed nodes.Node b, Node d, Node e are automatically set to inactive.The value of Node f changed as well.

// Existing tree
//      a(1)
//     /    \
//   b(2‍‍‌‌‌‍‍‌‌‍‍‍‌‍‍‌‌‍)    c(3)
//    / \       \
// d(4)  e(5)   g(7)

// New tree
//         a(1)
//       /      \
//      b(2)     h(8)
//   /   |   \       \
// e(5) d(4) f(6)    g(7)

// There are a total of 5 changed nodes.Node f is a newly - added node.c(3) and old g(7) are deactivated and h(8) and g(7) are newly added nodes

// followup print out the changes
*/
#include <string>
#include <vector>
#include <iostream>

using namespace std;

class Node {
private:
    string key;
    int value;
    bool isActive;
    vector<Node*> children;

public:
    Node(string key, int value, bool isActive) {
        this->key = key;
        this->value = value;
        this->isActive = isActive;
    }

    // Destructor to properly clean up memory used by children nodes
    ~Node() {
        for (auto child : children) {
            delete child;
        }
    }

    // Add a child to the node
    void addChild(Node* child) {
        children.push_back(child);
    }

    // Check for equality
    bool equals(const Node* node) const {
        return this->key == node->key
            && this->value == node->value
            && this->isActive == node->isActive;
    }

    // Convert node to string
    string toString() const {
        return key;
    }

    // Getters for Node properties
    string getKey() const { return key; }
    int getValue() const { return value; }
    bool getIsActive() const { return isActive; }

    // Get children
    const vector<Node*>& getChildren() const {
        return children;
    }
};

class Menu {
public:
  int getModifiedItems(Node* oldMenu, Node* newMenu) {
    if (oldMenu == nullptr && newMenu == nullptr) {
        return 0;
    }

    int count = 0;
    if (oldMenu == nullptr || newMenu == nullptr || !oldMenu->equals(newMenu)) {
        // cout << oldMenu->toString() << " " << newMenu->toString() << endl;
        count++;
    }

    unordered_map<string, Node*> children1 = getChildNodes(oldMenu);
    unordered_map<string, Node*> children2 = getChildNodes(newMenu);

    for (auto i: children1) {
        string key = i.first;
        count += getModifiedItems(children1[key], children2[key]);
    }

    for (auto i: children2) {
        string key = i.first;
        count += getModifiedItems(children1[key], children2[key]);
    }

    return count;
  }

  unordered_map<string, Node*> getChildNodes(Node* menu) {
    unordered_map<string, Node*> res;
    if (!menu) {
        return res;
    }

    for (Node* n : menu->getChildren()) {
        res[n->toString()] = n;
    }

    return res;
  }
};

int main() {
    Node* a = new Node("a", 1, true);
    Node* b = new Node("b", 2, true);
    Node* c = new Node("c", 3, true);
    Node* d = new Node("d", 4, true);
    Node* e = new Node("e", 5, true);
    Node* g = new Node("g", 7, true);

    a->addChild(b);
    a->addChild(c);
    b->addChild(d);
    b->addChild(e);
    // c->addChild(g); // Commented out as in your Java code

    Node* a1 = new Node("a", 1, true);
    Node* b1 = new Node("b", 2, true);
    Node* c1 = new Node("c", 3, true);
    Node* d1 = new Node("d", 4, true);
    Node* e1 = new Node("e", 5, true);
    Node* f1 = new Node("f", 6, true);
    Node* g1 = new Node("g", 7, false);

    a1->addChild(b1);
    a1->addChild(c1);
    b1->addChild(d1);
    // b1->addChild(e1); // Commented out as in your Java code
    // b1->addChild(f1); // Commented out as in your Java code
    c1->addChild(e1);

    Menu menu;
    int count = menu.getModifiedItems(a, a1);
    cout << "Changed Items are: " << count << endl;

    // Memory cleanup
    delete a;
    delete a1;

    return 0;
}```
