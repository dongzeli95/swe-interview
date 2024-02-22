// https://leetcode.com/problems/detonate-the-maximum-bombs/description/

/*
You are given a list of bombs. 
The range of a bomb is defined as the area where its effect can be felt. 
This area is in the shape of a circle with the center as the location of the bomb.
The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri].
xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb, whereas ri denotes the radius of its range.
You may choose to detonate a single bomb. When a bomb is detonated, it will detonate all bombs that lie in its range. 
These bombs will further detonate the bombs that lie in their ranges.
Given the list of bombs, return the maximum number of bombs that can be detonated if you are allowed to detonate only one bomb.

Ex1:
Input: bombs = [[2,1,3],[6,1,4]]
Output: 2
Explanation:
The above figure shows the positions and ranges of the 2 bombs.
If we detonate the left bomb, the right bomb will not be affected.
But if we detonate the right bomb, both bombs will be detonated.
So the maximum bombs that can be detonated is max(1, 2) = 2.

Ex2:
Input: bombs = [[1,1,5],[10,10,5]]
Output: 1
Explanation:
Detonating either bomb will not detonate the other bomb, so the maximum number of bombs that can be detonated is 1.

Ex3:
Input: bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]
Output: 5
Explanation:
The best bomb to detonate is bomb 0 because:
- Bomb 0 detonates bombs 1 and 2. The red circle denotes the range of bomb 0.
- Bomb 2 detonates bomb 3. The blue circle denotes the range of bomb 2.
- Bomb 3 detonates bomb 4. The green circle denotes the range of bomb 3.
Thus all 5 bombs are detonated.

*/

#include <vector>
#include <unordered_set>

using namespace std;

// Cannot use naive approach for x+r, x-r, y+r, y-r because that's a rectangular coverage, we want circular.
long long distanceSquare(int x1, int x2, int y1, int y2) {
    return (long long)(x1 - x2) * (x1 - x2) + (long long)(y1 - y2) * (y1 - y2);
}

// Time: O(n^3), we are trying for n bombs and each graph have worst of n^2 edges.
// Space: O(n), but if we build our own graph for saving avg time complexity, space would be O(n^2)
void dfs(vector<vector<int>>& bombs,
    int idx,
    int x, int y, int r,
    unordered_set<int>& detonated) {
    int n = bombs.size();
    for (int i = 0; i < n; i++) {
        int nx = bombs[i][0];
        int ny = bombs[i][1];
        int nr = bombs[i][2];
        if ((long long)r * r < distanceSquare(x, nx, y, ny)) continue;
        if (detonated.count(i)) continue;
        detonated.insert(i);

        dfs(bombs, i, nx, ny, nr, detonated);
    }
}

int maximumDetonation(vector<vector<int>>& bombs) {
    int n = bombs.size();
    int res = 0;
    for (int i = 0; i < n; i++) {
        unordered_set<int> detonated;
        detonated.insert(i);
        dfs(bombs, i, bombs[i][0], bombs[i][1], bombs[i][2], detonated);
        int count = detonated.size();
        res = max(res, count);
    }

    return res;
}