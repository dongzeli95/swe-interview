// 第三轮 coding 公式计算
// 第一小问 input : ["T2", ["T1 = 1", "T2 = T3", "T3 = T1"]] output : T2值   公式都是左边一个变量， 右边是变量或者数值
// 第二小问 input : ["T2", ["T1 = 1", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3]]  output:T2值
// 公式左边为变量，右边为一个或多个变量 / 数值，包括加减操作
// https://leetcode.com/playground/muocUhbv

#include <string>
#include <iostream>
#include <unordered_set>
#include <sstream>

using namespace std;

// Q1: Are there any case where we have multiple T sign on the right hand side: T3 = T1 + 4 + T2...
// Q2: Are there going to be case where one of the T sign is on the right hand side but it doesn't have a expression for a value.
// T3 = T1 + T2, T1 = 2

class ExpressionCalculator {
public:
    ExpressionCalculator(vector<string>& expressions) {
        this->expressions = expressions;
        constructGraph();
    }

    vector<string> split(string str) {
        istringstream iss(str);

        char space;
        string sign;
        string str1 = "";
        string str2 = "";
        iss >> str1 >> sign >> str2;

        vector<string> res;
        res.push_back(str1);
        if (!sign.empty()) res.push_back(sign);
        if (!str2.empty()) res.push_back(str2);
        return res;
    }

    void constructGraph() {
        for (int i = 0; i < expressions.size(); i++) {
            string exp = expressions[i];
            size_t equal_pos = exp.find('=');
            string left = exp.substr(0, equal_pos - 1);
            string right = exp.substr(equal_pos + 2);
            graph[left] = split(right);
        }
    }

    string dfs(string curr, unordered_set<string>& visited, unordered_map<string, string>& cache) {
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
        if (cache.count(curr)) {
          return cache[curr];
        }

        // Detect cycle
        if (visited.count(curr)) {
            return "IMPOSSIBLE";
        }

        visited.insert(curr);

        int sum = 0;
        int sign = 1;
        for (string i : graph[curr]) {
            if (i == "+") {
                sign = 1;
            } else if (i == "-") {
                sign = -1;
            } else {
                string val = dfs(i, visited, cache);
                if (val == "IMPOSSIBLE") return val;
                sum += sign * stoi(val);
            }
        }

        cache[curr] = to_string(sum);
        return to_string(sum);
    }

    string cal(string target) {
        unordered_set<string> visited;
        unordered_map<string, string> cache;
        return dfs(target, visited, cache);
    }

    unordered_map<string, vector<string>> graph;
    vector<string> expressions;
};

void debug(unordered_map<string, vector<string>>& graph) {
    for (auto i : graph) {
        cout << "k: " << i.first;
        cout << "value: " << endl;
        for (auto j : i.second) {
            cout << j << " ";
        }
        cout << endl;
    }
}

void test(vector<string> expressions, string target) {
    ExpressionCalculator expCalculator = ExpressionCalculator(expressions);
    cout << expCalculator.cal(target) << endl;
}

int main() {
    test({ "T1 = 4", "T1 = 2 + T2" }, "T2"); // Impossible
    test({ "T1 = T2", "T2 = T1" }, "T2"); // Impossible
    test({ "T1 = 1", "T2 = T3", "T3 = T1" }, "T2"); // 1
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