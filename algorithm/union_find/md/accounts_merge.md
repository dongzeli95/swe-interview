```cpp
// https://leetcode.com/problems/accounts-merge/

/*
Given a list of accounts where each element accounts[i] is a list of strings, 
where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.
Now, we would like to merge these accounts. 
Two accounts definitely belong to the same person if there is some common email to both accounts. 
Note that even if two accounts have the same name, they may belong to different people as people could have the same name. 
A person can have any number of accounts initially, but all of their accounts definitely have the same name.
After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. 
The accounts themselves can be returned in any order.

Ex1:
Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Explanation:
The first and second John's are the same person as they have the common email "johnsmith@mail.com".
The third John and Mary are different people as none of their email addresses are used by other accounts.
We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'],
['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.

Ex2:
Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
*/

#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <cassert>
#include <iostream>

using namespace std;

class UnionFind {
public:
    // Amortized O(1)
    string find(string curr) {
        if (!parents.count(curr)) return curr;
        if (parents[curr] == curr) {
            return curr;
        }

        parents[curr] = find(parents[curr]);
        return parents[curr];
    }

    // Amortized O(1)
    void uni(string i, string j) {
        string p1 = find(i);
        string p2 = find(j);
        if (p1 != p2) {
            int s1 = sizes[p1];
            int s2 = sizes[p2];
            sizes[p2] = s1+s2;
            parents[p1] = p2;
        }
    }

private:
    unordered_map<string, string> parents;
    unordered_map<string, int> sizes;
};

// N accounts, each account have K emails
// Time: O(NK * Log(NK)), Space: O(NK)
vector<vector<string>> accountsMergeUF(vector<vector<string>>& accounts) {
    unordered_map<string, string> owner;
    int n = accounts.size();
    UnionFind uf = UnionFind();
    for (int i = 0; i < n; i++) {
        string name = accounts[i][0];
        int s = accounts[i].size();
        string email1 = accounts[i][1];
        owner[email1] = name;
        for (int j = 2; j < s; j++) {
            string e = accounts[i][j];
            uf.uni(email1, e);
            owner[e] = name;
        }
    }

    unordered_map<string, set<string>> clusters;
    for (auto i : owner) {
        string name = i.second;
        string email = i.first;
        string p = uf.find(email);
        clusters[p].insert(p);
        clusters[p].insert(email);
    }

    vector<vector<string>> res;
    for (auto i : clusters) {
        string p = i.first;
        string name = owner[p];
        vector<string> account = {name};
        copy(clusters[p].begin(), clusters[p].end(), back_inserter(account));
        res.push_back(account);
    }

    return res;
}

void dfs(unordered_map<string, vector<string>>& graph,
        unordered_set<string>& visited,
        vector<string>& res,
        string curr) {
    res.push_back(curr);
    for (string next: graph[curr]) {
        if (visited.count(next)) continue;
        visited.insert(next);
        dfs(graph, visited, res, next);
    }
}

// N accounts, each account have K emails
// Time: O(NK * Log(NK)), Space: O(NK)
// Although we have a for loop iterating through owner, the time complexity is bounded by graph which is NK.
vector<vector<string>> accountsMergeDFS(vector<vector<string>>& accounts) {
    unordered_map<string, vector<string>> graph;
    unordered_map<string, string> owner;
    
    int n = accounts.size();
    for (int i = 0; i < n; i++) {
        string name = accounts[i][0];
        int s = accounts[i].size();
        string email1 = accounts[i][1];
        owner[email1] = name;
        for (int j = 2; j < s; j++) {
            string e = accounts[i][j];
            graph[e].push_back(email1);
            graph[email1].push_back(e);
            owner[e] = name;
        }
    }

    unordered_set<string> visited;
    vector<vector<string>> res;
    for (auto i : owner) {
        string name = i.second;
        string email = i.first;
        if (visited.count(email)) continue;

        vector<string> emailCluster = {name};
        visited.insert(email);
        dfs(graph, visited, emailCluster, email);
        sort(emailCluster.begin()+1, emailCluster.end());
        res.push_back(emailCluster);
    }

    return res;
}

int main() {
    vector<vector<string>> accounts1 = {{"John","johnsmith@mail.com", "john_newyork@mail.com"},
                                        {"John","johnsmith@mail.com", "john00@mail.com"},
                                        {"Mary","mary@mail.com"},
                                        {"John", "johnnybravo@mail.com"} };
    vector<vector<string>> result1 = accountsMergeUF(accounts1);
    assert(result1.size() == 3);
    for (int i = 0; i < result1.size(); i++) {
        for (int j = 0; j < result1[i].size(); j++) {
            cout << result1[i][j] << " ";
        }
        cout << endl;
    }

    // Test Case 2
    vector<vector<string>> accounts2 = { {"Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"},
                                        {"Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"},
                                        {"Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"},
                                        {"Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"},
                                        {"Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"} };
    vector<vector<string>> result2 = accountsMergeUF(accounts2);
    for (int i = 0; i < result2.size(); i++) {
        for (int j = 0; j < result2[i].size(); j++) {
            cout << result2[i][j] << " ";
        }
        cout << endl;
    }


    cout << "All test cases passed!" << endl;
    return 0;
    
}```
