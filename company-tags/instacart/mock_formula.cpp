// 第三轮 coding 公式计算
// 第一小问 input : ["T2", ["T1 = 1", "T2 = T3", "T3 = T1"]] output : T2值   公式都是左边一个变量， 右边是变量或者数值

#include <string>
#include <iostream>
#include <unordered_set>

using namespace std;

// Q1: Are there gonna be duplicate expressions for a given sign, T1 = 1, T1 = T2
// Q2: Do we need to deal with format issues like some expression might have spaces but some might not have spaces in-between?
// Q3: Are there going to be cycles with the given expressions?

class ExpressionCalculator {
public:
    ExpressionCalculator(vector<string>& expressions) {
        this->expressions = expressions;
        constructGraph();
    }

    void constructGraph() {
        for (int i = 0; i < expressions.size(); i++) {
            string exp = expressions[i];
            size_t equal_pos = exp.find('=');
            string left = exp.substr(0, equal_pos-1);
            string right = exp.substr(equal_pos+2);
            graph[left] = right;
        }
    }

    string dfs(string curr, unordered_set<string>& visited) {
        if (isdigit(graph[curr][0])) {
            return graph[curr];
        }

        if (visited.count(curr)) {
            return "IMPOSSIBLE";
        }

        visited.insert(curr);
        return dfs(graph[curr], visited);
    }

    string cal(string target) {
        unordered_set<string> visited;
        return dfs(target, visited);
    }

    unordered_map<string, string> graph;
    vector<string> expressions;
};

void debug(unordered_map<string, string>& graph) {
    for (auto i : graph) {
        cout << "k: " << i.first << " v: " << i.second << endl;
    }
}

int main() {
    vector<string> expressions {"T1 = T3", "T3 = 2", "T4 = T1"};
    ExpressionCalculator expCalculator = ExpressionCalculator(expressions);
    // debug(expCalculator.graph);

    string res = expCalculator.cal("T4");
    cout << res << endl;

    return 0;
}