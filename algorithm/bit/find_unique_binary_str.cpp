// https://leetcode.com/problems/find-unique-binary-string/description/

/*

Given an array of strings nums containing n unique binary strings each of length n, return a binary string of length n that does not appear in nums. 
If there are multiple answers, you may return any of them.

Ex1:
Input: nums = ["01","10"]
Output: "11"
Explanation: "11" does not appear in nums. "00" would also be correct.

Ex2:
Input: nums = ["00","01"]
Output: "11"
Explanation: "11" does not appear in nums. "10" would also be correct.

Ex3:
Input: nums = ["111","011","001"]
Output: "101"
Explanation: "101" does not appear in nums. "000", "010", "100", and "110" would also be correct.

*/

#include <string>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <bitset>

using namespace std;

// Method 1: HashTable
// Time: O(n^2), stoi is O(n)
// Space: O(n) integer hash set.
string findDifferentBinaryString(vector<string>& nums) {
    unordered_set<int> integers;
    for (string num : nums) {
        integers.insert(stoi(num, 0, 2));
    }

    int n = nums.size();
    for (int num = 0; num <= n; num++) {
        if (integers.find(num) == integers.end()) {
            string ans = bitset<16>(num).to_string();
            return ans.substr(16 - n);
        }
    }

    return "";
}

// Method 2: Bit
// Time: O(n^2), Space: O(1)
// count takes O(n)
string findDifferentBinaryString(vector<string>& nums) {
    // Initialize a variable to serve as a bitmask where each bit represents
    // the count of '1's in the binary strings seen so far.
    int bitmask = 0;
    int n = nums.size();

    // Loop through the binary strings.
    for (auto& str : nums) {
        // Count the number of '1's in the current string.
        int countOnes = count(str.begin(), str.end(), '1');
        // Set the corresponding bit in the bitmask.
        bitmask |= 1 << countOnes;
    }

    // Loop indefinitely to find a binary string with a different count of '1's.
    for (int i = 0; i < n; ++i) {
        // Check if the current count of '1's is not represented in the bitmask.
        // The expression (bitmask >> i) shifts the bitmask to the right by 'i' bits,
        // and then checks if the least significant bit is not set.
        if (((bitmask >> i) & 1) == 0) {
            // If not set, we found our number. Return a binary string with 'i' ones
            // followed by enough zeros to match the size of the input binary strings.
            return string(i, '1') + string(nums.size() - i, '0');
        }
    }
    // No return is needed here as the loop is guaranteed to return a string
    // because there are 2^N possible binary strings of length N, and only N of them
    // have unique counts of '1's, leaving at least one string that is different.
}

// Method 3: Cantor's diagonal argument.
/*
For each index i, we will check ith character of ith string in nums.
That is, we check curr = nums[i][i]. We then assign ans[i] to the opposite of curr. 
That is, if curr = "0", we assign ans[i] = "1". If curr = "1", we assign ans[i] = "0".

What is the point of this strategy? ans will differ from every string in at least one position. More specifically:

ans differs from nums[0] in nums[0][0].
ans differs from nums[1] in nums[1][1].
ans differs from nums[2] in nums[2][2].
...
ans differs from nums[n - 1] in nums[n - 1][n - 1].
*/

// Time: O(n), Space: O(1)
string findDifferentBinaryString(vector<string>& nums) {
    string ans;
    for (int i = 0; i < nums.size(); i++) {
        char curr = nums[i][i];
        ans += curr == '0' ? '1' : '0';
    }

    return ans;
}
