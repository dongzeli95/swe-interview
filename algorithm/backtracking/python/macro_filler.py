"""Macro Filler.

Problem: Given a set of ingredients each contributing some number of grams of
macros per unit, a target total macro amount, and a desired macro-ratio between
ingredients, find integer quantities per ingredient whose total macros land
within 10g of the target and whose resulting ingredient ratio deviates least
from the desired ratio.

Approaches:
    1. Backtracking enumeration + deviation scoring.
       - Enumerate all integer-multiplier combinations that get within 10g of
         target via DFS (helper), then pick the combination whose actual
         ingredient ratio minimizes L1 deviation from the desired ratio.
       - Time: O(product of per-ingredient multiplier ranges); Space: O(n * #combos).
"""

from typing import Dict, List


def calculate_deviation(quantities: Dict[str, int], ratios: Dict[str, int]) -> float:
    total = sum(quantities.values())

    deviation = 0.0
    for name, qty in quantities.items():
        actual_ratio = (qty / total) if total > 0 else 0.0
        deviation += abs(actual_ratio - ratios[name] / 10)

    return deviation


def helper(
    macros: List[float],
    target: float,
    curr: List[int],
    res: List[List[int]],
    idx: int,
) -> None:
    if target <= 10:
        res.append(curr[:])
        return

    n = len(macros)
    if idx >= n:
        return

    multiplier = 1
    while multiplier * macros[idx] < target:
        curr[idx] = multiplier
        helper(macros, target - multiplier * macros[idx], curr, res, idx + 1)
        curr[idx] = 1
        multiplier += 1


# as long as we are within 10g of target, we count it as a result.
def macro_filler(
    ingredients: Dict[str, float],
    ratios: Dict[str, int],
    target: float,
) -> Dict[str, int]:
    n = len(ingredients)
    idx_macro: Dict[int, str] = {}
    macros: List[float] = []
    for i, (name, grams) in enumerate(ingredients.items()):
        idx_macro[i] = name
        macros.append(grams)

    curr = [0] * n
    res: List[List[int]] = []
    helper(macros, target, curr, res, 0)

    outputs: List[Dict[str, int]] = []
    for combo in res:
        m: Dict[str, int] = {}
        for j, val in enumerate(combo):
            m[idx_macro[j]] = val
        outputs.append(m)

    min_deviation = float("inf")
    res_map: Dict[str, int] = {}
    for combo_map in outputs:
        d = calculate_deviation(combo_map, ratios)
        if d <= min_deviation:
            min_deviation = d
            res_map = combo_map

    return res_map


if __name__ == "__main__":
    ingredients = {
        "chicken breast": 2.33,  # 10g
        "shrimp": 2.4,
        "beef": 3.07,
    }

    ratios = {
        "chicken breast": 4,
        "shrimp": 4,
        "beef": 2,
    }

    res = macro_filler(ingredients, ratios, 140)

    for name, qty in res.items():
        print(f"{name}: {qty}")
    print()
