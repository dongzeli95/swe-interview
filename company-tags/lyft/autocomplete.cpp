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
            if (!curr->children[p[i] - 'a']) {
                curr->children[p[i] - 'a'] = new TrieNode();
            }

            curr = curr->children[p[i] - 'a'];
        }

        curr->isWord = true;
        curr->val = p;
    }

    void dfs(TrieNode* curr, vector<string>& res) {
        if (curr->isWord) {
            res.push_back(curr->val);
        }

        for (int i = 0; i < 26; i++) {
            if (!curr->children[i]) continue;
            dfs(curr->children[i], res);
        }
    }

    vector<string> searchWords(string str) {
        curr = root;

        for (int i = 0; i < str.size(); i++) {
            if (!curr->children[str[i] - 'a']) return {};
            curr = curr->children[str[i] - 'a'];
        }

        vector<string> res;
        dfs(curr, res);

        return res;
    }
private:
    TrieNode* root;
    TrieNode* curr;
};

// Time: O(M): number of character in products.
// Space: O(26n) n is the number of nodes in trie, we also output a number of strings, so it would be O(len(products))
vector<vector<string>> suggestedProducts(vector<string>& products, vector<string>& searchWords) {
    vector<vector<string>> res;
    if (products.empty() || searchWords.empty()) {
        return res;
    }

    Trie t = Trie();
    int n = products.size();
    for (int i = 0; i < n; i++) {
        t.addProduct(products[i]);
    }

    int m = searchWords.size();
    for (int i = 0; i < m; i++) {
        res.push_back(t.searchWords(searchWords[i]));
    }

    return res;
}

void debug(vector<vector<string>>& res) {
    for (int i = 0; i < res.size(); i++) {
        for (int j = 0; j < res[i].size(); j++) {
            cout << res[i][j] << " ";
        }
        cout << endl;
    }
}

vector<string> parse(int n) {
    vector<string> res;
    string line;
    for (int i = 0; i < n; i++) {
        getline(cin, line);
        res.push_back(line);
    }

    return res;
}

vector<vector<string>> parseStdin() {
    vector<vector<string>> res;

    string line;
    getline(cin, line);
    int n = stoi(line);
    vector<string> dicts = parse(n);

    getline(cin, line);
    n = stoi(line);
    vector<string> searchWords = parse(n);
    return vector<vector<string>> {dicts, searchWords};
}

int main() {
    // vector<string> products1 = { "mobile","mouse","moneypot","monitor","mousepad" };
    // vector<string> searchWords1 = {"mo", "mon"};
    // vector<vector<string>> res = suggestedProducts(products1, searchWords1);
    // debug(res);

    // vector<string> products2 = { "havana" };
    // vector<string> searchWords2 = {"hi"};
    // res = suggestedProducts(products2, searchWords2);
    // debug(res);

    vector<vector<string>> inputs = parseStdin();
    vector<vector<string>> res = suggestedProducts(inputs[0], inputs[1]);
    debug(res);

    return 0;
}

