```cpp
// https://leetcode.com/problems/most-profit-assigning-work/description/

/*

You have n jobs and m workers. 
You are given three arrays: difficulty, profit, and worker where:

difficulty[i] and profit[i] are the difficulty and the profit of the ith job, and
worker[j] is the ability of jth worker (i.e., the jth worker can only complete a job with difficulty at most worker[j]).
Every worker can be assigned at most one job, but one job can be completed multiple times.

For example, if three workers attempt the same job that pays $1, then the total profit will be $3. If a worker cannot complete any job, their profit is $0.
Return the maximum profit we can achieve after assigning the workers to the jobs.

Ex1:
Input: difficulty = [2,4,6,8,10], profit = [10,20,30,40,50], worker = [4,5,6,7]
Output: 100
Explanation: Workers are assigned jobs of difficulty [4,4,6,6] and they get a profit of [20,20,30,30] separately.

Ex2:
Input: difficulty = [85,47,57], profit = [24,66,99], worker = [40,25,25]
Output: 0

*/

// Intuition: We need to find max profit job for each worker under their capability.
// We are going to keep track a max profit job under cap i for worker i.
// later worker can keep using the max profit job if there are no job with more profit for more capabilities.

#include <vector>

using namespace std;

// Time: O(nlogn + qlogq), n is number of jobs and q is number of workers.
// Space: O(n) number of jobs.

// Two pointer, greedy.
int maxProfitAssignment(vector<int>& difficulty, vector<int>& profit, vector<int>& worker) {
    vector<pair<int, int>> jobs;
    int N = profit.size(), res = 0, i = 0, best = 0;
    for (int j = 0; j < N; ++j)
        jobs.push_back(make_pair(difficulty[j], profit[j]));
    sort(jobs.begin(), jobs.end());
    sort(worker.begin(), worker.end());
    for (int& ability : worker) {
        while (i < N && ability >= jobs[i].first)
            best = max(jobs[i++].second, best);
        res += best;
    }
    return res;
}```
