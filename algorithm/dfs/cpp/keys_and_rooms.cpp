// https://leetcode.com/problems/keys-and-rooms

/*
There are n rooms labeled from 0 to n - 1 and all the rooms are locked except for room 0. 
Your goal is to visit all the rooms. However, you cannot enter a locked room without having its key.
When you visit a room, you may find a set of distinct keys in it. 
Each key has a number on it, denoting which room it unlocks, and you can take all of them with you to unlock the other rooms.
Given an array rooms where rooms[i] is the set of keys that you can obtain if you visited room i, return true if you can visit all the rooms, or false otherwise.

Ex1:
Input: rooms = [[1],[2],[3],[]]
Output: true
Explanation:
We visit room 0 and pick up key 1.
We then visit room 1 and pick up key 2.
We then visit room 2 and pick up key 3.
We then visit room 3.
Since we were able to visit every room, we return true.

Ex2:
Input: rooms = [[1,3],[3,0,1],[2],[0]]
Output: false
Explanation: We can not enter room number 2 since the only key that unlocks it is in that room.

*/

#include <vector>
#include <cassert>
#include <unordered_set>

using namespace std;

// N is number of rooms, E is number of keys
// Time: O(N+E), Space: O(N)
void dfs(int curr, vector<vector<int>>& rooms, unordered_set<int>& visited) {
    for (int next: rooms[curr]) {
        if (visited.count(next)) continue;
        visited.insert(next);
        dfs(next, rooms, visited);
    }
}

bool canVisitAllRooms(vector<vector<int>>& rooms) {
    int n = rooms.size();
    unordered_set<int> visited;
    visited.insert(0);
    dfs(0, rooms, visited);

    return visited.size() == n;
}

int main() {
    vector<vector<int>> rooms1 = {{1},{2},{3},{}};
    assert(canVisitAllRooms(rooms1) == true);

    vector<vector<int>> rooms2 = {{1,3},{3,0,1},{2},{0}};
    assert(canVisitAllRooms(rooms2) == false);

    return 0;
}