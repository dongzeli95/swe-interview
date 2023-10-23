/* 

给两个list, l1, l2。 
返回两个list，第一个list是l1里的有但l2里没有的元素，
第二个list是l2有但是l1没有的元素。（元素可以是数字，也可以是string）

For example:
l1 = [1,2,3,4,5]
l2 = [2,3,4,6,7]
return [1,5], [6,7]

Duplicates?

*/

#include <vector>
#include <unordered_set>
#include <cassert>
#include <iostream>

using namespace std;

// Time: O(m+n), Space: O(m+n)
vector<vector<int>> getNonOverlaps(vector<int>& l1, vector<int>& l2) {
    unordered_set<int> l1_set;
    unordered_set<int> overlap;

    int m = l1.size();
    for (int i = 0; i < m; i++) {
        l1_set.insert(l1[i]);
    }

    int n = l2.size();
    for (int i = 0; i < n; i++) {
        if (l1_set.count(l2[i])) {
            overlap.insert(l2[i]);
        }
    }

    vector<int> v1;
    vector<int> v2;
    for (int i = 0; i < m; i++) {
        if (!overlap.count(l1[i])) {
            v1.push_back(l1[i]);
        }
    }
    for (int i = 0; i < n; i++) {
        if (!overlap.count(l2[i])) {
            v2.push_back(l2[i]);
        }
    }

    return {v1, v2};
}

int main() {
    vector<int> l1 {1, 2, 3, 4, 5};
    vector<int> l2 {2, 3, 4, 6, 7};
    vector<vector<int>> res = getNonOverlaps(l1, l2);
    for (int i = 0; i < res[0].size(); i++) {
        cout << res[0][i] << " ";
    }
    cout << endl;

    for (int i = 0; i < res[1].size(); i++) {
        cout << res[1][i] << " ";
    }
    cout << endl;

    return 0;
}

