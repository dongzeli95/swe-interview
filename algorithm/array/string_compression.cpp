// https://leetcode.com/problems/string-compression

/*
Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:

If the group's length is 1, append the character to s.
Otherwise, append the character followed by the group's length.
The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.
*/

/*
Ex1:
Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".

Ex2:
Input: chars = ["a"]
Output: Return 1, and the first character of the input array should be: ["a"]
Explanation: The only group is "a", which remains uncompressed since it's a single character.

Ex3:
Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".

 */

#include <vector>
#include <string>
#include <iostream>
using namespace std;

void reassign_chars(vector<char> &chars, char current, int& idx, int counter) {
    string groupLen = to_string(counter);
    chars[idx++] = current;
    if (counter == 1) {
        return;
    }

    for (int j = 0; j < groupLen.size(); j++) {
        chars[idx++] = groupLen[j];
    }
}

// Time: O(n), Space: O(1)
int compress(vector<char> & chars)
{
    if (chars.empty()) {
        return 0;
    }

    int res = 0;
    int counter = 1;
    int n = chars.size();
    int idx = 0;

    for (int i = 1; i < n; i++) {
        if (chars[i] == chars[i - 1]) {
            counter++;
        }
        else {
            string groupLen = to_string(counter);
            // +1 for the character itself if the group length greater than 1.
            res += (groupLen.size() + (counter > 1 ? 1 : 0));
            // Reassign the character and group length to the original array.
            reassign_chars(chars, chars[i - 1], idx, counter);

            counter = 1;
        }
    }

    // Add the last group length to the result length.
    string groupLen = to_string(counter);
    // +1 for the character itself if the group length greater than 1.
    res += (groupLen.size() + (counter > 1 ? 1 : 0));
    // Reassign the character and group length to the original array.
    reassign_chars(chars, chars[n - 1], idx, counter);

    return res;
}

int main() {
    vector<char> chars = {'a', 'a', 'b', 'b', 'c', 'c', 'c'};
    assert(compress(chars) == 6);
    assert(chars[0] == 'a');
    assert(chars[1] == '2');
    assert(chars[2] == 'b');
    assert(chars[3] == '2');
    assert(chars[4] == 'c');
    assert(chars[5] == '3');

    vector<char> chars2 = {'a'};
    assert(compress(chars2) == 1);
    assert(chars2[0] == 'a');

    vector<char> chars3 = {'a', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'};
    assert(compress(chars3) == 4);
    assert(chars3[0] == 'a');
    assert(chars3[1] == 'b');
    assert(chars3[2] == '1');
    assert(chars3[3] == '2');
}