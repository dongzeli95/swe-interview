```cpp
// https://leetcode.com/problems/implement-trie-prefix-tree

/*
A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:
Trie() Initializes the trie object.
void insert(String word) Inserts the string word into the trie.
boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.

Ex1:
Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True

*/

#include <string>
#include <vector>
#include <cassert>
#include <iostream>

using namespace std;

class TrieNode {
public:
    vector<TrieNode*> children;
    bool isWord;

    TrieNode() {
        children = vector<TrieNode*>(26, nullptr);
        isWord = false;
    }
};

// n is the number of nodes in the trie.
// k is the total number of unique characters in the alphabet.
// Total Space: O(n*k)
class Trie {
public:
    TrieNode* root;
    Trie() {
        root = new TrieNode();
    }

    // Time: O(n), Space: O(n)
    void insert(string word) {
        TrieNode* curr = root;
        int n = word.size();
        for (int i = 0; i < n; i++) {
            if (!curr->children[word[i] - 'a']) {
                curr->children[word[i] - 'a'] = new TrieNode();
            }
            curr = curr->children[word[i] - 'a'];
        }

        curr->isWord = true;
    }

    bool search(string word) {
        TrieNode* res = find(word);
        return (res && res->isWord);
    }

    bool startsWith(string prefix) {
        TrieNode* res = find(prefix);
        return res != nullptr;
    }

    // Time: O(n), Space: O(1)
    TrieNode* find(string word) {
        TrieNode* curr = root;
        int n = word.size();
        for (int i = 0; i < n; i++) {
            TrieNode* next = curr->children[word[i] - 'a'];
            if (!next) {
                return nullptr;
            }
            curr = next;
        }

        return curr;
    }
};

int main() {
    Trie trie = Trie();
    trie.insert("apple");
    assert(trie.search("apple") == true);
    assert(trie.search("app") == false);
    assert(trie.startsWith("app") == true);
    trie.insert("app");
    assert(trie.search("app") == true);
}
```
