```cpp
// https://leetcode.com/problems/find-original-array-from-doubled-array/description/

/*
An integer array original is transformed into a doubled array changed by appending twice the value of every element in original, and then randomly shuffling the resulting array.
Given an array changed, return original if changed is a doubled array.
If changed is not a doubled array, return an empty array. 
The elements in original may be returned in any order.

Ex1:
Input: changed = [1,3,4,2,6,8]
Output: [1,3,4]
Explanation: One possible original array could be [1,3,4]:
- Twice the value of 1 is 1 * 2 = 2.
- Twice the value of 3 is 3 * 2 = 6.
- Twice the value of 4 is 4 * 2 = 8.
Other original arrays could be [4,3,1] or [3,1,4].

Ex2:
Input: changed = [6,3,0,1]
Output: []
Explanation: changed is not a doubled array.

Ex3:
Input: changed = [1]
Output: []
Explanation: changed is not a doubled array.

*/

#include <vector>

using namespace std;

// Method 1: Sorting + Hashmap keep track of occurance of original.
// Time: O(nlogn), Space: O(n)
vector<int> findOriginalArray(vector<int>& changed) {
    // It can't be doubled array, if the size is odd
    if (changed.size() % 2) {
        return {};
    }

    // Sort in ascending order
    sort(changed.begin(), changed.end());
    unordered_map<int, int> freq;
    // Store the frequency in the map
    for (int num : changed) {
        freq[num]++;
    }

    vector<int> original;
    for (int num : changed) {
        // If element exists
        if (freq[num]) {
            freq[num]--;
            int twiceNum = num * 2;
            if (freq[twiceNum] > 0) {
                // Pair up the elements, decrement the count
                freq[twiceNum]--;
                // Add the original number to answer
                original.push_back(num);
            }
            else {
                return {};
            }
        }
    }

    return original;
}

// Method 2: Counting sort
// Time: O(n+k) where k is the maximum number in changed.
// Space: O(k)
vector<int> findOriginalArray(vector<int>& changed) {
    // It can't be doubled array, if the size is odd
    if (changed.size() % 2) {
        return {};
    }

    int maxNum = 0;
    // Find the max element in the array
    for (int num : changed) {
        maxNum = max(maxNum, num);
    }

    vector<int> freq(2 * maxNum + 1, 0);
    // Store the frequency in the map
    for (int num : changed) {
        freq[num]++;
    }

    vector<int> original;
    for (int num = 0; num <= maxNum; num++) {
        // If element exists
        if (freq[num]) {
            freq[num]--;

            int twiceNum = num * 2;
            if (freq[twiceNum] > 0) {
                // Pair up the elements, decrement the count
                freq[twiceNum]--;
                // Add the original number to answer
                original.push_back(num);
                num--;
            }
            else {
                return {};
            }
        }
    }

    return original;
}```
