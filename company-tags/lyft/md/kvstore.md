```cpp

#include <string>
#include <unordered_map>
#include <iostream>
#include <sstream>

using namespace std;

// Class for Parsed operation from STDIN.
class Operation {
public:
  string op;
  string k;
  string version;

  Operation(string operation, string key) : k(key), op(operation), version("") {}
  Operation(string operation, string key, string ver) : k(key), op(operation), version(ver) {}
};

// Class for VersionedValue entity.
class Value {
public:
  int val;
  int version;

  Value(int v, int ver): val(v), version(ver) {}
};

// Class for Key Value Store.
class KVStore {
public:
    int put(string k, int v) {
        m[k] = v;
        
        // store in version map
        int ver = version++;
        if (!versioned_m.count(k)) {
            versioned_m[k] = {Value(v, ver)};
        } else {
            versioned_m[k].push_back(Value(v, ver));
        }

        // Print line to STDOUT for put().
        cout << PUT << "(#" << to_string(ver) << ") " << k << " = " << to_string(v) << endl;
        return ver;
    }

    // Get latest value for key k.
    // Return <NULL> if not found.
    string get(string k) {
        string res = "";
        if (!m.count(k)) {
            res = NULL_STR;
        } else {
            res = to_string(m[k]);
        }

        // Print line to STDOUT for get().
        cout << GET << " " << k << " = " << res << endl; 

        return res;
    }

    // Get versioned value for key k.
    // Return <NULL> if not found.
    string get(string k, int version) {
        string res = "";

        if (!versioned_m.count(k)) {
            res = NULL_STR;
        } else {
            int idx = search(versioned_m[k], version);
            if (idx == -1) {
                res = NULL_STR;
            } else {
                Value v = versioned_m[k][idx];
                res = to_string(v.val);
            }
        }

        // Print line to STDOUT for get() with version.
        cout << GET << " " << k << "(#" << to_string(version) << ") = " << res << endl;

        return res;
    }

    // Search value in the value list from versioned_m using binary search.
    // Input: value list, version number
    // Output: idx of the found value in the list.
    // Time complexity: O(logn) for n number of values in the list.
    int search(vector<Value> vals, int version) {
        int n = vals.size();
        int l = 0, r = n-1;

        int res = -1;
        while (l <= r) {
            int m = l + (r-l) / 2;
            if (vals[m].version == version) {
                return m;
            } else if (vals[m].version < version) {
                res = m;
                l = m+1;
            } else {
                r = m-1;
            }
        }

        return res;
    }

private:
    // Hash table keeping track of regular kv entries.
    unordered_map<string, int> m;
    // Hash table keeping track of versioned kv entries.
    unordered_map<string, vector<Value>> versioned_m;
    // Monotonically increasing version number.
    int version = 1;

    // Constants
    const string GET = "GET";
    const string PUT = "PUT";
    const string NULL_STR = "<NULL>";
};

vector<Operation> parseStdin() {
    string line = "";
    vector<Operation> res;

    while (getline(cin, line)) {
        string op = "";
        string k = "";
        string ver = "";
        istringstream iss(line);
        iss >> op >> k >> ver;

        // cout << "operator: " << op << " key: " << k << " v:" << ver << endl;

        Operation operation = Operation(op, k, ver);
        res.push_back(operation);
    }

    return res;
}

void execute(vector<Operation>& operations) {
    int n = operations.size();
    KVStore kv = KVStore();
    for (int i = 0; i < n; i++) {
        Operation operation = operations[i];
        string op = operation.op;
        string k = operation.k;
        string ver = operation.version;

        if (op == "PUT") {
            kv.put(k, stoi(ver));
        } else if (op == "GET") {
            // regular get
            if (ver.empty()) {
                kv.get(k);
            } else {
                kv.get(k, stoi(ver));
            }
        }
    }
}

void testOperations() {
    vector<Operation> ops;
    ops.push_back(Operation("PUT", "key1", "5"));
    ops.push_back(Operation("PUT", "key2", "6"));

    ops.push_back(Operation("GET", "key1", ""));
    ops.push_back(Operation("GET", "key1", "1"));

    execute(ops);
}

void testFinal() {
    KVStore kv = KVStore();
    // PUT key1 5
    kv.put("key1", 5);
    // PUT key2 6
    kv.put("key2", 6);
    //     GET key1
    kv.get("key1");
    //     GET key1 1
    kv.get("key1", 1);
    //     GET key2 2
    kv.get("key2", 2); // 6
    //     PUT key1 7
    kv.put("key1", 7);
    //     GET key1 1
    kv.get("key1", 1);
    //     GET key1 2
    kv.get("key1", 2);
    //     GET key1 3
    kv.get("key1", 3);
    //     GET key4
    kv.get("key4");
    //     GET key1 4
    kv.get("key1", 4);
    //     GET key2 1
    kv.get("key2", 1);
    return;
}

void testVersionedMap() {
    KVStore kv = KVStore();
    kv.put("key1", 5); // 1, 5
    kv.put("key2", 6); // 2, 6

    kv.get("key2", 2); // 6
    kv.get("key2", 1); // NULL
    return;
}

void testMap() {
    KVStore kv = KVStore();
    kv.put("key1", 5);
    cout << kv.get("key1") << endl; // 5
    cout << kv.get("key2") << endl; // NULL

    kv.put("key1", 7);
    cout << kv.get("key1") << endl; // 7
    return;
}

// key2: 6 version: 2
void testParseAndExecute() {
    vector<Operation> operations = parseStdin();
    execute(operations);
}

int main() {
    // testVersionedMap();
    // testMap();

    // testFinal();
    // testOperations();

    testParseAndExecute();
    return 0;
}```
