// https://leetcode.com/problems/moving-average-from-data-stream/

/*
Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.
Implement the MovingAverage class:
MovingAverage(int size) Initializes the object with the size of the window size.
double next(int val) Returns the moving average of the last size values of the stream.

Ex1:
Input
["MovingAverage", "next", "next", "next", "next"]
[[3], [1], [10], [3], [5]]
Output
[null, 1.0, 5.5, 4.66667, 6.0]

Explanation
MovingAverage movingAverage = new MovingAverage(3);
movingAverage.next(1); // return 1.0 = 1 / 1
movingAverage.next(10); // return 5.5 = (1 + 10) / 2
movingAverage.next(3); // return 4.66667 = (1 + 10 + 3) / 3
movingAverage.next(5); // return 6.0 = (10 + 3 + 5) / 3

*/

#include <iostream>
#include <deque>

using namespace std;

// Time: O(1), Space: O(size)
class MovingAverage {
public:
    int s;
    deque<int> nums;
    int sum;
    MovingAverage(int size) : s(size), nums({}), sum(0) {};

    double next(int val) {
        sum += val;
        nums.push_back(val);
        if (nums.size() > s) {
            sum -= nums[0];
            nums.pop_front();
        }

        return (double)sum / nums.size() * 1.0;
    }
};

int main() {
    MovingAverage ma = MovingAverage(3);
    cout << ma.next(1) << endl;
    cout << ma.next(10) << endl;
    cout << ma.next(3) << endl;
    cout << ma.next(5) << endl;

    return 0;
}