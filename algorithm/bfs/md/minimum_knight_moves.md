```cpp
// https://leetcode.com/problems/minimum-knight-moves/

/*
In an infinite chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0].
A knight has 8 possible moves it can make, as illustrated below. 
Each move is two squares in a cardinal direction, then one square in an orthogonal direction.

Return the minimum number of steps needed to move the knight to the square [x, y]. It is guaranteed the answer exists.

Ex1:
Input: x = 2, y = 1
Output: 1
Explanation: [0, 0] → [2, 1]

Ex2:
Input: x = 5, y = 5
Output: 4
Explanation: [0, 0] → [2, 1] → [4, 2] → [3, 4] → [5, 5]

*/

// (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_set>
#include <cassert>

using namespace std;

struct Move {
    int x;
    int y;
    int steps;

    void print() {
        cout << "x: " << x << " y: " << y << " steps: " << steps << endl;
    }

    Move(int x, int y, int steps) : x(x), y(y), steps(steps) {}
};

// Time: O(max(x, y) ^ 2), Space: O(max(x, y) ^ 2)
int minKnightMoves(int x, int y) {
    vector<pair<int, int>> neighbors {{-1, 2}, {1, 2},
                                    {2, 1}, {2, -1},
                                    {1, -2}, {-1, -2},
                                    {-2, -1}, {-2, 1}};
    unordered_set<string> visited;
    queue<Move> q;
    q.push(Move(0, 0, 0));
    visited.insert("0#0");

    while (!q.empty()) {
        Move curr = q.front();
        q.pop();
        // Found our destination
        if (curr.x == x && curr.y == y) {
            return curr.steps;
        }

        // Explore next step
        for (int i = 0; i < 8; i++) {
            int tempX = curr.x + neighbors[i].first;
            int tempY = curr.y + neighbors[i].second;

            string hash = to_string(tempX) + "#" + to_string(tempY);
            if (visited.count(hash)) continue;
            visited.insert(hash);

            q.push(Move(tempX, tempY, curr.steps+1));
        }
    }

    return -1;
}

string hashPosition(int x, int y) {
    return to_string(x) + "#" + to_string(y);
}

// Bi-directional BFS
int minKnightMovesBidirectional(int x, int y) {
    vector<pair<int, int>> offsets{
        {1, 2}, {2, 1}, {2, -1}, {1, -2},
        {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}
    };

    queue<Move> originQueue, targetQueue;
    originQueue.push(Move(0, 0, 0));
    targetQueue.push(Move(x, y, 0));

    unordered_map<string, int> originDistance, targetDistance;
    originDistance[hashPosition(0, 0)] = 0;
    targetDistance[hashPosition(x, y)] = 0;

    while (true) {
        Move origin = originQueue.front();
        originQueue.pop();

        string originXY = hashPosition(origin.x, origin.y);
        if (targetDistance.count(originXY)) {
            return origin.steps + targetDistance[originXY];
        }

        Move target = targetQueue.front();
        targetQueue.pop();

        string targetXY = hashPosition(target.x, target.y);
        if (originDistance.count(targetXY)) {
            return target.steps + originDistance[targetXY];
        }

        for (const auto& offset : offsets) {
            // expand from the origin
            int nextOriginX = origin.x + offset.first;
            int nextOriginY = origin.y + offset.second;
            string nextOriginXY = hashPosition(nextOriginX, nextOriginY);

            if (!originDistance.count(nextOriginXY)) {
                originQueue.push(Move(nextOriginX, nextOriginY, origin.steps + 1));
                originDistance[nextOriginXY] = origin.steps + 1;
            }

            // expand from the target
            int nextTargetX = target.x + offset.first;
            int nextTargetY = target.y + offset.second;
            string nextTargetXY = hashPosition(nextTargetX, nextTargetY);

            if (!targetDistance.count(nextTargetXY)) {
                targetQueue.push(Move(nextTargetX, nextTargetY, target.steps + 1));
                targetDistance[nextTargetXY] = target.steps + 1;
            }
        }
    }

    return -1;
}


int main() {
    assert(minKnightMoves(2, 1) == 1);
    assert(minKnightMovesBidirectional(2, 1) == 1);

    assert(minKnightMoves(5, 5) == 4);
    assert(minKnightMovesBidirectional(5, 5) == 4);

    return 0;
}```
