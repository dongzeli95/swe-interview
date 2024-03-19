```cpp
// https://leetcode.com/problems/maximum-profit-in-job-scheduling/description/

/*
We have n jobs, where every job is scheduled to be done from startTime[i] to endTime[i],
obtaining a profit of profit[i].

You're given the startTime, endTime and profit arrays, 
return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.

If you choose a job that ends at time X you will be able to start another job that starts at time X.

Ex1:
Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
Output: 120
Explanation: The subset chosen is the first and fourth job.
Time range [1-3]+[3-6] , we get profit of 120 = 50 + 70.

Ex2:
Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
Output: 150
Explanation: The subset chosen is the first, fourth and fifth job.
Profit obtained 150 = 20 + 70 + 60.

Ex3:
Input: startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
Output: 6
*/

#include <vector>
#include <map>

using namespace std;


// Intuition: we sort the job based on their end time.
// dp[i]: maximum profit ended at time i.
// dp[i] = max(dp[i], dp[start_time] + profit);
// We can use binary search to find the max profit that have idx <= start_time

// Time: O(nlogn), Space: O(n)
int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
    vector<vector<int>> jobs;
    map<int, int> dp{ {0, 0} };
    for (int i = 0; i < startTime.size(); ++i) {
        jobs.push_back({ endTime[i], startTime[i], profit[i] });
    }
    sort(jobs.begin(), jobs.end());
    for (auto& job : jobs) {
        int cur = prev(dp.upper_bound(job[1]))->second + job[2];
        if (cur > dp.rbegin()->second) dp[job[0]] = cur;
    }
    return dp.rbegin()->second;
}

// You're a dasher, and you want to try planning out your schedule. You can view a list of deliveries along with their associated start time, end time, and dollar amount for completing the order. Assuming dashers can only deliver one order at a time, determine the maximum amount of money you can make from the given deliveries.

// The inputs are as follows :

// int start_time : when you plan to start your schedule
// int end_time : when you plan to end your schedule
// int d_starts[n] : the start times of each delivery[i]
// int d_ends[n] : the end times of each delivery[i]
// int d_pays[n] : the pay for each delivery[i]
// The output should be an integer representing the maximum amount of money you can make by forming a schedule with the given deliveries.

// Constraints
// end_time >= start_time
// d_ends[i] >= d_starts[i]
// d_pays[i] > 0
// len(d_starts) == len(d_ends) == len(d_pays)

// Test 1

// start_time = 4
// end_time = 10
// d_starts = [2, 3, 5, 7]
// d_ends = [6, 5, 11, 10]
// d_pays = [5, 2, 4, 1]
// max_pay[5, (2 + 4), 4, -]

// Expected: 6```
