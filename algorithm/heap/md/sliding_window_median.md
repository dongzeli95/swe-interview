```cpp
#include <set>
#include <deque>
#include <iostream>

using namespace std;

class Median {
public:
  multiset<int> ms;
  deque<int> dq;
  int cap = 0;

  Median(int cap): cap(cap) {}

  // O(logn)
  void add_value(int val) {
      // Insert the new value
      ms.insert(val);
      dq.push_back(val);

      // Adjust the iterator for the first element
      if (ms.size() == 1) {
          it = ms.begin();
          return;
      }

      // Adjust the iterator if the new element is less than the current median
      if (val < *it) {
          it--;
      }

      // If the size exceeds the capacity, remove the oldest element
      if (dq.size() > cap) {
          if (dq.front() <= *it) {
              it++;
          }
          ms.erase(ms.find(dq.front()));
          dq.pop_front();
      }
  }

  // Time: O(1)
  double get_median() {
    bool isOdd = ms.size() % 2;
    if (isOdd) {
        return *it;
    } else {
        auto it_next = next(it);
        return (*it + *it_next) / 2.0;
    }
  }

  void debug() {
    for (auto i : ms) {
        cout << i << endl;
    }
  }

private:
  multiset<int>::iterator it;
  int curr_pos = 0;
};

// [1, 2]
// [1, 2, 3]

// [2, 3] -> 3
// [1, 2, 3] -> 2
// [1, 3]
int main() {
  Median median = Median(2);
  median.add_value(1);
  cout << median.get_median() << endl; // 1

  median.add_value(2);
  cout << median.get_median() << endl; // 1.5

  median.add_value(3);
  cout << median.get_median() << endl; // 2.5

  median.add_value(1);
  cout << median.get_median() << endl; // 2

  median.add_value(9);
  cout << median.get_median() << endl; // 5
  return 0;
}

// [1, 2, 3]```
