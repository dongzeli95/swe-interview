"""
Tests for employee_training.py.

Run: python employee_training_test.py
"""

import unittest

from employee_training import (
    Employee,
    Group,
    GroupStats,
    compute_overdue,
)


class TestEmployeeOverdue(unittest.TestCase):
    def setUp(self):
        # due day = 10 + 30 = 40
        self.emp = Employee("alice", start_day=10, training_days_required=30)

    def test_before_due_day_compliant(self):
        self.assertEqual(self.emp.overdue(35), 0)
        self.assertTrue(self.emp.is_compliant(35))

    def test_boundary_due_day_compliant(self):
        # convention: employee due on day 40 is compliant on day 40
        self.assertEqual(self.emp.overdue(40), 0)
        self.assertTrue(self.emp.is_compliant(40))

    def test_one_day_overdue(self):
        self.assertEqual(self.emp.overdue(41), 1)
        self.assertFalse(self.emp.is_compliant(41))

    def test_many_days_overdue(self):
        self.assertEqual(self.emp.overdue(100), 60)

    def test_check_day_before_start(self):
        # Not yet started — compliant.
        self.assertEqual(self.emp.overdue(5), 0)
        self.assertTrue(self.emp.is_compliant(5))


class TestComputeOverdue(unittest.TestCase):
    def small_tree(self):
        # eng
        # ├── web         [bob due=30]
        # └── infra       [carol due=35]
        #     └── db-oncall  [dave due=30, eve due=40]
        web = Group("web", [], [Employee("bob", 0, 30)])
        db = Group("db-oncall", [], [Employee("dave", 0, 30), Employee("eve", 10, 30)])
        infra = Group("infra", [db], [Employee("carol", 5, 30)])
        eng = Group("eng", [web, infra], [])
        return eng

    def test_leaf_group(self):
        eng = self.small_tree()
        stats = compute_overdue([eng], check_day=60)
        # web has just bob (due=30, check=60 → 30 overdue)
        self.assertEqual(stats["web"].total_employees, 1)
        self.assertEqual(stats["web"].total_overdue, 30)

    def test_intermediate_group(self):
        eng = self.small_tree()
        stats = compute_overdue([eng], check_day=60)
        # infra = carol (25) + db-oncall subtree (dave=30, eve=20) = 75, 3 emps
        self.assertEqual(stats["infra"].total_employees, 3)
        self.assertEqual(stats["infra"].total_overdue, 75)

    def test_root_group_aggregates_everyone(self):
        eng = self.small_tree()
        stats = compute_overdue([eng], check_day=60)
        # eng = bob(30) + carol(25) + dave(30) + eve(20) = 105
        self.assertEqual(stats["eng"].total_employees, 4)
        self.assertEqual(stats["eng"].total_overdue, 105)

    def test_all_compliant_check_day(self):
        eng = self.small_tree()
        stats = compute_overdue([eng], check_day=30)
        self.assertEqual(stats["eng"].total_overdue, 0)
        self.assertEqual(stats["eng"].total_employees, 4)

    def test_empty_group_with_no_subgroups(self):
        empty = Group("empty", [], [])
        eng = Group("eng", [empty], [Employee("bob", 0, 30)])
        stats = compute_overdue([eng], check_day=50)
        self.assertEqual(stats["empty"].total_employees, 0)
        self.assertEqual(stats["empty"].total_overdue, 0)
        self.assertEqual(stats["eng"].total_employees, 1)
        self.assertEqual(stats["eng"].total_overdue, 20)

    def test_forest_multiple_roots(self):
        eng = Group("eng", [], [Employee("bob", 0, 30)])
        sales = Group("sales", [], [Employee("carol", 0, 30)])
        stats = compute_overdue([eng, sales], check_day=60)
        self.assertEqual(stats["eng"].total_employees, 1)
        self.assertEqual(stats["sales"].total_employees, 1)
        self.assertEqual(stats["eng"].total_overdue, 30)
        self.assertEqual(stats["sales"].total_overdue, 30)

    def test_wide_tree_mixed_overdue(self):
        # A ── B [e3=3, e4=1]
        #   ── C [e5=1, e6=0, e7=4]
        #   ── D [e8=7, e9=1]
        # e1=2, e2=0 direct on A
        check_day = 100
        def emp(name, ov):
            return Employee(name, 70 - ov, 30)

        B = Group("B", [], [emp("e3", 3), emp("e4", 1)])
        C = Group("C", [], [emp("e5", 1), emp("e6", 0), emp("e7", 4)])
        D = Group("D", [], [emp("e8", 7), emp("e9", 1)])
        A = Group("A", [B, C, D], [emp("e1", 2), emp("e2", 0)])

        stats = compute_overdue([A], check_day=check_day)
        self.assertEqual(stats["B"].total_employees, 2); self.assertEqual(stats["B"].total_overdue, 4)
        self.assertEqual(stats["C"].total_employees, 3); self.assertEqual(stats["C"].total_overdue, 5)
        self.assertEqual(stats["D"].total_employees, 2); self.assertEqual(stats["D"].total_overdue, 8)
        self.assertEqual(stats["A"].total_employees, 9); self.assertEqual(stats["A"].total_overdue, 19)


if __name__ == "__main__":
    unittest.main(verbosity=2)
