# Python ↔ C++ Reference (via task_dependency.{py,cpp})

Companion doc for `task_dependency.py` and `task_dependency.cpp`. Same algorithm,
two languages. Read one, glance here, know the other.

Organized bottom-up: types → declarations → loops → containers → error handling
→ then a side-by-side walk of specific chunks from the file.

---

## 1. Type mapping (the base layer)

| Concept | Python | C++ (`using namespace std;`) |
|---|---|---|
| String | `str` | `string` |
| Dynamic array | `list[T]` | `vector<T>` |
| Hash map | `dict[K, V]` | `unordered_map<K, V>` |
| Tree map | `dict` (ordered by insertion) | `map<K, V>` (ordered by key) |
| Hash set | `set[T]` | `unordered_set<T>` |
| FIFO queue | `collections.deque` | `queue<T>` |
| Stack | `list` (`append`/`pop`) | `stack<T>` or `vector<T>` |
| Priority queue | `heapq` (functions on a list) | `priority_queue<T>` (max-heap default) |
| Fixed-size record | `@dataclass` / `NamedTuple` | `struct` |
| Auto-inserting map | `defaultdict(list)` | `unordered_map<K, vector<V>>` (via `operator[]`) |
| Counter | `collections.Counter` | `unordered_map<K, int>` (manual `++`) |

**Gotcha:** Python's default `dict` and `set` are hash-based (`unordered_*` in C++).
For ordered iteration by key, use `std::map` / `std::set` in C++.

---

## 2. Declarations and initialization

```python
# Python
by_id: dict[str, Task] = {t.id: t for t in all_tasks}
target_set: set[str] = set(targets)
reachable: set[str] = set()
queue: deque[str] = deque()
```

```cpp
// C++
unordered_map<string, const Task*> by_id;
for (const Task& t : all_tasks) by_id[t.id] = &t;

unordered_set<string> target_set(targets.begin(), targets.end());
unordered_set<string> reachable;
queue<string> q;
```

**Notes:**
- Python variable annotations (`: dict[str, Task]`) are *hints*, not enforced. C++ types are real.
- Python dict-comprehension `{k: v for x in xs}` has no direct C++ equivalent — you write a range-for loop.
- Python's `set(iterable)` maps to the C++ range constructor `unordered_set<T>(begin, end)`.
- In C++ we store `const Task*` (pointer) instead of `Task` (copy). Python doesn't have this dilemma — everything is a reference under the hood.

---

## 3. Loop syntax

### Basic iteration
```python
for x in xs:
    ...
```
```cpp
for (const T& x : xs) { ... }
```

### With index
```python
for i, x in enumerate(xs):
    ...
```
```cpp
for (size_t i = 0; i < xs.size(); ++i) {
    const T& x = xs[i];
    ...
}
```

### Two containers zipped
```python
for a, b in zip(xs, ys):
    ...
```
```cpp
for (size_t i = 0; i < xs.size(); ++i) {
    const T& a = xs[i];
    const U& b = ys[i];
    ...
}
```

### Map iteration (key + value)
```python
for k, v in d.items():
    ...
```
```cpp
// with auto (idiomatic):
for (const auto& [k, v] : d) { ... }
// without auto (explicit):
for (const pair<const K, V>& entry : d) {
    const K& k = entry.first;
    const V& v = entry.second;
    ...
}
```

**Gotcha:** `pair<const K, V>` — the key is `const` because map keys are immutable
once inserted. Writing `pair<K, V>` compiles but *copies* each entry.

---

## 4. Membership, get-or-default, remove

| Op | Python | C++ |
|---|---|---|
| `x in s` | `x in s` | `s.count(x)` or `s.contains(x)` (C++20) |
| `x not in s` | `x not in s` | `!s.count(x)` |
| `d[k]` (KeyError if missing) | `d[k]` | `d.at(k)` (throws `out_of_range`) |
| `d[k]` (auto-insert default) | `defaultdict[k]` | `d[k]` (yes — `operator[]` on maps auto-inserts) |
| `d.get(k, default)` | `d.get(k, default)` | `d.count(k) ? d[k] : default` (no built-in) |
| `s.add(x)` | `s.add(x)` | `s.insert(x)` |
| `s.remove(x)` | `s.remove(x)` | `s.erase(x)` |

