// https://leetcode.com/problems/can-place-flowers/

// You have a long flowerbed in which some of the plots are planted, and some are not.
// However, flowers cannot be planted in adjacent plots.

// Given an integer array flowerbed containing 0's and 1's,
// where 0 means empty and 1 means not empty, and an integer n, 
// return true if n new flowers can be planted in the flowerbed without
// violating the no - adjacent - flowers rule and false otherwise.

// Ex1:
// Input: flowerbed = [1, 0, 0, 0, 1], n = 1
// Output : true

// Ex2:
// Input : flowerbed = [1, 0, 0, 0, 1], n = 2
// Output : false

#include <vector>
#include <iostream>

using namespace std;

// Time: O(n), Space: O(1)
bool canPlaceFlower(vector<int>& flowerbed, int n) {
    if (flowerbed.empty()) {
        return n == 0;
    }

    int capacity = 0;
    int s = flowerbed.size();
    for (int i = 0; i < s; i++) {
        if (flowerbed[i] == 0) {
            if ((i-1 < 0 || flowerbed[i-1] == 0) &&
                (i+1 >= s || flowerbed[i+1] == 0)) {
                capacity++;
                flowerbed[i] = 1;
            }
        }
    }

    return capacity >= n;
}

int main() {
    // 0 0 0 0 0
    vector<int> f1 {0, 0};
    cout << canPlaceFlower(f1, 1) << endl; // true

    vector<int> f2 {1, 0, 0, 0, 1};
    cout << canPlaceFlower(f2, 2) << endl; // false

    vector<int> f3 {0, 0, 1, 0, 1};
    cout << canPlaceFlower(f3, 1) << endl; // true

    vector<int> f4{ 0, 0, 0, 0, 0 };
    cout << canPlaceFlower(f4, 3) << endl; // true

    vector<int> f5{ 1, 0, 0, 0, 0 };
    cout << canPlaceFlower(f5, 3) << endl; // false;

    vector<int> f6{1, 0, 0, 0, 0, 1};
    cout << canPlaceFlower(f6, 2) << endl; // false
    return 0;
}