// C++ mirror of task_dependency.py — same algorithms, structured the same way,
// so you can diff them mentally to learn Python idioms coming from C++.
//
// Python  ↔  C++ cheat sheet used below (with `using namespace std;` in effect):
//   list[T]                         vector<T>
//   dict[K, V]                      unordered_map<K, V>
//   set[T]                          unordered_set<T>
//   deque[T]  (used as FIFO)        queue<T>            // plain FIFO — one end only
//   defaultdict(list)               unordered_map<K, vector<V>>
//                                     (operator[] auto-inserts a default-constructed value,
//                                      same as defaultdict semantics)
//   @dataclass                      plain struct with public fields
//   x in s                          s.count(x)                    (or s.contains(x) in C++20)
//   for x in xs                     for (const T& x : xs)
//   for k, v in d.items()           iterate as pair<const K, V>; use .first / .second
//   raise KeyError("...")           throw runtime_error("...")
//   [n for n in xs if pred(n)]      range loop + push_back
//   set(xs)                         unordered_set<T>(xs.begin(), xs.end())
//   queue.append(x)                 q.push(x)
//   queue.popleft()                 t = q.front(); q.pop();       // two steps, pop() returns void
//
// Note: this file uses fully explicit types (no `auto`) to keep the C++↔Python
// mapping as legible as possible. In real C++ you'd lean on `auto` and structured
// bindings for the same loops.
//
// Complexity is identical to the Python version:
//   dependencies_of_targets_brute: O(k*(V+E)) reachability + O(V+E) topo
//   dependencies_of_targets:       O(V+E) total
//   ancestors_of_target:           O(V+E)

#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;

struct Task {
    string id;
    vector<string> dependencies;
};


// ---------- Q1 (brute force): per-target reachability + topo sort ----------

vector<string> dependencies_of_targets_brute(
    const vector<Task>& all_tasks,
    const vector<string>& targets
) {
    // by_id: dict[str, Task*] — pointer avoids copying the Task; the vector owns storage.
    unordered_map<string, const Task*> by_id;
    for (const Task& t : all_tasks) by_id[t.id] = &t;

    unordered_set<string> target_set(targets.begin(), targets.end());
    for (const string& tgt : targets) {
        if (by_id.find(tgt) == by_id.end()) {
            throw runtime_error("target not found in all_tasks: " + tgt);
        }
    }

    // Pass 1: one BFS *per target*, fresh visited set each time, then union.
    // Wasteful when targets share deps — same subgraph gets walked more than once.
    unordered_set<string> reachable;
    for (const string& tgt : targets) {
        unordered_set<string> per_target_seen;
        queue<string> q;
        for (const string& dep : by_id[tgt]->dependencies) {
            if (!per_target_seen.count(dep)) {
                per_target_seen.insert(dep);
                q.push(dep);
            }
        }
        while (!q.empty()) {
            string node = q.front();
            q.pop();
            for (const string& dep : by_id[node]->dependencies) {
                if (!per_target_seen.count(dep)) {
                    per_target_seen.insert(dep);
                    q.push(dep);
                }
            }
        }
        for (const string& n : per_target_seen) reachable.insert(n);
    }

    // Pass 2: Kahn's topo sort restricted to `reachable`.
    unordered_map<string, vector<string>> reverse_adj;
    unordered_map<string, int> in_degree;
    for (const string& node : reachable) in_degree[node] = 0;
    for (const string& node : reachable) {
        for (const string& dep : by_id[node]->dependencies) {
            if (reachable.count(dep)) {
                reverse_adj[dep].push_back(node);
                in_degree[node] += 1;
            }
        }
    }

    queue<string> q;
    for (const pair<const string, int>& entry : in_degree) {
        if (entry.second == 0) q.push(entry.first);
    }
    vector<string> order;
    while (!q.empty()) {
        string node = q.front();
        q.pop();
        order.push_back(node);
        for (const string& dependent : reverse_adj[node]) {
            if (--in_degree[dependent] == 0) q.push(dependent);
        }
    }

    if (order.size() != reachable.size()) {
        throw runtime_error("cycle detected in dependency graph");
    }

    vector<string> result;
    for (const string& n : order) {
        if (!target_set.count(n)) result.push_back(n);
    }
    return result;
}


// ---------- Q1 (optimized): multi-source BFS with shared visited set ----------

