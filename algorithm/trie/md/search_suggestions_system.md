```cpp
// https://leetcode.com/problems/search-suggestions-system

/*
You are given an array of strings products and a string searchWord.
Design a system that suggests at most three product names from products after each character of searchWord is typed. 
Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimums products.
Return a list of lists of the suggested products after each character of searchWord is typed.

Ex1:
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
After typing mou, mous and mouse the system suggests ["mouse","mousepad"].

Ex2:
Input: products = ["havana"], searchWord = "havana"
Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
Explanation: The only word "havana" will be always suggested while typing the search word.

*/

#include <vector>
#include <string>
#include <cassert>
#include <iostream>

using namespace std;

class TrieNode {
public:
    bool isWord;
    string val;
    vector<TrieNode*> children;

    TrieNode() {
        isWord = false;
        val = "";
        children = vector<TrieNode*>(26, nullptr);
    }
};

class Trie {
public:
    Trie() {
        root = new TrieNode();
        curr = nullptr;
    }

    void addProduct(string p) {
        TrieNode* curr = root;
        int n = p.size();
        for (int i = 0; i < n; i++) {
            if (!curr->children[p[i]-'a']) {
                curr->children[p[i]-'a'] = new TrieNode();
            }

            curr = curr->children[p[i]-'a'];
        }

        curr->isWord = true;
        curr->val = p;
    }

    void dfs(TrieNode* curr, vector<string>& res) {
        if (res.size() == 3) {
            return;
        }

        if (curr->isWord) {
            res.push_back(curr->val);
        }

        for (int i = 0; i < 26; i++) {
            if (!curr->children[i]) continue;
            dfs(curr->children[i], res);
        }
    }

    vector<string> searchWords(char c) {
        if (!curr) {
            curr = root;
        }

        if (!curr->children[c-'a']) {
            return {};
        }

        curr = curr->children[c-'a'];
        vector<string> res;
        dfs(curr, res);

        return res;
    }
private:
    TrieNode* root;
    TrieNode* curr;
};

vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
    vector<vector<string>> res;
    if (products.empty() || searchWord.empty()) {
        return res;
    }

    Trie t = Trie();
    int n = products.size();
    for (int i = 0; i < n; i++) {
        t.addProduct(products[i]);
    }

    int m = searchWord.size();
    for (int i = 0; i < m; i++) {
        res.push_back(t.searchWords(searchWord[i]));
    }

    return res;
}

int main() {
    vector<string> products1 = {"mobile","mouse","moneypot","monitor","mousepad"};
    string searchWord1 = "mouse";
    vector<vector<string>> res = suggestedProducts(products1, searchWord1);
    vector<vector<string>> expected = { {"mobile","moneypot","monitor"},{"mobile","moneypot","monitor"},{"mouse","mousepad"},{"mouse","mousepad"},{"mouse","mousepad"} };
    assert(res == expected);

    vector<string> products2 = {"havana"};
    string searchWord2 = "havana";
    res = suggestedProducts(products2, searchWord2);
    expected = { {"havana"},{"havana"},{"havana"},{"havana"},{"havana"},{"havana"} };
    assert(res == expected);
    
    return 0;
}

```
