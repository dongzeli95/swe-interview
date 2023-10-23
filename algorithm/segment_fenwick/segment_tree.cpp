// Segment tree implementation

#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

using namespace std;

class SegmentTree {
public:
    vector<int> arr;
    vector<int> segTree;

    SegmentTree(vector<int>& arr) {
        this->arr = arr;
        int n = arr.size();
        segTree.resize(4 * n);
        build(1, 0, n - 1);
    }

    void build(int node, int start, int end) {
        if (start == end) {
            segTree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;
        build(2 * node, start, mid);
        build(2 * node + 1, mid + 1, end);
        segTree[node] = segTree[2 * node] + segTree[2 * node + 1];
    }

    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            arr[idx] += val;
            segTree[node] += val;
            return;
        }

        int mid = (start + end) / 2;
        if (idx <= mid)
            update(2 * node, start, mid, idx, val);
        else
            update(2 * node + 1, mid + 1, end, idx, val);

        segTree[node] = segTree[2 * node] + segTree[2 * node + 1];
    }

    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l)
            return 0;
        if (l <= start && end <= r)
            return segTree[node];

        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r) + query(2 * node + 1, mid + 1, end, l, r);
    }

    void print() {
        for (int i = 0; i < segTree.size(); ++i)
            cout << segTree[i] << " ";
        cout << endl;
    }
};

int main() {
    vector<int> arr = { 1, 3, 5, 7, 9, 11 };
    SegmentTree st(arr);
    st.print();
    cout << "Initial sum of range (1, 3): " << st.query(1, 0, arr.size() - 1, 1, 3) << endl; // 3 + 5 + 7 = 15
    st.update(1, 0, arr.size() - 1, 1, 7);
    cout << "Updated sum of range (1, 3): " << st.query(1, 0, arr.size() - 1, 1, 3) << endl; // 22

    return 0;
}
