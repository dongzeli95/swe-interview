```cpp
// https://leetcode.com/problems/detect-squares/description/

/*
You are given a stream of points on the X-Y plane. Design an algorithm that:

Adds new points from the stream into a data structure. Duplicate points are allowed and should be treated as different points.
Given a query point, counts the number of ways to choose three points from the data structure such that the three points and the query point form an axis-aligned square with positive area.
An axis-aligned square is a square whose edges are all the same length and are either parallel or perpendicular to the x-axis and y-axis.

Implement the DetectSquares class:

DetectSquares() Initializes the object with an empty data structure.
void add(int[] point) Adds a new point point = [x, y] to the data structure.
int count(int[] point) Counts the number of ways to form axis-aligned squares with point point = [x, y] as described above.

Ex1:

Input
["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
[[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
Output
[null, null, null, null, 1, 0, null, 2]

Explanation
DetectSquares detectSquares = new DetectSquares();
detectSquares.add([3, 10]);
detectSquares.add([11, 2]);
detectSquares.add([3, 2]);
detectSquares.count([11, 10]); // return 1. You can choose:
                               //   - The first, second, and third points
detectSquares.count([14, 8]);  // return 0. The query point cannot form a square with any points in the data structure.
detectSquares.add([11, 2]);    // Adding duplicate points is allowed.
detectSquares.count([11, 10]); // return 2. You can choose:
                               //   - The first, second, and third points
                               //   - The first, third, and fourth points

*/

// To compute count(p1) :
//     We try all points p3 which together with p1 form the diagonal of non - empty square, it means abs(p1.x - p3.x) == abs(p1.y - p3.y) && abs(p1.x - p3.x) > 0
//     Since we have 2 points p1 and p3, we can form a square by computing the positions of 2 remain points p2, p4.
//     p2 = (p1.x, p3.y)
//     p4 = (p3.x, p1.y)

#include <vector>

using namespace std;

class DetectSquares { // 216 ms, faster than 66.67%
public:
    int cntPoints[1001][1001] = {};
    vector<pair<int, int>> points;

    void add(vector<int> p) {
        cntPoints[p[0]][p[1]]++;
        points.emplace_back(p[0], p[1]);
    }

    // Time: O(n)
    int count(vector<int> p1) {
        int x1 = p1[0], y1 = p1[1], ans = 0;
        for (auto& [x3, y3] : points) {
            if (abs(x1 - x3) == 0 || abs(x1 - x3) != abs(y1 - y3))
                continue; // Skip empty square or invalid square point!
            ans += cntPoints[x1][y3] * cntPoints[x3][y1];
        }
        return ans;
    }
};```
