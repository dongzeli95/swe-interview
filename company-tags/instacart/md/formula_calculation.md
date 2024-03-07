```cpp
// 第三轮 coding 公式计算
// 第一小问 input : ["T2", ["T1 = 1", "T2 = T3", "T3 = T1"]] output : T2值   公式都是左边一个变量， 右边是变量或者数值
// 第二小问 input : ["T2", ["T1 = 1", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3]]  output:T2值
// 公式左边为变量，右边为一个或多个变量 / 数值，包括加减操作
// 第三小问： 在第二小问基础上可能存在解不出的情况
// 这道题我是用topological sort的方法，但后来发现Top - down 递归就够了
// 然后发现所有的变量都会有一个相应的赋值
// 比如这种情况的Testcase就不存在["T2", ["T1=4", "T1 = 2 + T2"]]

#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

// Function to parse input and construct the graph
unordered_map<string, string> constructGraph(const vector<string>& formulas) {
    unordered_map<string, string> graph;
    for (const auto& formula : formulas) {
        size_t equalPos = formula.find('=');
        string left = formula.substr(0, equalPos - 1);
        string right = formula.substr(equalPos + 2);
        graph[left] = right;
    }
    return graph;
}

// DFS function to find the value of a variable
string dfs(const string& node, unordered_map<string, string>& graph, unordered_map<string, bool>& visited) {
    // Check if the node is a number
    if (isdigit(node[0])) return node;

    // Detect cycles
    if (visited[node]) throw runtime_error("Cycle detected");
    visited[node] = true;

    // DFS on the adjacent node
    return dfs(graph[node], graph, visited);
}

// Main function to find the value of a target variable
string solve(const string& target, const vector<string>& formulas) {
    auto graph = constructGraph(formulas);
    unordered_map<string, bool> visited;
    return dfs(target, graph, visited);
}

// Question part 2.
// Structure to represent an expression term
struct Term {
    string var; // Variable name or constant value
    char op;    // Operation: '+' or '-'
};

// Function to parse a formula and return the variable and its expression
pair<string, vector<Term>> parseFormula(const string& formula) {
    istringstream iss(formula);
    string variable, eq;
    vector<Term> expression;
    iss >> variable >> eq; // Read variable and equal sign

    // Read the expression
    string token;
    char op = '+';
    while (iss >> token) {
        if (token == "+") {
            op = '+';
        }
        else if (token == "-") {
            op = '-';
        }
        else {
            expression.push_back({ token, op });
        }
    }
    return { variable, expression };
}

vector<string> split(const string& str) {
    istringstream iss(str);
    vector<string> tokens;
    string token;
    while (iss >> token) {
        tokens.push_back(token);
    }
    return tokens;
}

// Function to construct the graph from the formulas
unordered_map<string, vector<string>> constructGraph2(const vector<string>& formulas) {
    unordered_map<string, vector<string>> graph;
    for (const auto& formula : formulas) {
        size_t equalPos = formula.find('=');
        string left = formula.substr(0, equalPos - 1);
        string right = formula.substr(equalPos + 2);
        graph[left] = split(right);
    }
    return graph;
}

// Function to evaluate expressions
int evaluate(const vector<string>& expr, unordered_map<string, vector<string>>& graph, unordered_map<string, bool>& visited, unordered_map<string, int>& computed);

// DFS function to find the value of a variable
int dfs2(const string& node, unordered_map<string, vector<string>>& graph, unordered_map<string, bool>& visited, unordered_map<string, int>& computed) {
    // Check if the node is a number
    if (isdigit(node[0]) || (node[0] == '-' && node.size() > 1)) {
        return stoi(node);
    }

    // Check for precomputed values
    if (computed.find(node) != computed.end()) {
        return computed[node];
    }

    // Check for cycles
    if (visited[node]) {
        throw runtime_error("Cycle detected in " + node);
    }
    visited[node] = true;

    // Evaluate the expression
    int value = evaluate(graph[node], graph, visited, computed);
    visited[node] = false;
    computed[node] = value;
    return value;
}

// DFS function to find the value of a variable
int evaluate(const vector<string>& expr, unordered_map<string, vector<string>>& graph, unordered_map<string, bool>& visited, unordered_map<string, int>& computed) {
    int result = 0;
    int sign = 1;

    for (const string& token : expr) {
        if (token == "+") {
            sign = 1;
        }
        else if (token == "-") {
            sign = -1;
        }
        else {
            result += sign * dfs2(token, graph, visited, computed);
        }
    }
    return result;
}

// Main function to find the value of a target variable
int solve2(const string& target, const vector<string>& formulas) {
    auto graph = constructGraph2(formulas);
    unordered_map<string, bool> visited;
    unordered_map<string, int> computed;
    return dfs2(target, graph, visited, computed);
}

int main() {
    // Example usage
    // vector<string> formulas = { "T1 = 1", "T2 = T3", "T3 = T1" };
    // string target = "T2";
    // try {
    //     cout << "Value of " << target << " is " << solve(target, formulas) << endl;
    // }
    // catch (const runtime_error& e) {
    //     cout << "Error: " << e.what() << endl;
    // }

    // Part2 Test
    // vector<string> formulas = { "T1 = 2", "T2 = 2 + T4", "T3 = T1 - 4", "T4 = T1 + T3" };
    // 比如这种情况的Testcase就不存在["T2", ["T1=4", "T1 = 2 + T2"]]
    vector<string> formulas = { "T1=4", "T1 = 2 + T2" };
    string target = "T2";
    try {
        cout << "Value of " << target << " is " << solve2(target, formulas) << endl;
    }
    catch (const runtime_error& e) {
        cout << "Error: " << e.what() << endl;
    }
    return 0;
}
```
