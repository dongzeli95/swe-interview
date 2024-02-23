```cpp
// https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/

/*
You have information about n different recipes. 
You are given a string array recipes and a 2D string array ingredients. 
The ith recipe has the name recipes[i], and you can create it if you have all the needed ingredients from ingredients[i]. 
Ingredients to a recipe may need to be created from other recipes, i.e., ingredients[i] may contain a string that is in recipes.
You are also given a string array supplies containing all the ingredients that you initially have, and you have an infinite supply of all of them.
Return a list of all the recipes that you can create. You may return the answer in any order.
Note that two recipes may contain each other in their ingredients.

Ex1:
Input: recipes = ["bread"], ingredients = [["yeast","flour"]], supplies = ["yeast","flour","corn"]
Output: ["bread"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".

Ex2:
Input: recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".

Ex3:
Input: recipes = ["bread","sandwich","burger"], ingredients = [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich","burger"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".
We can create "burger" since we have the ingredient "meat" and can create the ingredients "bread" and "sandwich".

*/

#include <string>
#include <vector>
#include <unordered_set>

using namespace std;

// Time: O(recipes*ingredients), Space: O(recipes*ingredients + supplies)
bool canMake(string recipe,
    unordered_map<string, vector<string>>& graph,
    unordered_set<string>& suppliesSet,
    unordered_set<string>& recipesSet,
    unordered_set<string>& visited,
    unordered_map<string, bool>& cache) {
    if (cache.count(recipe)) {
        return cache[recipe];
    }

    int n = graph[recipe].size();
    int res = true;
    for (int i = 0; i < n; i++) {
        string ing = graph[recipe][i];
        if (suppliesSet.count(ing)) continue;
        if (!recipesSet.count(ing)) {
            res = false;
            break;
        }

        if (visited.count(ing)) {
            res = false;
            break;
        }

        visited.insert(ing);
        bool sub = canMake(ing, graph, suppliesSet, recipesSet, visited, cache);
        visited.erase(ing);
        if (!sub) {
            res = false;
            break;
        }
    }

    cache[recipe] = res;
    return res;
}

vector<string> findAllRecipes(vector<string>& recipes, vector<vector<string>>& ingredients, vector<string>& supplies) {
    int n = recipes.size();
    // Build graph
    unordered_map<string, vector<string>> graph;
    unordered_set<string> recipesSet;
    for (int i = 0; i < n; i++) {
        string recipe = recipes[i];
        graph[recipe] = ingredients[i];
        recipesSet.insert(recipe);
    }

    int m = supplies.size();
    unordered_set<string> suppliesSet;
    for (int i = 0; i < m; i++) {
        suppliesSet.insert(supplies[i]);
    }

    unordered_map<string, bool> cache;
    vector<string> res;
    for (int i = 0; i < n; i++) {
        if (suppliesSet.count(recipes[i])) {
            res.push_back(recipes[i]);
            continue;
        }

        unordered_set<string> visited;
        visited.insert(recipes[i]);
        if (canMake(recipes[i], graph, suppliesSet, recipesSet, visited, cache)) {
            res.push_back(recipes[i]);
        }
    }

    return res;
}```
