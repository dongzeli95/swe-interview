// https://leetcode.com/problems/minimum-fuel-cost-to-report-to-the-capital/description/

/*

There is a tree (i.e., a connected, undirected graph with no cycles) 
structure country network consisting of n cities numbered from 0 to n - 1 and exactly n - 1 roads. 
The capital city is city 0. 
You are given a 2D integer array roads where roads[i] = [ai, bi] 
denotes that there exists a bidirectional road connecting cities ai and bi.

There is a meeting for the representatives of each city. The meeting is in the capital city.
There is a car in each city. 
You are given an integer seats that indicates the number of seats in each car.
A representative can use the car in their city to travel or change the car and ride with another representative.
The cost of traveling between two cities is one liter of fuel.

Return the minimum number of liters of fuel to reach the capital city.

Ex1:
Input: roads = [[0,1],[0,2],[0,3]], seats = 5
Output: 3
Explanation:
- Representative1 goes directly to the capital with 1 liter of fuel.
- Representative2 goes directly to the capital with 1 liter of fuel.
- Representative3 goes directly to the capital with 1 liter of fuel.
It costs 3 liters of fuel at minimum.
It can be proven that 3 is the minimum number of liters of fuel needed.

Ex2:
Input: roads = [[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], seats = 2
Output: 7
Explanation:
- Representative2 goes directly to city 3 with 1 liter of fuel.
- Representative2 and representative3 go together to city 1 with 1 liter of fuel.
- Representative2 and representative3 go together to the capital with 1 liter of fuel.
- Representative1 goes directly to the capital with 1 liter of fuel.
- Representative5 goes directly to the capital with 1 liter of fuel.
- Representative6 goes directly to city 4 with 1 liter of fuel.
- Representative4 and representative6 go together to the capital with 1 liter of fuel.
It costs 7 liters of fuel at minimum.
It can be proven that 7 is the minimum number of liters of fuel needed.

Ex3:
Input: roads = [], seats = 1
Output: 0
Explanation: No representatives need to travel to the capital city.

*/

/*
Intuition
We can see that taking a car from level l to l + 1 and back to level l to get to the root node is pointless. 
It takes two units of fuel to go from l to l + 1 and back again. 
Instead, the representative at level l + 1 can drive to level l in one unit of fuel. 
As a result, the cars would move from higher to lower levels in order to reach the root node.
We will try to put as many representatives as possible in the same car to save fuel. 
Let's look at an example to see how we should arrange the representatives.
Consider a node node that has a parent node parent. 
Assume there are r representatives in the subtree of node. 
To reach node 0, all representatives in this subtree must pass through parent. 
Let's compute how much fuel would be required to just cross the edge that connects nodes node and parent.
Intitutively, we can think that the worst-case scenario would be the one where all the representatives take their own car and cross the edge. This would require r units of fuel.
The best way would be to put r representatives one by one into the cars until the cars reach seat capacity. 
This would require ceil(r / seats) cars and an equal amount of fuel (since a car takes one unit of fuel to travel over an edge).
For example, if you have 10 representatives in a subtree and the capacity is 3, then you would need ceil(10 / 3) = 4 cars.
Also, regardless of how the representatives arrive at node, 
there will definitely be at least ceil(r / seats) cars. 
This is because all of the representatives in the subtree of node except for the one at node 
would arrive by using at least ceil((r - 1) / seats) cars or more (since we can accommodate 
a maximum of seats people in a car). 
Hence, we already have cars that can seat r - 1 people, 
and there is one representative and one car at node to take all the representatives 
in the required number of cars (1 + ceil(r - 1 / seats) >= ceil(r / seats)). 
That brings us to our solution.

We begin by moving all the representatives in a node's subtree to the node. 
Then, using the minimum fuel calculated by the above formula, move all of the representatives to the parent node. 
So our task is to compute the number of representatives in each node's subtree and add the fuel 
required to move all of the representatives in the node's subtree to the parent node.

The depth-first search (DFS) algorithm can be used to compute the number of representatives in each subtree. 
In DFS, we use a recursive function to explore nodes as far as possible along each branch. 
Upon reaching the end of a branch, we backtrack to the next branch and continue exploring.

Once we encounter an unvisited node, we will take one of its neighbor nodes (if exists) as the next node on this branch. 
Recursively call the function to take the next node as the 'starting node' and solve the subproblem.
*/

#include <vector>

using namespace std;

class Solution {
public:
    long long fuel;

    long long dfs(int node, int parent, vector<vector<int>>& adj, int& seats) {
        // The node itself has one representative.
        int representatives = 1;
        for (auto& child : adj[node]) {
            if (child != parent) {
                // Add count of representatives in each child subtree to the parent subtree.
                representatives += dfs(child, node, adj, seats);
            }
        }

        if (node != 0) {
            // Count the fuel it takes to move to the parent node.
            // Root node does not have any parent so we ignore it.
            fuel += ceil((double)representatives / seats);
        }
        return representatives;
    }

    long long minimumFuelCost(vector<vector<int>>& roads, int seats) {
        int n = roads.size() + 1;
        vector<vector<int>> adj(n);
        for (auto& road : roads) {
            adj[road[0]].push_back(road[1]);
            adj[road[1]].push_back(road[0]);
        }
        dfs(0, -1, adj, seats);
        return fuel;
    }
};