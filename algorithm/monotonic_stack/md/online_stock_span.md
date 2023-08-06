```cpp
// https://leetcode.com/problems/online-stock-span

/*
Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.

The span of the stock's price in one day is the maximum number of consecutive days (starting from that day and going backward) for which the stock price was less than or equal to the price of that day.

For example, if the prices of the stock in the last four days is [7,2,1,2] and the price of the stock today is 2, then the span of today is 4 because starting from today, the price of the stock was less than or equal 2 for 4 consecutive days.
Also, if the prices of the stock in the last four days is [7,34,1,2] and the price of the stock today is 8, then the span of today is 3 because starting from today, the price of the stock was less than or equal 8 for 3 consecutive days.
Implement the StockSpanner class:

StockSpanner() Initializes the object of the class.
int next(int price) Returns the span of the stock's price given that today's price is price.

Ex1:
Input
["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
[[], [100], [80], [60], [70], [60], [75], [85]]
Output
[null, 1, 1, 1, 2, 1, 4, 6]

Explanation
StockSpanner stockSpanner = new StockSpanner();
stockSpanner.next(100); // return 1
stockSpanner.next(80);  // return 1
stockSpanner.next(60);  // return 1
stockSpanner.next(70);  // return 2
stockSpanner.next(60);  // return 1
stockSpanner.next(75);  // return 4, because the last 4 prices (including today's price of 75) were less than or equal to today's price.
stockSpanner.next(85);  // return 6
*/

#include <vector>
#include <cassert>
#include <stack>

using namespace std;

// Time: O(n), Space: O(n)
class StockPlanner {
public:
    vector<int> prices;
    vector<int> spans;
    StockPlanner() {

    }

    int next(int price) {
        if (prices.empty()) {
            prices.push_back(price);
            spans.push_back(1);
            return 1;
        }

        int span = 1;
        int prev_idx = prices.size()-1;
        while (prev_idx >= 0 && price >= prices[prev_idx]) {
            span += spans[prev_idx];
            prev_idx -= spans[prev_idx];
        }

        prices.push_back(price);
        spans.push_back(span);
        return span;
    }
};

// Improvement: Use a stack to store the index of the prices and spans.
// We don't need to store every price and span in the vector, if the current span is greater than the previous span, we can pop the previous span.
// Time: O(n), Space: O(n)
class StockPlannerWithStack {
public:
    // first is the price, second is the span.
    stack<pair<int, int>> st;
    StockPlannerWithStack() {

    }

    int next(int price) {
        if (st.empty()) {
            st.push({price, 1});
            return 1;
        }

        int span = 1;
        while (!st.empty()) {
            pair<int, int> curr = st.top();
            if (price < curr.first) {
                break;
            }

            span += curr.second;
            st.pop();
        }

        st.push({price, span});
        return span;
    }
};

int main() {
    StockPlanner stockPlanner;
    int res = stockPlanner.next(100);
    assert(res == 1);
    res = stockPlanner.next(80);
    assert(res == 1);
    res = stockPlanner.next(60);
    assert(res == 1);
    res = stockPlanner.next(70);
    assert(res == 2);
    res = stockPlanner.next(60);
    assert(res == 1);
    res = stockPlanner.next(75);
    assert(res == 4);
    res = stockPlanner.next(85);
    assert(res == 6);

    StockPlannerWithStack stockPlannerWithStack;
    res = stockPlannerWithStack.next(100);
    assert(res == 1);
    res = stockPlannerWithStack.next(80);
    assert(res == 1);
    res = stockPlannerWithStack.next(60);
    assert(res == 1);
    res = stockPlannerWithStack.next(70);
    assert(res == 2);
    res = stockPlannerWithStack.next(60);
    assert(res == 1);
    res = stockPlannerWithStack.next(75);
    assert(res == 4);
    res = stockPlannerWithStack.next(85);
    assert(res == 6);

    return 0;
}```
