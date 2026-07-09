// https://leetcode.com/problems/rle-iterator/

/*
We can use run-length encoding (i.e., RLE) to encode a sequence of integers. 
In a run-length encoded array of even length encoding (0-indexed), for all even i, encoding[i] tells us the number of times that the non-negative integer value encoding[i + 1] is repeated in the sequence.

For example, the sequence arr = [8,8,8,5,5] can be encoded to be encoding = [3,8,2,5]. 
encoding = [3,8,0,9,2,5] and encoding = [2,8,1,8,2,5] are also valid RLE of arr.
Given a run-length encoded array, design an iterator that iterates through it.

Implement the RLEIterator class:

RLEIterator(int[] encoded) Initializes the object with the encoded array encoded.
int next(int n) Exhausts the next n elements and returns the last element exhausted in this way. 
If there is no element left to exhaust, return -1 instead.

*/

#include <vector>

using namespace std;

class RLEIterator {
public:
    vector<int> encoding;
    int idx;
    RLEIterator(vector<int>& encoding) {
        this->encoding = encoding;
        idx = 0;
    }

    int next(int n) {
        while (n > 0 && idx < encoding.size()) {
            if (n > encoding[idx]) {
                n -= encoding[idx];
                idx += 2;
            }
            else {
                encoding[idx] -= n;
                break;
            }
        }

        if (idx + 1 >= encoding.size()) {
            return -1;
        }

        return encoding[idx + 1];
    }
};