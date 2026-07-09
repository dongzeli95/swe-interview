"""
Difference Between Two Objects (Recursive Deep Diff)

Given two arbitrary JSON-like values (dicts, lists, primitives), return a
structure describing where they differ.

Rules (mirroring the reference JS/C++ implementation):
- If the two values are equal, return {} (no difference).
- If exactly one is None, return [obj1, obj2].
- If either is a non-container primitive (not a dict/list), return [obj1, obj2].
- If one is a list and the other is a dict, return [obj1, obj2].
- Otherwise, recurse on keys present in obj1. If a key exists in obj2 too,
  compare recursively; only include the key in the result when the sub-diff
  is non-empty.

Approaches:
    1. Solution.objDiff - Recursive structural diff.
       Time:  O(N) where N is the total number of nodes visited across both
              structures.
       Space: O(D) recursion depth plus O(N) for the returned diff in the
              worst case.
"""

from typing import Any


class Solution:
    def objDiff(self, obj1: Any, obj2: Any) -> Any:
        # Equal values => no difference.
        if obj1 == obj2:
            return {}

        # If exactly one side is None, report the pair as the diff.
        if obj1 is None or obj2 is None:
            return [obj1, obj2]

        # If either side is not a container (dict/list), they are leaves that
        # differ; report the pair.
        if not isinstance(obj1, (dict, list)) or not isinstance(obj2, (dict, list)):
            return [obj1, obj2]

        # Container-kind mismatch (list vs dict) is a leaf-level diff too.
        if isinstance(obj1, list) != isinstance(obj2, list):
            return [obj1, obj2]

        return_object: dict = {}

        # Iterate over keys/indices of obj1 (matching the JS `for (key in obj1)`).
        if isinstance(obj1, dict):
            keys = obj1.keys()
            for key in keys:
                if key in obj2:
                    sub_diff = self.objDiff(obj1[key], obj2[key])
                    if len(sub_diff) > 0:
                        return_object[key] = sub_diff
        else:
            # Both are lists here.
            for idx in range(len(obj1)):
                if idx < len(obj2):
                    sub_diff = self.objDiff(obj1[idx], obj2[idx])
                    if len(sub_diff) > 0:
                        return_object[idx] = sub_diff

        return return_object
