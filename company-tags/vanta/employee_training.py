"""
Vanta phone screen (backup problem): Employee Security Training & Group Aggregation.

Q1: Given an Employee (start_day, training_days_required) and a check_day,
    is the employee compliant? If not, how many days overdue?

    An employee's training is due on day `start_day + training_days_required`.
    Convention (CLARIFY with interviewer):
      - If check_day <= start_day + training_days_required → compliant, overdue = 0.
      - Else → overdue = check_day - (start_day + training_days_required).

Q2: Employees live in a TREE of groups. For every group in the tree, compute:
      - total_employees:   count of employees in this group's subtree
      - total_overdue_days: sum of overdue days across all those employees
                            (as of a given check_day)

    Do it in one DFS — O(V + total_employees).

Assumptions to CLARIFY:
    - Is the group tree guaranteed connected / single root? (Handle forest below.)
    - Are training-not-yet-started employees compliant? (Yes here.)
    - Boundary: employee due on check_day itself — compliant? (Yes here.)
"""

from dataclasses import dataclass, field


@dataclass
class Employee:
    id: str
    start_day: int
    training_days_required: int


# ---------- Q1: single-employee compliance ----------

def overdue_days(emp: Employee, check_day: int) -> int:
    """Return 0 if compliant, else positive number of days overdue."""
    due_day = emp.start_day + emp.training_days_required
    if check_day <= due_day:
        return 0
    return check_day - due_day


def is_compliant(emp: Employee, check_day: int) -> bool:
    return overdue_days(emp, check_day) == 0


# ---------- Q2: aggregate per group over a tree ----------

@dataclass
class GroupStats:
    total_employees: int = 0
    total_overdue_days: int = 0


def aggregate_group_stats(
    groups: dict[str, list[str]],          # parent_group_id -> list of child group ids
    employees_by_group: dict[str, list[Employee]],  # group_id -> employees directly in it
    check_day: int,
) -> dict[str, GroupStats]:
    """Return a dict mapping every group id to its aggregated stats over its subtree.

    Runs one DFS per connected component in the forest. Cost: O(V + E + N)
    where N is total employees; each employee is visited once via its group.
    """
    result: dict[str, GroupStats] = {}
    # Discover every group id referenced (as parent, as child, or in employees_by_group)
    all_group_ids: set[str] = set(groups.keys()) | set(employees_by_group.keys())
    for children in groups.values():
        all_group_ids.update(children)

    # Find roots — groups that are not any other group's child.
    child_of_someone: set[str] = {c for children in groups.values() for c in children}
    roots = [g for g in all_group_ids if g not in child_of_someone]

    def dfs(group_id: str) -> GroupStats:
        # Employees directly in this group
        stats = GroupStats()
        for emp in employees_by_group.get(group_id, []):
            stats.total_employees += 1
            stats.total_overdue_days += overdue_days(emp, check_day)
        # Recurse into subgroups
        for child in groups.get(group_id, []):
            child_stats = dfs(child)
            stats.total_employees += child_stats.total_employees
            stats.total_overdue_days += child_stats.total_overdue_days
        result[group_id] = stats
        return stats

    for root in roots:
        dfs(root)

    # Sanity: any group not visited (e.g., cycle in groups dict? shouldn't happen in a tree)
    unvisited = all_group_ids - result.keys()
    if unvisited:
        # If input truly is a tree/forest this branch is unreachable. Raise so
        # a bad input surfaces instead of silently returning partial data.
        raise ValueError(f"unvisited groups (cycle or disconnected input?): {unvisited}")

    return result


# ---------- demo ----------

if __name__ == "__main__":
    # Q1 demo
    alice = Employee("alice", start_day=10, training_days_required=30)
    print("Q1  alice due day       :", alice.start_day + alice.training_days_required)  # 40
    print("Q1  alice on day 35     :", overdue_days(alice, 35), "  compliant?", is_compliant(alice, 35))
    print("Q1  alice on day 40     :", overdue_days(alice, 40), "  compliant?", is_compliant(alice, 40))
    print("Q1  alice on day 50     :", overdue_days(alice, 50), "  compliant?", is_compliant(alice, 50))

    # Q2 demo
    #
    # Group tree:
    #     eng
    #    /   \
    #  web  infra
    #        |
    #      db-oncall
    #
    groups = {
        "eng": ["web", "infra"],
        "infra": ["db-oncall"],
        # web and db-oncall are leaves
    }
    employees_by_group = {
        "web":       [Employee("bob",   start_day=0,  training_days_required=30)],
        "infra":     [Employee("carol", start_day=5,  training_days_required=30)],
        "db-oncall": [
            Employee("dave", start_day=0,  training_days_required=30),
            Employee("eve",  start_day=10, training_days_required=30),
        ],
    }
    stats = aggregate_group_stats(groups, employees_by_group, check_day=60)
    for gid in ["eng", "web", "infra", "db-oncall"]:
        s = stats[gid]
        print(f"Q2  {gid:12} employees={s.total_employees}  overdue_days={s.total_overdue_days}")
