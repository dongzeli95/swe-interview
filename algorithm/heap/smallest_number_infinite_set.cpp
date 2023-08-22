// https://leetcode.com/problems/smallest-number-in-infinite-set

/*
You have a set which contains all positive integers [1, 2, 3, 4, 5, ...].

Implement the SmallestInfiniteSet class:

SmallestInfiniteSet() Initializes the SmallestInfiniteSet object to contain all positive integers.
int popSmallest() Removes and returns the smallest integer contained in the infinite set.
void addBack(int num) Adds a positive integer num back into the infinite set, if it is not already in the infinite set.

Ex1:

Input
["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"]
[[], [2], [], [], [], [1], [], [], []]
Output
[null, null, 1, 2, 3, null, 1, 4, 5]

Explanation
SmallestInfiniteSet smallestInfiniteSet = new SmallestInfiniteSet();
smallestInfiniteSet.addBack(2);    // 2 is already in the set, so no change is made.
smallestInfiniteSet.popSmallest(); // return 1, since 1 is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 2, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 3, and remove it from the set.
smallestInfiniteSet.addBack(1);    // 1 is added back to the set.
smallestInfiniteSet.popSmallest(); // return 1, since 1 was added back to the set and
                                   // is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 4, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 5, and remove it from the set.

*/

// currmin = 3

// 1, 2, 3, 4, 5, 6, 7, 8
// backMap: 3, 5

#include <set>
#include <queue>
#include <unordered_set>
#include <cassert>
#include <iostream>

using namespace std;

// Priority queue on addBack operation
// Use a min heap to keep track of potential smallest number candidates.
// 
// n: number of addBack, m: number of popSmallest
// Time complexity: O((m+n)*log(n)), Space complexity: O(n)
class SmallestInfiniteSetAddBackWithPQ {
public:
    SmallestInfiniteSetAddBackWithPQ() {
    }

    int popSmallest() {
        if (pq.empty()) {
            int res = currMin;
            currMin++;
            return res;
        }

        int res = pq.top();
        pq.pop();
        // Don't forget to remove the number from the set.
        exist.erase(res);
        return res;
    }

    void addBack(int num) {
        // If the number is already in the set, we don't need to do anything.
        // If the number is greater than the current min, meaning we haven't popped it yet.
        if (exist.count(num) || num >= currMin) {
            return;
        }

        pq.push(num);
        exist.insert(num);
    }

private:
    int currMin = 1;
    priority_queue<int, vector<int>, greater<int>> pq; // min-heap
    unordered_set<int> exist;
};

// Two sets: popSet and backSet.
//
// n: number of addBack, m: number of popSmallest
// Time complexity: O((m+n)*log(m+n)), Space complexity: O(m+n)
class SmallestInfiniteSet {
public:
    SmallestInfiniteSet() {
    }

    int popSmallest() {
        if (popSet.empty() && backSet.empty()) {
            popSet.insert(1);
            return 1;
        }

        if (backSet.empty()) {
            auto lastPop = popSet.end();
            lastPop--;
            int res = *lastPop+1;
            popSet.insert(res);
            return res;
        } else {
            int res = *backSet.begin();
            backSet.erase(backSet.begin());
            popSet.insert(res);
            return res;
        }
    }

    void addBack(int num) {
        if (!popSet.count(num)) {
            return;
        }

        backSet.insert(num);
        popSet.erase(num);
    }

private:
    set<int> popSet;
    set<int> backSet;
};

int main() {
    SmallestInfiniteSet s;

    s.addBack(2);
    assert(s.popSmallest() == 1);
    assert(s.popSmallest() == 2);
    assert(s.popSmallest() == 3);
    s.addBack(1);
    assert(s.popSmallest() == 1);
    assert(s.popSmallest() == 4);
    assert(s.popSmallest() == 5);

    SmallestInfiniteSetAddBackWithPQ sPQ;
    sPQ.addBack(2);
    assert(sPQ.popSmallest() == 1);
    assert(sPQ.popSmallest() == 2);
    assert(sPQ.popSmallest() == 3);
    sPQ.addBack(1);
    assert(sPQ.popSmallest() == 1);
    assert(sPQ.popSmallest() == 4);
    assert(sPQ.popSmallest() == 5);

    return 0;
}