**Gotcha in C++:** `map[k]` on a `const map` is a compile error, and on a non-const
map with a missing `k`, it silently *creates* a default entry. Use `.at(k)` when you
want the "throw if missing" behavior of Python's `d[k]`.

---

## 5. Queue / stack ops (the BFS/DFS bread-and-butter)

```python
# Python deque as BFS queue
q = deque()
q.append(x)          # enqueue
node = q.popleft()   # dequeue (returns value)

# Python list as DFS stack
s = []
s.append(x)
node = s.pop()       # returns value
```

```cpp
// C++ queue<T> for BFS
queue<string> q;
q.push(x);              // enqueue
string node = q.front(); // peek — pop() returns void
q.pop();                // discard front

// C++ stack<T> for DFS
stack<string> s;
s.push(x);
string node = s.top();  // peek — pop() returns void
s.pop();

// Or use vector<T> as an ad-hoc stack (very common):
vector<string> s;
s.push_back(x);
string node = s.back();
s.pop_back();
```

**Gotcha:** In C++, `pop()` never returns the value. Always two lines: read
front/top, then pop. Python's `popleft()` and `pop()` return the value.

---

## 6. List comprehensions → range loops

```python
# Python
result = [n for n in order if n not in target_set]
```

```cpp
// C++ — no equivalent, just a loop:
vector<string> result;
for (const string& n : order) {
    if (!target_set.count(n)) result.push_back(n);
}
```

This is the single biggest ergonomic gap. In an interview, using comprehensions
in Python is worth 3–5 lines of C++ per filter/transform, and it reads better.

---

## 7. Error handling

```python
raise KeyError(f"target {tgt!r} not found in all_tasks")

try:
    ...
except KeyError as e:
    ...
```

```cpp
throw runtime_error("target not found in all_tasks: " + tgt);

try {
    ...
} catch (const runtime_error& e) {
    ...
}
```

**Gotcha:** Python has typed exceptions with a specific hierarchy. C++ exceptions
are just types you inherit from `std::exception`. In interview code, one-off
`runtime_error` for anything unexpected is fine.

---

## 8. Side-by-side: pass 1 of the optimized Q1

This is the core of the algorithm — multi-source BFS building the reachable set.

**Python (`task_dependency.py:105–116`):**
```python
reachable: set[str] = set()
queue: deque[str] = deque()
for tgt in targets:
    for dep in by_id[tgt].dependencies:
        if dep not in reachable:
            reachable.add(dep)
            queue.append(dep)
while queue:
    node = queue.popleft()
    for dep in by_id[node].dependencies:
        if dep not in reachable:
            reachable.add(dep)
            queue.append(dep)
```

**C++ (`task_dependency.cpp` pass 1 of `dependencies_of_targets`):**
```cpp
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
```

**Line-by-line diff:**

| Python | C++ | Note |
|---|---|---|
| `set()` | `unordered_set<string>` (default ctor) | Hash set |
| `deque()` | `queue<string>` (default ctor) | Plain FIFO |
| `for tgt in targets:` | `for (const string& tgt : targets)` | Range-for |
| `by_id[tgt].dependencies` | `by_id[tgt]->dependencies` | `->` because pointer |
| `dep not in reachable` | `!reachable.count(dep)` | Python is briefer |
| `reachable.add(dep)` | `reachable.insert(dep)` | Method name diff |
| `queue.append(dep)` | `q.push(dep)` | Method name diff |
| `while queue:` | `while (!q.empty())` | Python: empty containers are falsy |
| `queue.popleft()` | `string node = q.front(); q.pop();` | Two-step in C++ |

---

## 9. Side-by-side: pass 2 (Kahn's topo sort)

**Python (`task_dependency.py:119–132`):**
```python
reverse_adj: dict[str, list[str]] = defaultdict(list)
in_degree: dict[str, int] = {node: 0 for node in reachable}
for node in reachable:
    for dep in by_id[node].dependencies:
        if dep in reachable:
            reverse_adj[dep].append(node)
            in_degree[node] += 1

queue = deque(n for n, d in in_degree.items() if d == 0)
order: list[str] = []
while queue:
    node = queue.popleft()
    order.append(node)
    for dependent in reverse_adj[node]:
        in_degree[dependent] -= 1
        if in_degree[dependent] == 0:
            queue.append(dependent)
```

