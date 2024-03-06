#include <string>
#include <chrono>
#include <iostream>

using namespace std;

class Value {
public: 
  string val;
  int time;

  Value(string v, int t): val(v), time(t) {}
};

// KV Store with timestamp
class KVStore {
public:
    unordered_map<string, string> m;
    unordered_map<string, vector<Value>> timed_m;

    int counter = 0;

    string get(string k) {
        if (!m.count(k)) {
            throw runtime_error("Key doesn't exist");
        }

        return m[k];
    }

    void set(string k, string v) {
        m[k] = v;

        // set k, v in timed_m
        int t = getTime();
        Value value = Value(v, t);
        if (!timed_m.count(k)) {
            timed_m[k] = {value};
        } else {
            timed_m[k].push_back(value);
        }
    }

    string get(string k, int time) {
        if (!timed_m.count(k)) {
            throw runtime_error("Key doesn't exist");
        }

        vector<Value> valList = timed_m[k];
        int idx = search(valList, time);
        if (idx == -1) {
            throw runtime_error("Couldn't find key in time");
        }

        return valList[idx].val;
    }

    void debug(vector<Value>& valList) {
        for (int i = 0; i < valList.size(); i++) {
            cout << valList[i].val << " ";
        }
        cout << endl;
    }

    int search(vector<Value>& valList, int time) {
        int n = valList.size();
        int l = 0, r = n-1;

        int res = -1;
        while (l <= r) {
            int m = l + (r-l) / 2;
            if (valList[m].time == time) {
                return m;
            } else if (valList[m].time < time) {
                res = m;
                l = m+1;
            } else {
                r = m-1;
            }
        }

        return res;
    }

    int getTime() {
        //   const auto now = std::chrono::system_clock::now();
        //   const std::time_t t_c = std::chrono::system_clock::to_time_t(now);
        return counter++;
    }
};

int main() {
    KVStore kvStore;
    kvStore.set("k1", "v1"); // 0
    kvStore.set("k2", "v2"); // 1
    kvStore.set("k1", "v3"); // 2

    cout << kvStore.get("k1") << endl; //v3
    cout << kvStore.get("k1", 1) << endl; // v1

    kvStore.getTime(); // 3
    kvStore.getTime(); // 4
    kvStore.set("k1", "v4"); // 5
    cout << kvStore.get("k1") << endl; //v4
    cout << kvStore.get("k1", 0) << endl; //v1
    cout << kvStore.get("k1", 1) << endl; //v1
    cout << kvStore.get("k1", 2) << endl; //v3
    cout << kvStore.get("k1", 3) << endl; //v3
    cout << kvStore.get("k1", 4) << endl; //v3
    cout << kvStore.get("k1", 5) << endl; //v4
    cout << kvStore.get("k1", 6) << endl; //v4

    // {"k1": [(v1, 0), (v3, 2)]}
    return 0;
}