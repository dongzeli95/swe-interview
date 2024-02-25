#include <string>
#include <map>
#include <iostream>
#include <queue>
#include <variant>
#include <unordered_set>

using namespace std;

// 1. Update Parent/
// 2. parent can get to child using different path?

// Q: if a node with a subtree is added, are the nodes within the subtree already set in the graph?

class SpreadSheetBFS {
public:
    map<string, variant<int, pair<string, string>>> m;
    SpreadSheetBFS() {}

    // Time: O(n)
    int getCell(string key) {
        if (!m.count(key)) {
            throw runtime_error("Key not found");
        }

        return bfs(key);
    }

    // Time: O(1)
    void setCell(string key, variant<int, pair<string, string>> val) {
        m[key] = val;
    }

    int bfs(string key) {
        queue<string> q;
        q.push(key);

        int res = 0;
        while (!q.empty()) {
            string curr = q.front();
            q.pop();

            if (holds_alternative<int>(m[curr])) {
                res += std::get<int>(m[curr]);
            }
            else {
                auto& children = get<pair<string, string>>(m[curr]);
                if (!children.first.empty()) {
                    q.push(children.first);
                }
                if (!children.second.empty()) {
                    q.push(children.second);
                }
            }
        }

        return res;
    }
};

class SpreadSheetBFSWithCache {
public:
    map<string, variant<int, pair<string, string>>> m;

    // Parent relationship
    unordered_map<string, unordered_set<string>> parents;
    // Values
    unordered_map<string, int> values;

    // Time: O(1)
    int getCell(string key) {
        if (!values.count(key)) {
            throw runtime_error("Key not found");
        }

        return values[key];
    }

    // Case 1: key doesn't exist: update parent relationship and val;
    // Case 2: key exist:
    // a. val -> children: update new value based on children, update parent relationship.
    // b. children->val
    // c. val->val
    // d. children -> children

    // Time: O(n)
    void setCell(string key, variant<int, pair<string, string>> val) {
        pair<int, vector<string>> value = parse(val);
        if (!m.count(key)) {
            m[key] = val;
            values[key] = value.first;
            for (auto i: value.second) {
                parents[i].insert(key);
            }

            return;
        }

        variant<int, pair<string, string>> prevVal = m[key];
        pair<int, vector<string>> prevValue = parse(prevVal);

        m[key] = val;
        // Invalidate previous parent relationship or keep track of value diff.
        for (auto i: prevValue.second) {
            parents[i].erase(key);
        }

        // Update parents relationship
        for (auto i: value.second) {
            parents[i].insert(key);
        }

        // Update downstream parent values using BFS.
        int valueDiff = value.first - prevValue.first;
        updateParentValues(key, valueDiff);
    }

    pair<int, vector<string>> parse(variant<int, pair<string, string>> val) {
        if (holds_alternative<int>(val)) {
            return {get<int>(val), {}};
        } else {
            auto& children = get<pair<string, string>>(val);
            int value = values[children.first] + values[children.second];
            return {value, {children.first, children.second}};
        }
    }

    void updateParentValues(string key, int diff) {
        queue<string> q;
        q.push(key);

        while (!q.empty()) {
            string curr = q.front();
            q.pop();

            values[curr] += diff;

            for (auto p : parents[curr]) {
                q.push(p);
            }
        }
    }

};   

int main() {

    // SpreadSheetBFS ss;
    // ss.setCell("A", 6);
    // ss.setCell("B", 7);
    // ss.setCell("C", make_pair("A", "B"));

    // cout << "A: " << ss.getCell("A") << endl; // 6
    // cout << "B: " << ss.getCell("B") << endl; // 7
    // cout << "C: " << ss.getCell("C") << endl; // 13

    // ss.setCell("A", 13);
    // cout << "C: " << ss.getCell("C") << endl; // 20

    // // C -> B, G
    // ss.setCell("C", make_pair("B", "G"));
    // ss.setCell("B", make_pair("G", "D"));
    // ss.setCell("G", make_pair("D", "F"));
    // ss.setCell("D", 1);
    // ss.setCell("F", 2);

    // cout << "B: " << ss.getCell("B") << endl; // 4
    // cout << "C: " << ss.getCell("C") << endl; // 7
    // cout << "D: " << ss.getCell("D") << endl; // 1
    // cout << "G: " << ss.getCell("G") << endl; // 3
    // cout << "F: " << ss.getCell("F") << endl; // 2

    SpreadSheetBFSWithCache ss;
    ss.setCell("A", 6);
    ss.setCell("B", 7);
    ss.setCell("C", make_pair("A", "B"));

    cout << "A: " << ss.getCell("A") << endl; // 6
    cout << "B: " << ss.getCell("B") << endl; // 7
    cout << "C: " << ss.getCell("C") << endl; // 13

    ss.setCell("A", 13);
    cout << "C: " << ss.getCell("C") << endl; // 20

    // C -> B, G
    ss.setCell("D", 1);
    ss.setCell("F", 2);
    ss.setCell("G", make_pair("D", "F"));
    ss.setCell("B", make_pair("G", "D"));
    ss.setCell("C", make_pair("B", "G"));

    cout << "B: " << ss.getCell("B") << endl; // 4
    cout << "C: " << ss.getCell("C") << endl; // 7
    cout << "D: " << ss.getCell("D") << endl; // 1
    cout << "G: " << ss.getCell("G") << endl; // 3
    cout << "F: " << ss.getCell("F") << endl; // 2



    // Cell A = Cell(6);
    // Cell B = Cell(7);
    // Cell C = Cell(13, "A", "B");
    // SpreadSheet sheet;
    // sheet.set("A", A);
    // sheet.set("B", B);
    // sheet.set("C", C);
    // int a = sheet.get("A");
    // cout << a << endl;

    // int b = sheet.get("B");
    // cout << b << endl;

    // int c = sheet.get("C");
    // cout << c << endl;

    // A.val = 13;
    // sheet.set("A", A);

    // c = sheet.get("C");
    // cout << c << endl;

    return 0;
}

class Cell {
public:
    int val;
    string child1;
    string child2;

    Cell() : val(0), child1(""), child2("") {}
    Cell(int val) : val(val), child1(""), child2("") {}
    Cell(int val, string child1, string child2) : val(val), child1(child1), child2(child2) {}
};

// A -> [B, C], C -> [D, E]
// Without Cache
class SpreadSheet {
public:
    unordered_map<string, Cell> m;

    SpreadSheet() {}
    int get(string key) {
        if (!m.count(key)) {
            throw;
        }
        return dfs(key);
    }

    int dfs(string key) {
        Cell cell = m[key];
        if (cell.child1.empty() && cell.child2.empty()) {
            return cell.val;
        }

        int v1 = get(cell.child1);
        int v2 = get(cell.child2);
        return v1 + v2;
    }

    void set(string key, Cell cell) {
        m[key] = cell;
    }
};