**C++ (`task_dependency.cpp` pass 2 of `dependencies_of_targets`):**
```cpp
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
```

**Interesting bits:**

| Python | C++ | Note |
|---|---|---|
| `defaultdict(list)` | `unordered_map<string, vector<string>>` | C++ `operator[]` auto-inserts default-constructed `vector` |
| `{node: 0 for node in reachable}` | separate loop `for ... in_degree[node] = 0;` | No dict comprehension in C++ |
| `deque(n for n, d in items if d == 0)` | separate loop + `push` | No generator + range constructor for `queue` |
| `n for n, d in ...` | `for (const pair<const string, int>& entry : ...)` | Structured binding needs `auto` |
| `in_degree[dep] -= 1; if ... == 0` | `if (--in_degree[dep] == 0)` | C++ pre-decrement expression is cheeky but common |

---

## 10. Python idioms to actively use in interviews

These aren't in the C++ file because C++ doesn't have equivalents (or they're
ugly). Learn these — they're what makes Python interview code short:

```python
# 1. List/set/dict comprehensions
squares = [x*x for x in nums]
even_squares = [x*x for x in nums if x % 2 == 0]
lookup = {v: k for k, v in d.items()}
seen = {x for x in xs}

# 2. Tuple unpacking (multiple returns, swaps, enumerate/zip)
a, b = 1, 2
a, b = b, a               # swap without temp
first, *rest = [1, 2, 3]  # rest = [2, 3]

# 3. Chained comparisons
if 0 <= i < len(arr):
    ...

# 4. any() / all() / sum() with generators
if any(x < 0 for x in xs): ...
total = sum(x*2 for x in xs)

# 5. sorted / sort with key=
sorted(words, key=len)
sorted(pairs, key=lambda p: (p[1], -p[0]))  # sort by 2nd asc, 1st desc

# 6. enumerate / zip
for i, x in enumerate(xs): ...
for a, b in zip(xs, ys): ...

# 7. Slicing (no equivalent in C++)
arr[::-1]     # reverse
arr[i:j]      # subarray (view-like)
arr[::2]      # every other element

# 8. collections shortcuts
from collections import defaultdict, Counter, deque
counts = Counter("hello")   # {'h':1,'e':1,'l':2,'o':1}
adj = defaultdict(list)     # adj[k].append(x) works without init

# 9. String tricks
",".join(strs)              # C++: manual loop with separator
s.split()                   # split on whitespace
s.startswith("foo")
"".join(reversed(s))

# 10. heapq for priority queue (min-heap by default)
import heapq
heap = []
heapq.heappush(heap, 3)
smallest = heapq.heappop(heap)
```

---

## 11. Suggested workflow to internalize

1. Open both files side-by-side in your IDE.
2. Pick one function (`ancestors_of_target` is the smallest — start there).
3. Cover the Python; try to translate the C++ back to Python from memory.
4. Uncover, diff. Note what surprised you.
5. Move to `dependencies_of_targets` (harder — two passes).
6. When you can do both without peeking, move to the "idioms to use" section
   above and drill 2–3 problems using them (Course Schedule, Clone Graph,
   Word Ladder — all graph problems that reuse the same patterns).

---

## 12. Interview-day cheat: what to remember under pressure

If your brain freezes and you need to code fast, these are the muscle-memory
substitutions from C++:

- `vector<X> v` → `v = []`
- `unordered_map<K,V> m` → `m = {}`
- `unordered_set<K> s` → `s = set()`
- `queue<X> q; q.push(x); q.pop()` → `q = deque(); q.append(x); q.popleft()`
- `stack<X> s; s.push(x); s.pop()` → `s = []; s.append(x); s.pop()`
- Adjacency list `unordered_map<K, vector<V>>` → `adj = defaultdict(list)`
- BFS visited set → same `visited = set()`, `visited.add(x)`, `x in visited`
- Loop range `for (int i = 0; i < n; ++i)` → `for i in range(n):`
- Loop with index `for (size_t i = 0; i < v.size(); ++i)` → `for i, x in enumerate(v):`
