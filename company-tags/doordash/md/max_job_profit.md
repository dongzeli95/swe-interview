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
#include <iostream>
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

// Expected: 6


int maxDeliveryProfit(int start_time, int end_time, vector<int>& d_starts, vector<int>& d_ends, vector<int>& d_pays) {
    vector<vector<int>> deliveries;
    // End time, profit
    map<int, int> dp{ {0, 0} };

    // Filter deliveries based on the start and end times
    for (int i = 0; i < d_starts.size(); ++i) {
        if (d_starts[i] >= start_time && d_ends[i] <= end_time) {
            deliveries.push_back({ d_ends[i], d_starts[i], d_pays[i] });
        }
    }

    // Sort deliveries by end time
    sort(deliveries.begin(), deliveries.end());

    // Dynamic programming to calculate the maximum profit
    for (auto& delivery : deliveries) {
        int cur = prev(dp.upper_bound(delivery[1]))->second + delivery[2];
        if (cur > dp.rbegin()->second) dp[delivery[0]] = cur;
    }

    for (auto i: dp) {
        cout << "key: " << i.first << " second: " << i.second << endl;
    }

    return dp.rbegin()->second;
}

// FOLLOW UP 1: Get the jobs you selected

// In the DP array, instead of just storing max profit for a given index, also store which intervals led to that max profit.This will be either be[currInterval, nextAvailableInterval], or [nextImmediateInterval] --since these are the 2 choices we made in the DP solution.

// After you have finished with the DP, you end up with something like the following DP array :

//     0 : [20, [0, 3]] -- > index 0 has max profit of 20, and used profits from indices 0, 3 in to get there
//     1: ...
//     2 : ...
//     3 : [10, [4]] -- > index 3 has max profit of 10, and used interval 4 to get it
//     4: [10, [4]] -- > index 4 used itself to get max profit of 4
//     ...
//     You can follow through the indices and collect which values were used.If the current index is in the list of intervals used, add it to the solution.Continue checking for the remaining index in the list.

//     0: [0, 3] -- > add 0 to jobs since index == 0. go to index 3
//     3: [4] -- > 3 is missing from intervals, so don't add it. go to index 4
//     4: [4] -- > add 4 to jobs since index == 4. No other items used, so terminate

//     jobs = [0, 4]
//     This is O(n) operation.You can also do this during the DP itself rather than getting the selected jobs at the end

vector<int> maxDeliveryProfit2(int start_time, int end_time, vector<int>& d_starts, vector<int>& d_ends, vector<int>& d_pays) {
    vector<vector<int>> deliveries;
    // Map: End time -> (Max Profit, Previous End Time, List of Jobs)
    map<int, tuple<int, int, vector<int>>> dp{ {0, {0, -1, {}}} };

    for (int i = 0; i < d_starts.size(); ++i) {
        if (d_starts[i] >= start_time && d_ends[i] <= end_time) {
            deliveries.push_back({ d_ends[i], d_starts[i], d_pays[i], i });
        }
    }

    sort(deliveries.begin(), deliveries.end());

    for (auto& delivery : deliveries) {
        auto it = prev(dp.upper_bound(delivery[1]));
        int curProfit = get<0>(it->second) + delivery[2];
        vector<int> curJobs = get<2>(it->second);
        curJobs.push_back(delivery[3]); // Add current job index

        if (dp.find(delivery[0]) == dp.end() || curProfit > get<0>(dp[delivery[0]])) {
            dp[delivery[0]] = { curProfit, it->first, curJobs };
        }
    }

    // Trace back the selected jobs
    vector<int> selectedJobs;
    int lastEnd = dp.rbegin()->first;
    while (lastEnd != 0) {
        selectedJobs.push_back(get<2>(dp[lastEnd]).back());
        lastEnd = get<1>(dp[lastEnd]);
    }

    reverse(selectedJobs.begin(), selectedJobs.end());
    return selectedJobs;
}

// A follow up : multiple orders can now be allowed to be carried out at the same time, e.g.
// Add a variable max_allowed_parallel_runs.max_allowed_parallel_runs = 1 Then the result is still 6. If max_allowed_parallel_runs = 2, the result is 11.
int maxDeliveryProfit3(int start_time, int end_time, vector<int>& d_starts, vector<int>& d_ends, vector<int>& d_pays, int max_allowed_parallel_runs) {
    vector<vector<int>> deliveries;
    for (int i = 0; i < d_starts.size(); ++i) {
        if (d_starts[i] >= start_time && d_ends[i] <= end_time) {
            deliveries.push_back({ d_ends[i], d_starts[i], d_pays[i] });
        }
    }

    sort(deliveries.begin(), deliveries.end());

    int n = deliveries.size();
    vector<vector<int>> dp(n + 1, vector<int>(max_allowed_parallel_runs + 1, 0));

    for (int i = 0; i < n; ++i) {
        for (int k = 1; k <= max_allowed_parallel_runs; ++k) {
            // Continue without taking the current job
            dp[i][k] = max(dp[i][k], dp[i - 1 < 0 ? 0 : i - 1][k]);

            // Take the current job
            int nextIndex = upper_bound(d_starts.begin(), d_starts.end(), deliveries[i][0]) - d_starts.begin();
            dp[nextIndex][k - 1] = max(dp[nextIndex][k - 1], dp[i][k] + deliveries[i][2]);
        }
    }
    
    int max_profit = 0;
    for (int k = 0; k <= max_allowed_parallel_runs; ++k) {
        max_profit = max(max_profit, dp[n][k]);
    }

    return max_profit;
}

int main () {
    vector<int> d_starts {2, 3, 5, 7};
    vector<int> d_ends {6, 5, 11, 10};
    vector<int> d_pays {5, 2, 4, 1};
    // cout << maxDeliveryProfit(0, 10, d_starts, d_ends, d_pays) << endl;

    // vector<int> selectedJobs = maxDeliveryProfit2(4, 10, d_starts, d_ends, d_pays);
    // cout << "Selected Jobs: ";
    // for (int job : selectedJobs) {
    //     cout << job << " ";
    // }
    // cout << endl;

    int maxProfit = maxDeliveryProfit3(0, 10, d_starts, d_ends, d_pays, 1);
    cout << "Maximum Profit: " << maxProfit << endl;

    return 0;
}```
