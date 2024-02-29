```cpp
// https://leetcode.com/problems/largest-palindromic-number/description/

/*
You are given a string num consisting of digits only.

Return the largest palindromic integer (in the form of a string) that can be formed using digits taken from num. It should not contain leading zeroes.

Notes:

You do not need to use all the digits of num, but you must use at least one digit.
The digits can be reordered.

Ex1:
Input: num = "444947137"
Output: "7449447"
Explanation:
Use the digits "4449477" from "444947137" to form the palindromic integer "7449447".
It can be shown that "7449447" is the largest palindromic integer that can be formed.

Ex2:
Input: num = "00009"
Output: "9"
Explanation:
It can be shown that "9" is the largest palindromic integer that can be formed.
Note that the integer returned should not contain leading zeroes.

*/

#include <vector>
#include <string>

using namespace std;

// Time: O(n), Space: O(n)
string largestPalindromic(string num) {
    vector<int>freqArr(10); // Creating Frequency array of only size 10 as the range of characters is : 0 - 9 (total 10 different values)

    for (char i : num) freqArr[i - '0']++; // Storing the frequency

    string front = "", back = ""; // Intiliasing two empty strings 

    for (int i = 9;i >= 0;i--) { // starting the loop in the reverse as we need to create largest palindrome number
        // if the front and back string is empty and we add zero to it , it will have leading zeroes , which we explicitly do not want in our answer 
        if (i == 0 && front.empty())  continue;

        // if it has only one character as its frequency than we may or may not need it in our final answer as we can have at max only one character in our answer whose frequency is one or else we cannot create palindrome.
        while (freqArr[i] > 1) {
            // Inserting the characters in both the strings
            front += to_string(i);
            back += to_string(i);
            freqArr[i] -= 2;
        }
    }

    //As above mentioned , we can have one value whose frequency is one in our final answer, 
    //so the trick is to add the lasrgest possible value available in the frequency array 
    // to get the largest possible palindrome
    for (int i = 9;i >= 0;i--) {
        if (freqArr[i]) {
            front += to_string(i);
            break;
        }
    }

    // reverse the back string and concatenate it with the front and return it;
    reverse(back.begin(), back.end());

    return front + back;
}```
