```cpp
// https://leetcode.com/problems/subarray-sums-divisible-by-k/description/

/*
Given an integer array nums and an integer k, 
return the number of non-empty subarrays that have a sum divisible by k.
A subarray is a contiguous part of an array.

Ex1:
Input: nums = [4,5,0,-2,-3,1], k = 5
Output: 7
Explanation: There are 7 subarrays with a sum divisible by k = 5:
[4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]

Ex2:
Input: nums = [5], k = 9
Output: 0

*/

/*
As stated previously, our task is to determine 
the number of pairs (i, j) where i < j and (prefixSum[j] - prefix[i]) % k = 0. 
This equality can only be true if prefixSum[i] % k = prefixSum[j] % k. 
We will demonstrate this property.
*/

#include <vector>
#include <unordered_map>

using namespace std;

// Time: O(n), Space: O(k)
int subarraysDivByK(vector<int>& A, int K) {
    int res = 0, sum = 0;
    unordered_map<int, int> m{ {0, 1} };
    for (int num : A) {
        sum = (sum + num % K + K) % K;
        res += m[sum];
        ++m[sum];
    }
    return res;
}```
