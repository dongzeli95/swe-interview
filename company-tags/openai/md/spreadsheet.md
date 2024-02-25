# Spreadsheet

<figure><img src="../../../.gitbook/assets/Screenshot 2024-02-25 at 1.51.48 PM.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2024-02-25 at 1.51.55 PM.png" alt=""><figcaption></figcaption></figure>

<pre class="language-cpp"><code class="lang-cpp"><strong>#include &#x3C;string>
</strong>#include &#x3C;map>
#include &#x3C;iostream>
#include &#x3C;queue>
#include &#x3C;variant>
#include &#x3C;unordered_set>

using namespace std;

// 1. Update Parent/
// 2. parent can get to child using different path?

// Q: if a node with a subtree is added, are the nodes within the subtree already set in the graph?

class SpreadSheetBFS {
public:
    map&#x3C;string, variant&#x3C;int, pair&#x3C;string, string>>> m;
    SpreadSheetBFS() {}

    // Time: O(n)
    int getCell(string key) {
        if (!m.count(key)) {
            throw runtime_error("Key not found");
        }

        return bfs(key);
    }

    // Time: O(1)
    void setCell(string key, variant&#x3C;int, pair&#x3C;string, string>> val) {
        m[key] = val;
    }

    int bfs(string key) {
        queue&#x3C;string> q;
        q.push(key);

        int res = 0;
        while (!q.empty()) {
            string curr = q.front();
            q.pop();

            if (holds_alternative&#x3C;int>(m[curr])) {
                res += std::get&#x3C;int>(m[curr]);
            }
            else {
                auto&#x26; children = get&#x3C;pair&#x3C;string, string>>(m[curr]);
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
    map&#x3C;string, variant&#x3C;int, pair&#x3C;string, string>>> m;

    // Parent relationship
    unordered_map&#x3C;string, unordered_set&#x3C;string>> parents;
    // Values
    unordered_map&#x3C;string, int> values;

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
    void setCell(string key, variant&#x3C;int, pair&#x3C;string, string>> val) {
        pair&#x3C;int, vector&#x3C;string>> value = parse(val);
        if (!m.count(key)) {
            m[key] = val;
            values[key] = value.first;
            for (auto i: value.second) {
                parents[i].insert(key);
            }

            return;
        }

        variant&#x3C;int, pair&#x3C;string, string>> prevVal = m[key];
        pair&#x3C;int, vector&#x3C;string>> prevValue = parse(prevVal);

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

    pair&#x3C;int, vector&#x3C;string>> parse(variant&#x3C;int, pair&#x3C;string, string>> val) {
        if (holds_alternative&#x3C;int>(val)) {
            return {get&#x3C;int>(val), {}};
        } else {
            auto&#x26; children = get&#x3C;pair&#x3C;string, string>>(val);
            int value = values[children.first] + values[children.second];
            return {value, {children.first, children.second}};
        }
    }

    void updateParentValues(string key, int diff) {
        queue&#x3C;string> q;
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

    // cout &#x3C;&#x3C; "A: " &#x3C;&#x3C; ss.getCell("A") &#x3C;&#x3C; endl; // 6
    // cout &#x3C;&#x3C; "B: " &#x3C;&#x3C; ss.getCell("B") &#x3C;&#x3C; endl; // 7
    // cout &#x3C;&#x3C; "C: " &#x3C;&#x3C; ss.getCell("C") &#x3C;&#x3C; endl; // 13

    // ss.setCell("A", 13);
    // cout &#x3C;&#x3C; "C: " &#x3C;&#x3C; ss.getCell("C") &#x3C;&#x3C; endl; // 20

    // // C -> B, G
    // ss.setCell("C", make_pair("B", "G"));
    // ss.setCell("B", make_pair("G", "D"));
    // ss.setCell("G", make_pair("D", "F"));
    // ss.setCell("D", 1);
    // ss.setCell("F", 2);

    // cout &#x3C;&#x3C; "B: " &#x3C;&#x3C; ss.getCell("B") &#x3C;&#x3C; endl; // 4
    // cout &#x3C;&#x3C; "C: " &#x3C;&#x3C; ss.getCell("C") &#x3C;&#x3C; endl; // 7
    // cout &#x3C;&#x3C; "D: " &#x3C;&#x3C; ss.getCell("D") &#x3C;&#x3C; endl; // 1
    // cout &#x3C;&#x3C; "G: " &#x3C;&#x3C; ss.getCell("G") &#x3C;&#x3C; endl; // 3
    // cout &#x3C;&#x3C; "F: " &#x3C;&#x3C; ss.getCell("F") &#x3C;&#x3C; endl; // 2

    SpreadSheetBFSWithCache ss;
    ss.setCell("A", 6);
    ss.setCell("B", 7);
    ss.setCell("C", make_pair("A", "B"));

    cout &#x3C;&#x3C; "A: " &#x3C;&#x3C; ss.getCell("A") &#x3C;&#x3C; endl; // 6
    cout &#x3C;&#x3C; "B: " &#x3C;&#x3C; ss.getCell("B") &#x3C;&#x3C; endl; // 7
    cout &#x3C;&#x3C; "C: " &#x3C;&#x3C; ss.getCell("C") &#x3C;&#x3C; endl; // 13

    ss.setCell("A", 13);
    cout &#x3C;&#x3C; "C: " &#x3C;&#x3C; ss.getCell("C") &#x3C;&#x3C; endl; // 20

    // C -> B, G
    ss.setCell("D", 1);
    ss.setCell("F", 2);
    ss.setCell("G", make_pair("D", "F"));
    ss.setCell("B", make_pair("G", "D"));
    ss.setCell("C", make_pair("B", "G"));

    cout &#x3C;&#x3C; "B: " &#x3C;&#x3C; ss.getCell("B") &#x3C;&#x3C; endl; // 4
    cout &#x3C;&#x3C; "C: " &#x3C;&#x3C; ss.getCell("C") &#x3C;&#x3C; endl; // 7
    cout &#x3C;&#x3C; "D: " &#x3C;&#x3C; ss.getCell("D") &#x3C;&#x3C; endl; // 1
    cout &#x3C;&#x3C; "G: " &#x3C;&#x3C; ss.getCell("G") &#x3C;&#x3C; endl; // 3
    cout &#x3C;&#x3C; "F: " &#x3C;&#x3C; ss.getCell("F") &#x3C;&#x3C; endl; // 2



    // Cell A = Cell(6);
    // Cell B = Cell(7);
    // Cell C = Cell(13, "A", "B");
    // SpreadSheet sheet;
    // sheet.set("A", A);
    // sheet.set("B", B);
    // sheet.set("C", C);
    // int a = sheet.get("A");
    // cout &#x3C;&#x3C; a &#x3C;&#x3C; endl;

    // int b = sheet.get("B");
    // cout &#x3C;&#x3C; b &#x3C;&#x3C; endl;

    // int c = sheet.get("C");
    // cout &#x3C;&#x3C; c &#x3C;&#x3C; endl;

    // A.val = 13;
    // sheet.set("A", A);

    // c = sheet.get("C");
    // cout &#x3C;&#x3C; c &#x3C;&#x3C; endl;

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
    unordered_map&#x3C;string, Cell> m;

    SpreadSheet() {}
    int get(string key) {
        if (!m.count(key)) {
            throw;
        }
        return dfs(key);
    }

    int dfs(string key) {
        Cell cell = m[key];
        if (cell.child1.empty() &#x26;&#x26; cell.child2.empty()) {
            return cell.val;
        }

        int v1 = get(cell.child1);
        int v2 = get(cell.child2);
        return v1 + v2;
    }

    void set(string key, Cell cell) {
        m[key] = cell;
    }
};```
</code></pre>
