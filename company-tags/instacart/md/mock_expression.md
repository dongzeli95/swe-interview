```cpp
// 第三轮 coding 公式计算
// 第一小问 input : ["T2", ["T1 = 1", "T2 = T3", "T3 = T1"]] output : T2值   公式都是左边一个变量， 右边是变量或者数值
// 第二小问 input : ["T2", ["T1 = 1", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3]]  output:T2值
// 公式左边为变量，右边为一个或多个变量 / 数值，包括加减操作
// 第三小问： 在第二小问基础上可能存在解不出的情况
// 这道题我是用topological sort的方法，但后来发现Top - down 递归就够了
// 然后发现所有的变量都会有一个相应的赋值
// 比如这种情况的Testcase就不存在["T2", ["T1=4", "T1 = 2 + T2"]]

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <sstream>

using namespace std;

class Calculator {
public:
  Calculator(string target, vector<string>& exps) : expressions(exps), target(target) {}

  int dfs(string curr, unordered_map<string, string>& graph) {
    if (isdigit(curr[0])) {
        return stoi(curr);
    }

    return dfs(graph[curr], graph);
  }

  void trim(string& s) {
    int count = 0;
    int n = s.size();
    for (int i = 0; i < n; i++) {
        if (s[i] != ' ') {
            s[count++] = s[i];
        }
    }

    s = s.substr(0, count);
  }

  void constructGraph() {
    for (string& exp: expressions) {
        trim(exp);
        size_t equal = exp.find('=');
        string left = exp.substr(0, equal);
        string right = exp.substr(equal+1);
        graph[left] = right;
    }
  }

  void debugGraph() {
    for (auto i : graph) {
        cout << i.first << " " << i.second << endl;
    }
  }

  int cal() {
    constructGraph();
    debugGraph();
    return dfs(target, graph);
  }

  unordered_map<string, string> graph;
  vector<string> expressions;
  string target;
};

class CalculatorPart2 {
public:
    CalculatorPart2(string target, vector<string>& exps) : expressions(exps), target(target) {}

    string dfs(string curr, unordered_map<string, vector<string>>& graph, unordered_set<string>& visited) {
        if (isdigit(curr[0])) {
            return curr;
        }

        // Impossible to solve since we have no expression for this left hand string.
        if (!graph.count(curr)) {
            return "IMPOSSIBLE";
        }

        if (graph[curr].size() == 1 && isdigit(graph[curr][0][0])) {
            return graph[curr][0];
        }

        // Return computed cache
        // if (cache.count(curr)) {
        //     return cache[curr];
        // }

        // Part 3: detect cycle
        if (visited.count(curr)) {
            return "IMPOSSIBLE";
        }

        visited.insert(curr);

        int sum = 0;
        int sign = 1;
        for (auto i : graph[curr]) {
            if (i == "+") {
                sign = 1;
            } else if (i == "-") {
                sign = -1;
            } else {
                string s = dfs(i, graph, visited);
                // Part 3
                if (s == "IMPOSSIBLE") {
                    return s;
                }

                int val = stoi(s);
                sum += sign*val;
            }
        }

        return to_string(sum);
    }

    vector<string> split(string s) {
        vector<string> res;
        string current;

        for (char ch : s) {
            if (isdigit(ch) || isalpha(ch)) {
                current += ch;
            }
            else {
                if (!current.empty()) {
                    res.push_back(current);
                    current = "";
                }
                res.push_back(string(1, ch));
            }
        }

        if (!current.empty()) {
            res.push_back(current);
        }

        return res;
    }

    void trim(string& s) {
        int count = 0;
        int n = s.size();
        for (int i = 0; i < n; i++) {
            if (s[i] != ' ') {
                s[count++] = s[i];
            }
        }

        s = s.substr(0, count);
    }

    void constructGraph() {
        for (string& exp : expressions) {
            trim(exp);
            size_t equal = exp.find('=');
            string left = exp.substr(0, equal);
            string right = exp.substr(equal + 1);
            graph[left] = split(right);
        }
    }

    void debugGraph() {
        for (auto i : graph) {
            cout << "key: " <<  i.first << endl;
            for (auto j : i.second) {
                cout << j << " ";
            }
            cout << endl;
        }
    }

    string cal() {
        unordered_set<string> visited;
        constructGraph();
        // debugGraph();
        return dfs(target, graph, visited);
    }

    unordered_map<string, vector<string>> graph;
    vector<string> expressions;
    string target;
};


void test(vector<string> expressions, string target) {
    CalculatorPart2 expCalculator = CalculatorPart2(target, expressions);
    cout << expCalculator.cal() << endl;
}

int main() {
    test({ "T1 = 4", "T1 = 2 + T2" }, "T2"); // Impossible
    test({ "T1 = T2", "T2 = T1" }, "T2"); // Impossible
    test({ "T1 = T2", "T2 = T3", "T3 = 1+5-4" }, "T2"); // 1
    test({ "T1 = 1", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3" }, "T2"); // 0
    test({ "T1 = 1", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3" }, "T3"); // -3
    test({ "T1 = 1", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3" }, "T4"); // -2
    test({ "X6 = 36",
 "X1 = X9",
 "X10 = X7",
 "X7 = X2",
 "X4 = X9",
 "X2 = X6",
 "X3 = X6",
 "X5 = X2",
 "X9 = X8",
 "X8 = 63" }, "X10"); // 36

    return 0;
}

// Entity parseUtil(ifstream& file) {
//     vector<string> res;
//     string line;

//     // Parse index
//     getline(file, line);
//     int idx;
//     istringstream iss_idx(line);
//     iss_idx >> idx;

//     // Part 3
//     if (seen.count(idx)) {
//         vector<string> res;
//         // return Entity(-1, -1, -1, res);
//         return Entity(-1, -1, -1);
//     }
//     seen.insert(idx);

//     // Parse x, y
//     getline(file, line);
//     char delim;
//     int x, y;
//     istringstream iss(line);
//     iss >> delim >> x >> delim >> y >> delim;

//     Entity e = Entity(x, y, idx);

//     // Parse board portion, if digit means it's next chunk of entity.
//     while (!isdigit(file.peek()) && getline(file, line) && !line.empty()) {
//         // res.push_back(line);
//         e.add(line);
//     }

//     // return Entity(x, y, idx, res);
//     return e;
// }```
