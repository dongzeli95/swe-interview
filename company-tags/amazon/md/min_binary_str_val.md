```cpp
#include <string>
#include <iostream>

using namespace std;

// 第二题是这样的，给你一个字符串只有二进制或者“！”，比如这样的“01!”，然后！可以是0或者是1。所以这个字符串可以是“011”或者“010”二者其一。然后你需要算这个字符串的最小值，字符串算值的方法是 ：
// 1. 找出字符串所有的subsquennce是01，所以对于“011”它有两个，这个方法得到的值是2 * val1
// 2. 找出字符串所有的subsquennce是10， 所以对于“010”它有只有一个，这个方法得到的是1 * val2
// 3. val1 和 val2会作为input给你，
// 所以对于“01!”，它可以是“011”最终的值是：2 * val1   + 1 * val2，也可是“010”最终的值是1 * val1 + 1 * val2。然后返回二者最小的那个。当然字符串也可能是“！！！”所以就有2 * 2 * 2 = 8 种可能。然后因为最后的这个值可能会非常大，结果要MOD一个常数(java肯定会overflow如果不做处理)。
// 我最后尝试了dfs + memorization但是有些测试会超时，不知道最优解是啥，可能是贪心。

// count0[i] how many 0 before this point.
// count1[i] how many 1 before this point.
const int MOD = 1e9 + 7;

int minBinaryStringVal(string s, int val1, int val2) {
}


// Q1:
// Imagine you are shopping on Amazon.com for some good weight lifting equipment.The equipment you want has plates of many different weights that you can combine to lift.

// The listing on Amazon gives you an array, plates, that consists of n different weighted plates, in kilograms.There are no two plates with the same weight.The element plates[i] denotes the weight of the ith plate from the top of the stack.You consider weight lifting equipment to be good if the plate at the top is the lightest, and the plate at the bottom is the heaviest.

// More formally, the equipment with array plates will be called good weight lifting equipment if it satisfies the following conditions(assuming the index of the array starts from 1) :

//     •	 plates[1] < plates[i] for all(2 <= i <= n)

//     •	 plates[i] < plates[n] for all(1 <= i <= n - 1)
//     In one move, you can swap the order of adjacent plates.Find out the minimum number of moves required to form good weight lifting equipment.

//     Example :
//     Let the plates be in the order :
// plates = [3, 2, 1]
// In the first move, we swap the first and the second plates.After swapping, the order becomes :
// plates = [2, 3, 1]
// In the second move, we swap the second and the third plates.After swapping, the order becomes :
// plates = [2, 1, 3]
// In the third move, we swap the first and the second plates.After swapping, the order becomes :
// plates = [1, 2, 3]
// Now, the array satisfies the condition after 3 moves.

// Function Description :

// Complete the function getMinMoves in the editor below.
// getMinMoves has the following parameter :
// int plates[n] : the distinct weights
// Returns
// int : the minimum number of operations required
// Constraints

// 2 <= n <= 10 ^ 5
// 1 <= plates[i] <= 109 for all(1 <= i <= n)
// plates consists of distinct integers.
// Input Format For Custom Testing

// The first line contains an integer, n, the number of elements in array plates.

// Each line i of the n subsequent lines(where 1 <= i <= n) contains an integer, plates[i].
// Sample Case 0

// Sample Input For Custom Testing

// STDIN    FUNCTION
// ---- - --------
// 5->plates size, n = 5
// 2        plates = [2, 4, 3, 1, 6]
// 4
// 3
// 1
// 6

// Sample Output
// 3

// Explanation:
// The lightest plate needs to move left.The heaviest plate is already in the correct position.
// • In the first move, swap the third and the fourth plates : plates = [2, 4, 1, 3, 6].
// • Swap the second and the third plates : plates = [2, 1, 4, 3, 6].
// • Swap the first and the second plates : plates = [1, 2, 4, 3, 6].

// Sample Case 1 :
//     Sample Input For Custom Testing

//     STDIN    FUNCTION
//     ---- - --------
//     5->plates size is 5
//     4->plates = [4, 11, 9, 10, 12]
//     11
//     9
//     10
//     12

//     Sample Output
//     0

//     Explanation
//     The plates are already in their correct positions.

int minSwap(vector<int>& arr, int n) {
    int minPlatePosition = (min_element(arr.begin(), arr.end()) - arr.begin());
    int maxPlatePosition = (max_element(arr.begin(), arr.end()) - arr.begin());
    return (minPlatePosition)+(n - 1 - maxPlatePosition) + (minPlatePosition > maxPlatePosition ? -1 : 0);
}

int main() {
    // 2 * val1 + val2 = 4
    // val1 + val2 = 3
    int res = minBinaryStringVal("01!", 1, 2);
    cout << res << endl;
    return 0;
}```
