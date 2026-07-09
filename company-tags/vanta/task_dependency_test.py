"""
Tests for task_dependency.py.

Run:  python -m pytest company-tags/vanta/task_dependency_test.py -v
   OR python  company-tags/vanta/task_dependency_test.py     (uses stdlib unittest)
"""

import unittest

from task_dependency import Task, ancestors_of_target, dependencies_of_targets


def is_topo_order(order: list[str], edges: dict[str, list[str]]) -> bool:
    """edges: dep -> list of dependents. Return True iff every dep appears
    before its dependent in `order` (restricted to the ids in `order`)."""
    idx = {node: i for i, node in enumerate(order)}
    for dep, dependents in edges.items():
        if dep not in idx:
            continue
        for dependent in dependents:
            if dependent in idx and idx[dep] >= idx[dependent]:
                return False
    return True


class TestDependenciesOfTargets(unittest.TestCase):
    def small_graph(self):
        # F → {D, E}   D → {A, B, C}   E → {}   A,B,C → {}
        return [
            Task("A"),
            Task("B"),
            Task("C"),
            Task("D", ["A", "B", "C"]),
            Task("E"),
            Task("F", ["D", "E"]),
        ]

    def test_single_target_all_deps(self):
        tasks = self.small_graph()
        result = dependencies_of_targets(tasks, ["F"])
        self.assertEqual(set(result), {"A", "B", "C", "D", "E"})
        self.assertNotIn("F", result)  # target itself excluded
        edges = {"A": ["D"], "B": ["D"], "C": ["D"], "D": ["F"], "E": ["F"]}
        self.assertTrue(is_topo_order(result, edges))

    def test_multiple_targets_dedup(self):
        tasks = self.small_graph()
        # D and E share nothing with each other, but both are targets
        result = dependencies_of_targets(tasks, ["D", "E"])
        # D's deps = {A, B, C}; E has no deps
        self.assertEqual(set(result), {"A", "B", "C"})
        # targets themselves excluded
        self.assertNotIn("D", result)
        self.assertNotIn("E", result)

    def test_overlapping_targets(self):
        tasks = self.small_graph()
        # F's deps include D + D's deps + E; D is itself a target
        # Expected: dedup, targets excluded → {A, B, C, E}
        result = dependencies_of_targets(tasks, ["F", "D"])
        self.assertEqual(set(result), {"A", "B", "C", "E"})
        self.assertNotIn("F", result)
        self.assertNotIn("D", result)

    def test_target_with_no_deps(self):
        tasks = self.small_graph()
        self.assertEqual(dependencies_of_targets(tasks, ["A"]), [])
        self.assertEqual(dependencies_of_targets(tasks, ["A", "B", "C"]), [])

    def test_empty_targets(self):
        tasks = self.small_graph()
        self.assertEqual(dependencies_of_targets(tasks, []), [])

    def test_diamond_dedup(self):
        # A → B, A → C, B → D, C → D  (D is deepest; A depends on B,C)
        # deps of [A] should be {B, C, D}, D appears once
        tasks = [
            Task("D"),
            Task("B", ["D"]),
            Task("C", ["D"]),
            Task("A", ["B", "C"]),
        ]
        result = dependencies_of_targets(tasks, ["A"])
        self.assertEqual(set(result), {"B", "C", "D"})
        self.assertEqual(len(result), 3)  # dedup
        # D must come before B and C
        self.assertLess(result.index("D"), result.index("B"))
        self.assertLess(result.index("D"), result.index("C"))

    def test_unknown_target_raises(self):
        tasks = self.small_graph()
        with self.assertRaises(KeyError):
            dependencies_of_targets(tasks, ["ZZZ"])

    def test_cycle_raises(self):
        # X → Y, Y → X  (cycle)
        tasks = [Task("X", ["Y"]), Task("Y", ["X"]), Task("Z", ["X"])]
        with self.assertRaises(ValueError):
            dependencies_of_targets(tasks, ["Z"])


class TestAncestorsOfTarget(unittest.TestCase):
    def small_graph(self):
        return [
            Task("A"),
            Task("B"),
            Task("C"),
            Task("D", ["A", "B", "C"]),
            Task("E"),
            Task("F", ["D", "E"]),
        ]

    def test_leaf_has_ancestors(self):
        # A is depended on by D; D is depended on by F
        result = ancestors_of_target(self.small_graph(), "A")
        self.assertEqual(set(result), {"D", "F"})
        self.assertNotIn("A", result)

    def test_shallow_ancestor(self):
        # D is depended on by F only
        self.assertEqual(set(ancestors_of_target(self.small_graph(), "D")), {"F"})

    def test_no_ancestors(self):
        # F is not depended on by anything
        self.assertEqual(ancestors_of_target(self.small_graph(), "F"), [])

    def test_unknown_target_raises(self):
        with self.assertRaises(KeyError):
            ancestors_of_target(self.small_graph(), "ZZZ")

    def test_multiple_ancestor_paths(self):
        # A → B, A → C, B → D, C → D
        # ancestors of D = {B, C, A}  (A reaches D through both B and C, should dedup)
        tasks = [
            Task("D"),
            Task("B", ["D"]),
            Task("C", ["D"]),
            Task("A", ["B", "C"]),
        ]
        self.assertEqual(set(ancestors_of_target(tasks, "D")), {"A", "B", "C"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
