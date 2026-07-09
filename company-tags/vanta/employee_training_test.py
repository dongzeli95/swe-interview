"""
Tests for employee_training.py.

Run: python employee_training_test.py
"""

import unittest

from employee_training import (
    Employee,
    GroupStats,
    aggregate_group_stats,
    is_compliant,
    overdue_days,
)


class TestQ1(unittest.TestCase):
    def setUp(self):
        self.emp = Employee("alice", start_day=10, training_days_required=30)  # due day 40

    def test_before_due_day_compliant(self):
        self.assertEqual(overdue_days(self.emp, 35), 0)
        self.assertTrue(is_compliant(self.emp, 35))

    def test_boundary_due_day_compliant(self):
        # convention: employee due on day 40 is compliant on day 40
        self.assertEqual(overdue_days(self.emp, 40), 0)
        self.assertTrue(is_compliant(self.emp, 40))

    def test_one_day_overdue(self):
        self.assertEqual(overdue_days(self.emp, 41), 1)
        self.assertFalse(is_compliant(self.emp, 41))

    def test_many_days_overdue(self):
        self.assertEqual(overdue_days(self.emp, 100), 60)

    def test_check_day_before_start(self):
        # Not yet started — compliant.
        self.assertEqual(overdue_days(self.emp, 5), 0)
        self.assertTrue(is_compliant(self.emp, 5))


class TestQ2(unittest.TestCase):
    def small_tree(self):
        # eng
        # ├── web         [bob due=30]
        # └── infra       [carol due=35]
        #     └── db-oncall  [dave due=30, eve due=40]
        groups = {
            "eng": ["web", "infra"],
            "infra": ["db-oncall"],
        }
        employees_by_group = {
            "web":       [Employee("bob",   0,  30)],
            "infra":     [Employee("carol", 5,  30)],
            "db-oncall": [
                Employee("dave", 0,  30),
                Employee("eve",  10, 30),
            ],
        }
        return groups, employees_by_group

    def test_leaf_group(self):
        groups, empg = self.small_tree()
        stats = aggregate_group_stats(groups, empg, check_day=60)
        # web has just bob (due=30, check=60 → 30 overdue)
        self.assertEqual(stats["web"].total_employees, 1)
        self.assertEqual(stats["web"].total_overdue_days, 30)

    def test_intermediate_group(self):
        groups, empg = self.small_tree()
        stats = aggregate_group_stats(groups, empg, check_day=60)
        # infra = carol (25 overdue: due=35) + db-oncall subtree (dave=30, eve=20)
        # total employees = 3 (carol, dave, eve)
        # total overdue = 25 + 30 + 20 = 75
        self.assertEqual(stats["infra"].total_employees, 3)
        self.assertEqual(stats["infra"].total_overdue_days, 75)

    def test_root_group_aggregates_everyone(self):
        groups, empg = self.small_tree()
        stats = aggregate_group_stats(groups, empg, check_day=60)
        # eng = bob + carol + dave + eve
        # total overdue = 30 (bob) + 25 (carol) + 30 (dave) + 20 (eve) = 105
        self.assertEqual(stats["eng"].total_employees, 4)
        self.assertEqual(stats["eng"].total_overdue_days, 105)

    def test_all_compliant_check_day(self):
        groups, empg = self.small_tree()
        # check_day = 30: bob due=30 compliant, carol due=35 compliant, dave due=30 compliant, eve due=40 compliant
        stats = aggregate_group_stats(groups, empg, check_day=30)
        self.assertEqual(stats["eng"].total_overdue_days, 0)
        # employee count unaffected by compliance
        self.assertEqual(stats["eng"].total_employees, 4)

    def test_empty_group_with_no_subgroups(self):
        # A group with no employees and no subgroups should still appear with zeros.
        groups = {"eng": ["empty"]}
        empg = {"eng": [Employee("bob", 0, 30)]}
        stats = aggregate_group_stats(groups, empg, check_day=50)
        self.assertEqual(stats["empty"].total_employees, 0)
        self.assertEqual(stats["empty"].total_overdue_days, 0)
        self.assertEqual(stats["eng"].total_employees, 1)
        self.assertEqual(stats["eng"].total_overdue_days, 20)

    def test_forest_multiple_roots(self):
        # Two disjoint trees
        groups = {
            "eng": ["web"],
            "sales": ["ae"],
        }
        empg = {
            "web": [Employee("bob", 0, 30)],
            "ae":  [Employee("carol", 0, 30)],
        }
        stats = aggregate_group_stats(groups, empg, check_day=60)
        self.assertEqual(stats["eng"].total_employees, 1)
        self.assertEqual(stats["sales"].total_employees, 1)
        self.assertEqual(stats["eng"].total_overdue_days, 30)
        self.assertEqual(stats["sales"].total_overdue_days, 30)


if __name__ == "__main__":
    unittest.main(verbosity=2)
