#include <string>
#include <map>
#include <iostream>

using namespace std;

class Cell {
public:
    int val;
    string child1;
    string child2;

    Cell() : val(0), child1(""), child2("") {}
    Cell(int val): val(val), child1(""), child2("") {}
    Cell(int val, string child1, string child2) : val(val), child1(child1), child2(child2) {}
};

class Excel {
public:
    Excel(int H, char W) {
        m.clear();
        mat.resize(H, vector<int>(W - 'A', 0));
    }

    void set(int r, char c, int v) {
        if (m.count({ r, c })) m.erase({ r, c });
        mat[r - 1][c - 'A'] = v;
    }

    int get(int r, char c) {
        if (m.count({ r, c })) return sum(r, c, m[{r, c}]);
        return mat[r - 1][c - 'A'];
    }

    int sum(int r, char c, vector<string> strs) {
        int res = 0;
        for (string str : strs) {
            auto found = str.find_last_of(":");
            if (found == string::npos) {
                char y = str[0];
                int x = stoi(str.substr(1));
                res += get(x, y);
            }
            else {
                int x1 = stoi(str.substr(1, (int)found - 1)), y1 = str[0] - 'A';
                int x2 = stoi(str.substr(found + 2)), y2 = str[found + 1] - 'A';
                for (int i = x1; i <= x2; ++i) {
                    for (int j = y1; j <= y2; ++j) {
                        res += get(i, j + 'A');
                    }
                }
            }
        }
        m[{r, c}] = strs;
        return res;
    }

private:
    vector<vector<int>> mat;
    map<pair<int, char>, vector<string>> m;
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
        return v1+v2;
    }

    void set(string key, Cell cell) {
        m[key] = cell;
    }
};

// 1. Update Parent/
// 2. parent can get to child using different path?
class SpreadSheet2 {
public:
    unordered_map<string, Cell> m;
    unordered_map<string, int> vals;


    SpreadSheet2() {}
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

int main() {
    Cell A = Cell(6);
    Cell B = Cell(7);
    Cell C = Cell(13, "A", "B");
    SpreadSheet sheet;
    sheet.set("A", A);
    sheet.set("B", B);
    sheet.set("C", C);
    int a = sheet.get("A");
    cout << a << endl;

    int b = sheet.get("B");
    cout << b << endl;

    int c = sheet.get("C");
    cout << c << endl;

    A.val = 13;
    sheet.set("A", A);

    c = sheet.get("C");
    cout << c << endl;

    return 0;
}