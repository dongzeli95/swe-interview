"""
Vanta phone screen (backup problem): Employee Security Training & Group Aggregation.

Q1: Given an Employee (start_day, training_days_required) and a check_day,
    is the employee compliant? If not, how many days overdue?

    Due day = start_day + training_days_required.
    Convention (CLARIFY with interviewer):
      - check_day <= due_day → compliant, overdue = 0.
      - check_day  > due_day → overdue = check_day - due_day.

Q2: Employees live in a TREE (or forest) of groups. For every group, compute:
      - total_employees:  count of employees in this group's subtree
      - total_overdue:    sum of overdue days across those employees
                          (as of a given check_day)

    Done in a single DFS.

Assumptions to CLARIFY with the interviewer:
    - Group graph is a tree/forest (no cycles, no shared subtrees).
    - Not-yet-started employees (check_day < start_day) are compliant.
    - Boundary: employee due on check_day itself is compliant.

Complexity summary (V = # groups, N = total # employees):
    Time  : O(V + N) — visit every group once, every employee once.
    Space : O(V) for the result dict + O(H) recursion depth
            (H = tree height; H = V in the pathological linear-tree case).
"""

from __future__ import annotations


class Employee:
    def __init__(self, name: str, start_day: int, training_days_required: int):
        self.name = name
        self.start_day = start_day
        self.training_days_required = training_days_required

    def overdue(self, check_day: int) -> int:
        """Days overdue as of check_day, or 0 if compliant.

        Time : O(1)
        Space: O(1)
        """
        due_day = self.start_day + self.training_days_required
        if check_day <= due_day:
            return 0
        return check_day - due_day

    def is_compliant(self, check_day: int) -> bool:
        return self.overdue(check_day) == 0


class Group:
    def __init__(self, g_id: str, sub_groups: list[Group], employees: list[Employee]):
        self.g_id = g_id
        self.sub_groups = sub_groups
        self.employees = employees


class GroupStats:
    def __init__(self, total_employees: int, total_overdue: int):
        self.total_employees = total_employees
        self.total_overdue = total_overdue

    def __repr__(self) -> str:
        return (
            f"GroupStats(total_employees={self.total_employees}, "
            f"total_overdue={self.total_overdue})"
        )


def _dfs(curr: Group, check_day: int, out: dict[str, GroupStats]) -> GroupStats:
    """Aggregate stats for `curr` and its subtree, writing every visited
    group into `out`. Assumes a tree — each group visited exactly once.

    Time : O(subtree_size_in_groups + subtree_employees)
    Space: O(subtree_height) recursion
    """
    stats = GroupStats(0, 0)

    for emp in curr.employees:
        stats.total_employees += 1
        stats.total_overdue += emp.overdue(check_day)

    for child in curr.sub_groups:
        child_stats = _dfs(child, check_day, out)
        stats.total_employees += child_stats.total_employees
        stats.total_overdue += child_stats.total_overdue

    out[curr.g_id] = stats
    return stats


def compute_overdue(roots: list[Group], check_day: int) -> dict[str, GroupStats]:
    """For each group in the forest rooted at `roots`, return its subtree stats.

    Time : O(V + N)  — V groups, N employees, each visited once.
    Space: O(V) result dict + O(H) recursion depth.
    """
    result: dict[str, GroupStats] = {}
    for root in roots:
        _dfs(root, check_day, result)
    return result


# ---------- demo ----------

if __name__ == "__main__":
    # Q1 demo
    alice = Employee("alice", start_day=10, training_days_required=30)  # due day 40
    print("Q1  alice on day 35:", alice.overdue(35), "  compliant?", alice.is_compliant(35))
    print("Q1  alice on day 40:", alice.overdue(40), "  compliant?", alice.is_compliant(40))
    print("Q1  alice on day 50:", alice.overdue(50), "  compliant?", alice.is_compliant(50))

    # Q2 demo
    #     eng
    #    /   \
    #  web  infra
    #        |
    #      db-oncall
    web = Group("web", [], [Employee("bob", 0, 30)])
    db = Group("db-oncall", [], [Employee("dave", 0, 30), Employee("eve", 10, 30)])
    infra = Group("infra", [db], [Employee("carol", 5, 30)])
    eng = Group("eng", [web, infra], [])

    stats = compute_overdue([eng], check_day=60)
    for gid in ["eng", "web", "infra", "db-oncall"]:
        print(f"Q2  {gid:12} {stats[gid]}")
