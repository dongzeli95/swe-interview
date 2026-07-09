// https://leetcode.com/problems/random-pick-with-weight/

/*
You are given a 0-indexed array of positive integers w where w[i] describes the weight of the ith index.
You need to implement the function pickIndex(), which randomly picks an index in the range [0, w.length - 1] (inclusive) and returns it. The probability of picking an index i is w[i] / sum(w).
For example, if w = [1, 3], the probability of picking index 0 is 1 / (1 + 3) = 0.25 (i.e., 25%), and the probability of picking index 1 is 3 / (1 + 3) = 0.75 (i.e., 75%).

Ex1:
Input
["Solution","pickIndex"]
[[[1]],[]]
Output
[null,0]

Explanation
Solution solution = new Solution([1]);
solution.pickIndex(); // return 0. The only option is to return 0 since there is only one element in w.

Ex2:
Input
["Solution","pickIndex","pickIndex","pickIndex","pickIndex","pickIndex"]
[[[1,3]],[],[],[],[],[]]
Output
[null,1,1,1,1,0]

Explanation
Solution solution = new Solution([1, 3]);
solution.pickIndex(); // return 1. It is returning the second element (index = 1) that has a probability of 3/4.
solution.pickIndex(); // return 1
solution.pickIndex(); // return 1
solution.pickIndex(); // return 1
solution.pickIndex(); // return 0. It is returning the first element (index = 0) that has a probability of 1/4.

Since this is a randomization problem, multiple answers are allowed.
All of the following outputs can be considered correct:
[null,1,1,1,1,0]
[null,1,1,1,1,1]
[null,1,1,1,0,0]
[null,1,1,1,0,1]
[null,1,0,1,0,0]
......
and so on.
*/

#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <numeric>

using namespace std;

class Solution {
public:
    Solution(vector<int>& w) {
        int prefixSum = 0;
        for (int weight : w) {
            prefixSum += weight;
            prefix_sum.push_back(prefixSum);
        }
        // total sum
        total_sum = prefix_sum.back();
    }
    
    // Time: O(logn), Space: O(n)
    int pickIndex() {
        // random number
        int random_num = rand() % total_sum;
        // binary search
        return upper_bound(prefix_sum.begin(), prefix_sum.end(), random_num) - prefix_sum.begin();
    }

private:
    vector<int> prefix_sum;
    int total_sum;
};

// Follow up 2: For each index we pick, we delete it from the array.
// Time: O(logn), Space: O(n)
// Segment Tree

class Solution2 {
public:
    Solution2(vector<int>& w) {
        this->arr = w;
        int n = w.size();
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

    void query(int node, int start, int end, int& val, int& res) {
        cout << "start: " << start << " end: " << end << " sum: " << segTree[node] << endl;
        // If out of boundary, return best index found so far.
        if (start > end || segTree[node] == 0) {
            return;
        }

        // If it's a leaf node, check if it's the best index found so far.
        if (start == end) {
            if (segTree[node] <= val && arr[start] != 0) {
                res = max(res, start);
            }
            return;
        }

        int mid = (start + end) / 2;
        if (arr[mid] != 0) {
            res = max(res, mid);
        }

        // If the left child has a sum less than or equal to val, 
        // then we might need to go to the right child.
        if (segTree[2 * node+1] >= val) {
            query(2 * node + 1, mid + 1, end, val, res);
        }
        // Else, continue searching in the left child.
        else {
            query(2 * node, start, mid, val, res);
        }
    }

    int pickIndex() {
        if (segTree[1] == 0) {
            return -1;
        }

        // random number
        int random_num = rand() % segTree[1];
        // query using segment tree.
        int idx = -1;
        query(1, 0, arr.size()-1, random_num, idx);
        // update segment tree along with original array.
        int delta = arr[idx];
        update(1, 0, arr.size()-1, idx, -delta);
        print();
        return idx;
    }

    void print() {
        cout << "segment tree" << endl;
        for (int i = 0; i < segTree.size(); ++i)
            cout << segTree[i] << " ";
        cout << endl;

        cout << "array " << endl;
        for (int i = 0; i < arr.size(); i++) {
            cout << arr[i] << " ";
        }
        cout << endl;
    }

    vector<int> segTree;
    vector<int> arr;
};

int main() {
    vector<int> w = {1, 3, 5, 7, 9, 11};
    // Solution solution(w);
    // cout << solution.pickIndex() << endl;
    // cout << solution.pickIndex() << endl;
    // cout << solution.pickIndex() << endl;
    // cout << solution.pickIndex() << endl;
    // cout << solution.pickIndex() << endl;
    // cout << solution.pickIndex() << endl;

    Solution2 segSolution(w);
    cout << segSolution.pickIndex() << endl;
    cout << segSolution.pickIndex() << endl;
    cout << segSolution.pickIndex() << endl;
    cout << segSolution.pickIndex() << endl;
    cout << segSolution.pickIndex() << endl;
    cout << segSolution.pickIndex() << endl;
    // cout << segSolution.pickIndex() << endl;
    return 0;
}