"""
Find All Possible Recipes from Given Supplies
https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/

Approaches:
  1. DFS with memoization + cycle detection via visiting set.
     Time: O(recipes * ingredients), Space: O(recipes * ingredients + supplies)
"""

from typing import Dict, List, Set


def canMake(
    recipe: str,
    graph: Dict[str, List[str]],
    suppliesSet: Set[str],
    recipesSet: Set[str],
    visited: Set[str],
    cache: Dict[str, bool],
) -> bool:
    if recipe in cache:
        return cache[recipe]

    res = True
    for ing in graph[recipe]:
        if ing in suppliesSet:
            continue
        if ing not in recipesSet:
            res = False
            break

        if ing in visited:
            res = False
            break

        visited.add(ing)
        sub = canMake(ing, graph, suppliesSet, recipesSet, visited, cache)
        visited.discard(ing)
        if not sub:
            res = False
            break

    cache[recipe] = res
    return res


def findAllRecipes(
    recipes: List[str],
    ingredients: List[List[str]],
    supplies: List[str],
) -> List[str]:
    n = len(recipes)
    # Build graph
    graph: Dict[str, List[str]] = {}
    recipesSet: Set[str] = set()
    for i in range(n):
        recipe = recipes[i]
        graph[recipe] = ingredients[i]
        recipesSet.add(recipe)

    suppliesSet: Set[str] = set(supplies)

    cache: Dict[str, bool] = {}
    res: List[str] = []
    for i in range(n):
        if recipes[i] in suppliesSet:
            res.append(recipes[i])
            continue

        visited: Set[str] = set()
        visited.add(recipes[i])
        if canMake(recipes[i], graph, suppliesSet, recipesSet, visited, cache):
            res.append(recipes[i])

    return res
