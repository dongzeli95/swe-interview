```cpp
// https://leetcode.com/problems/total-cost-to-hire-k-workers

/*
You are given a 0-indexed integer array costs where costs[i] is the cost of hiring the ith worker.

You are also given two integers k and candidates. We want to hire exactly k workers according to the following rules:

You will run k sessions and hire exactly one worker in each session.
In each hiring session, choose the worker with the lowest cost from either the first candidates workers or the last candidates workers. Break the tie by the smallest index.
For example, if costs = [3,2,7,7,1,2] and candidates = 2, then in the first hiring session, we will choose the 4th worker because they have the lowest cost [3,2,7,7,1,2].
In the second hiring session, we will choose 1st worker because they have the same lowest cost as 4th worker but they have the smallest index [3,2,7,7,2]. 
Please note that the indexing may be changed in the process.
If there are fewer than candidates workers remaining, choose the worker with the lowest cost among them. Break the tie by the smallest index.
A worker can only be chosen once.
Return the total cost to hire exactly k workers.

Ex1:
Input: costs = [17,12,10,2,7,2,11,20,8], k = 3, candidates = 4
Output: 11
Explanation: We hire 3 workers in total. The total cost is initially 0.
- In the first hiring round we choose the worker from [17,12,10,2,7,2,11,20,8]. 
The lowest cost is 2, and we break the tie by the smallest index, which is 3. The total cost = 0 + 2 = 2.
- In the second hiring round we choose the worker from [17,12,10,7,2,11,20,8]. 
The lowest cost is 2 (index 4). The total cost = 2 + 2 = 4.
- In the third hiring round we choose the worker from [17,12,10,7,11,20,8]. 
The lowest cost is 7 (index 3). The total cost = 4 + 7 = 11. Notice that the worker with index 3 was common in the first and last four workers.
The total hiring cost is 11.

Ex2:
Input: costs = [1,2,4,1], k = 3, candidates = 3
Output: 4
Explanation: We hire 3 workers in total. The total cost is initially 0.
- In the first hiring round we choose the worker from [1,2,4,1]. 
The lowest cost is 1, and we break the tie by the smallest index, which is 0. The total cost = 0 + 1 = 1. Notice that workers with index 1 and 2 are common in the first and last 3 workers.
- In the second hiring round we choose the worker from [2,4,1]. 
The lowest cost is 1 (index 2). The total cost = 1 + 1 = 2.
- In the third hiring round there are less than three candidates. 
We choose the worker from the remaining workers [2,4]. The lowest cost is 2 (index 0). The total cost = 2 + 2 = 4.
The total hiring cost is 4.

*/

#include <vector>
#include <queue>
#include <cassert>
#include <iostream>

using namespace std;

// C is candidates size, K is the number of workers to hire
// Time complexity: O((C+K)*logC), Space complexity: O(C)
long long totalCost(vector<int>& costs, int k, int candidates) {
    if (costs.empty()) {
        return 0;
    }

    // custom comparator for min heap
    auto cmp = [&costs](int a, int b) {
        if (costs[a] == costs[b]) {
            return a > b;
        }
        return costs[a] > costs[b];
    };

    int n = costs.size();

    priority_queue<int, vector<int>, decltype(cmp)> pq(cmp);

    for (int i = 0; i < candidates; ++i) {
        pq.push(i);
    }

    // the boundary is important.
    // candidates size can be larger than n/2
    int boundary = max(n-candidates-1, candidates-1);
    for (int i = n-1; i > boundary; --i) {
        pq.push(i);
    }

    int l = candidates;
    int r = boundary;

    long long res = 0;
    for (int i = 0; i < k; i++) {
        int idx = pq.top();
        pq.pop();
        res += costs[idx];

        if (l > r) {
            continue;
        }
        if (idx < l) {
            pq.push(l);
            l++;
        } else if (idx > r) {
            pq.push(r);
            r--;
        }
    }

    return res;
}

int main() {
    vector<int> costs = {17,12,10,2,7,2,11,20,8};
    int k = 3;
    int candidates = 4;
    long long res = totalCost(costs, k, candidates);
    assert(res == 11);

    costs = {1,2,4,1};
    k = 3;
    candidates = 3;
    res = totalCost(costs, k, candidates);
    assert(res == 4);

    //[18,64,12,21,21,78,36,58,88,58,99,26,92,91,53,10,24,25,20,92,73,63,51,65,87,6,17,32,14,42,46,65,43,9,75]
    costs = {18,64,12,21,21,78,36,58,88,58,99,26,92,91,53,10,24,25,20,92,73,63,51,65,87,6,17,32,14,42,46,65,43,9,75};
    k = 13;
    candidates = 23;
    res = totalCost(costs, k, candidates);
    assert(res == 223);

    // [69,10,63,24,1,71,55,46,4,61,78,21,85,52,83,77,42,21,73,2,80,99,98,89,55,94,63,50,43,62,14]
    costs = {69,10,63,24,1,71,55,46,4,61,78,21,85,52,83,77,42,21,73,2,80,99,98,89,55,94,63,50,43,62,14};
    candidates = 31;
    k = 21;
    res = totalCost(costs, k, candidates);
    assert(res == 829);

    return 0;
}```
