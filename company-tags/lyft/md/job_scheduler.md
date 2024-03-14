```cpp
// 上机，Job Scheduler。每一行输入是这样：
// J1：Job号；
// 0023， 24小时制的开始时间 00：23；
// 45：Job需要45分钟。
// 输出Job和对应的Machine No.（！！并且，如果同时有多个machine 空闲，要用编号小的那个！！）
// input
// J1 0023 45
// J2 0025 10
// J3 0100 60

// output
// J1 M1
// J2 M2
// J3 M1

// Qs:
// 1. Any duplicate jobs from input?
// 2. If the previous job end 
// Do we have cases for overnight jobs? where it starts with 23:20 for example and last 50 minutes.
// it's hard to justify the end time with other jobs to figure out which one finished first?

#include <vector>
#include <queue>
#include <string>
#include <iostream>
#include <sstream>

using namespace std;

// Convert to number of minutes since midnight?
int parseTime(const string& timeStr) {
    int hour = stoi(timeStr.substr(0, 2));
    int minute = stoi(timeStr.substr(2, 2));
    return hour * 60 + minute;
}

class Machine {
public:
    Machine(int i) {
        idx = i;
        endTime = 0;
    };

    int idx;
    int endTime;

    string getName() {
        return "M" + to_string(this->idx);
    }

    void debug() {
        cout << getName() << " endTime: " << endTime << endl;
    }
};

class Job {
public:
    Job(string id, string startTime, string duration) {
        jobId = id;
        start = parseTime(startTime);
        end = start + stoi(duration);
    }

    string jobId;
    int start;
    int end;
};

// Intuition, we loop through each job,
// for each job we find if there are any idle machine that can handle it, initially we only have one machine.
// 
// Whenever there is no idle machine, we check if ocupied machine has finished?

// N be the number of machines.
// M be the number of jobs.
// Sorting jobs takes O(M*LogM)
// Popping and pushing into PQ each cost O(logN) with for loop over jobs: O(M*LogN)

// Time: O(mlogm + mlogn), Space: O(n + logn for sort in c++)
unordered_map<string, string> jobScheduler(vector<Job>& jobs) {
    if (jobs.empty()) {
        return {};
    }

    sort(jobs.begin(), jobs.end(), [](const Job& j1, Job& j2) {
        return j1.start < j2.start;
    });

    auto occupiedMachineCmp = [](Machine a, Machine b) {
        if (a.endTime == b.endTime) {
            return a.idx > b.idx;
        }

        return a.endTime > b.endTime;
    };

    auto idleMachineCmp = [](Machine a, Machine b) {
        return a.idx > b.idx;
    };

    priority_queue<Machine, vector<Machine>, decltype(occupiedMachineCmp)> occupiedMachinePQ(occupiedMachineCmp);
    priority_queue<Machine, vector<Machine>, decltype(idleMachineCmp)> idleMachinePQ(idleMachineCmp);

    // The first idle machine.
    Machine m1 = Machine(1);
    idleMachinePQ.push(m1);

    int n = jobs.size();
    int counter = 2; // new machine will start with number 2.
    unordered_map<string, string> assignments;
    for (int i = 0; i < n; i++) {
        string jobId = jobs[i].jobId;
        int jobStartTime = jobs[i].start;
        int jobEndTime = jobs[i].end;

        // if (!occupiedMachinePQ.empty()) {
        //     Machine m = occupiedMachinePQ.top();
        //     m.debug();
        // }
        // cout << "curr job start time: " << jobStartTime << endl;

        // Move machine from occupied machine to idle machine if previous job already ended.
        while (!occupiedMachinePQ.empty() && occupiedMachinePQ.top().endTime <= jobStartTime) {
            Machine curr = occupiedMachinePQ.top();
            occupiedMachinePQ.pop();
            idleMachinePQ.push(curr);
        }

        // If we have idle machine, use it.
        if (idleMachinePQ.size() > 0) {
            Machine curr = idleMachinePQ.top();
            idleMachinePQ.pop();
            curr.endTime = jobEndTime;
            occupiedMachinePQ.push(curr);
            assignments[jobId] = curr.getName();
        } else {
            Machine newMachine = Machine(counter++);
            newMachine.endTime = jobEndTime;
            occupiedMachinePQ.push(newMachine);
            assignments[jobId] = newMachine.getName();
        }
    }

    return assignments;
}

vector<Job> parseStdin() {
    vector<Job> res;

    string line;
    while (getline(cin, line)) {
        string jobId, startTime, endTime;
        istringstream iss(line);
        iss >> jobId >> startTime >> endTime;

        Job j = Job(jobId, startTime, endTime);
        res.push_back(j);
    }

    return res;
}

// J1 0023 45
// J2 0025 10
// J3 0100 60
// J4 0108 20
// J5 0201 30
// J6 0112 30

// job: J4 get assigned to M1
// job : J6 get assigned to M3
// job : J3 get assigned to M2
// job : J2 get assigned to M2
// job : J5 get assigned to M1
// job : J1 get assigned to M1

int main() {
    vector<Job> jobs = parseStdin();
    unordered_map<string, string> res = jobScheduler(jobs);
    for (auto i : res) {
      cout << "job: " << i.first << " get assigned to " << i.second << endl;
    }

    return 0;
}```