vector<string> dependencies_of_targets(
    const vector<Task>& all_tasks,
    const vector<string>& targets
) {
    unordered_map<string, const Task*> by_id;
    for (const Task& t : all_tasks) by_id[t.id] = &t;

    unordered_set<string> target_set(targets.begin(), targets.end());
    for (const string& tgt : targets) {
        if (by_id.find(tgt) == by_id.end()) {
            throw runtime_error("target not found in all_tasks: " + tgt);
        }
    }

    // Pass 1: multi-source BFS. `reachable` is shared across all targets, so
    // each node is enqueued at most once regardless of how many targets reach it.
    unordered_set<string> reachable;
    queue<string> q;
    for (const string& tgt : targets) {
        for (const string& dep : by_id[tgt]->dependencies) {
            if (!reachable.count(dep)) {
                reachable.insert(dep);
                q.push(dep);
            }
        }
    }
    while (!q.empty()) {
        string node = q.front();
        q.pop();
        for (const string& dep : by_id[node]->dependencies) {
            if (!reachable.count(dep)) {
                reachable.insert(dep);
                q.push(dep);
            }
        }
    }

    // Pass 2: Kahn's topo sort restricted to `reachable`. Identical to brute version.
    unordered_map<string, vector<string>> reverse_adj;
    unordered_map<string, int> in_degree;
    for (const string& node : reachable) in_degree[node] = 0;
    for (const string& node : reachable) {
        for (const string& dep : by_id[node]->dependencies) {
            if (reachable.count(dep)) {
                reverse_adj[dep].push_back(node);
                in_degree[node] += 1;
            }
        }
    }

    queue<string> topo_q;
    for (const pair<const string, int>& entry : in_degree) {
        if (entry.second == 0) topo_q.push(entry.first);
    }
    vector<string> order;
    while (!topo_q.empty()) {
        string node = topo_q.front();
        topo_q.pop();
        order.push_back(node);
        for (const string& dependent : reverse_adj[node]) {
            if (--in_degree[dependent] == 0) topo_q.push(dependent);
        }
    }

    if (order.size() != reachable.size()) {
        throw runtime_error("cycle detected in dependency graph");
    }

    vector<string> result;
    for (const string& n : order) {
        if (!target_set.count(n)) result.push_back(n);
    }
    return result;
}


// ---------- Q2: transitive ancestors of a single target ----------

vector<string> ancestors_of_target(
    const vector<Task>& all_tasks,
    const string& target
) {
    unordered_map<string, const Task*> by_id;
    for (const Task& t : all_tasks) by_id[t.id] = &t;
    if (by_id.find(target) == by_id.end()) {
        throw runtime_error("target not found in all_tasks: " + target);
    }

    // Build reverse adjacency: dep → list of things that depend on it.
    unordered_map<string, vector<string>> reverse_adj;
    for (const Task& task : all_tasks) {
        for (const string& dep : task.dependencies) {
            reverse_adj[dep].push_back(task.id);
        }
    }

    vector<string> ancestors;
    unordered_set<string> seen = {target};
    queue<string> q;
    q.push(target);
    while (!q.empty()) {
        string node = q.front();
        q.pop();
        for (const string& parent : reverse_adj[node]) {
            if (!seen.count(parent)) {
                seen.insert(parent);
                ancestors.push_back(parent);
                q.push(parent);
            }
        }
    }
    return ancestors;
}


// ---------- demo ----------

static void print_vec(const string& label, const vector<string>& v) {
    cout << label << ": [";
    for (size_t i = 0; i < v.size(); ++i) {
        cout << "'" << v[i] << "'";
        if (i + 1 < v.size()) cout << ", ";
    }
    cout << "]\n";
}

int main() {
    //
    //   A ──┐
    //   B ──┤─→ D ─→ F
    //   C ──┘       ↑
    //          E ───┘
    //
    vector<Task> tasks = {
        {"A", {}},
        {"B", {}},
        {"C", {}},
        {"D", {"A", "B", "C"}},
        {"E", {}},
        {"F", {"D", "E"}},
    };

    print_vec("Q1 brute  deps of [F]   ", dependencies_of_targets_brute(tasks, {"F"}));
    print_vec("Q1 opt    deps of [F]   ", dependencies_of_targets(tasks, {"F"}));
    print_vec("Q1 brute  deps of [D,E] ", dependencies_of_targets_brute(tasks, {"D", "E"}));
    print_vec("Q1 opt    deps of [D,E] ", dependencies_of_targets(tasks, {"D", "E"}));
    print_vec("Q1 brute  deps of [F,D] ", dependencies_of_targets_brute(tasks, {"F", "D"}));
    print_vec("Q1 opt    deps of [F,D] ", dependencies_of_targets(tasks, {"F", "D"}));
    print_vec("Q2  ancestors of A      ", ancestors_of_target(tasks, "A"));
    print_vec("Q2  ancestors of E      ", ancestors_of_target(tasks, "E"));
    print_vec("Q2  ancestors of F      ", ancestors_of_target(tasks, "F"));

    return 0;
}
