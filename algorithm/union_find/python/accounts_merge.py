"""
Accounts Merge - https://leetcode.com/problems/accounts-merge/

Approaches:
1. accountsMergeUF: Union-Find on emails. Time: O(NK * log(NK)), Space: O(NK).
2. accountsMergeDFS: Build an undirected email graph and DFS each component.
   Time: O(NK * log(NK)), Space: O(NK).
"""

from collections import defaultdict
from typing import Dict, List, Set


class UnionFind:
    def __init__(self) -> None:
        self.parents: Dict[str, str] = {}
        self.sizes: Dict[str, int] = defaultdict(lambda: 1)

    # Amortized O(1)
    def find(self, curr: str) -> str:
        if curr not in self.parents:
            return curr
        if self.parents[curr] == curr:
            return curr
        self.parents[curr] = self.find(self.parents[curr])
        return self.parents[curr]

    # Amortized O(1)
    def uni(self, i: str, j: str) -> None:
        p1 = self.find(i)
        p2 = self.find(j)
        if p1 != p2:
            s1 = self.sizes[p1]
            s2 = self.sizes[p2]
            self.sizes[p2] = s1 + s2
            self.parents[p1] = p2


# N accounts, each account have K emails
# Time: O(NK * Log(NK)), Space: O(NK)
def accountsMergeUF(accounts: List[List[str]]) -> List[List[str]]:
    owner: Dict[str, str] = {}
    uf = UnionFind()
    for account in accounts:
        name = account[0]
        email1 = account[1]
        owner[email1] = name
        for e in account[2:]:
            uf.uni(email1, e)
            owner[e] = name

    clusters: Dict[str, Set[str]] = defaultdict(set)
    for email, name in owner.items():
        p = uf.find(email)
        clusters[p].add(p)
        clusters[p].add(email)

    res: List[List[str]] = []
    for p, emails in clusters.items():
        name = owner[p]
        account = [name] + sorted(emails)
        res.append(account)

    return res


def dfs(
    graph: Dict[str, List[str]],
    visited: Set[str],
    res: List[str],
    curr: str,
) -> None:
    res.append(curr)
    for nxt in graph[curr]:
        if nxt in visited:
            continue
        visited.add(nxt)
        dfs(graph, visited, res, nxt)


# N accounts, each account have K emails
# Time: O(NK * Log(NK)), Space: O(NK)
# Although we have a for loop iterating through owner, the time complexity is bounded by graph which is NK.
def accountsMergeDFS(accounts: List[List[str]]) -> List[List[str]]:
    graph: Dict[str, List[str]] = defaultdict(list)
    owner: Dict[str, str] = {}

    for account in accounts:
        name = account[0]
        email1 = account[1]
        owner[email1] = name
        for e in account[2:]:
            graph[e].append(email1)
            graph[email1].append(e)
            owner[e] = name

    visited: Set[str] = set()
    res: List[List[str]] = []
    for email, name in owner.items():
        if email in visited:
            continue

        email_cluster: List[str] = [name]
        visited.add(email)
        dfs(graph, visited, email_cluster, email)
        email_cluster[1:] = sorted(email_cluster[1:])
        res.append(email_cluster)

    return res


if __name__ == "__main__":
    accounts1 = [
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    result1 = accountsMergeUF(accounts1)
    assert len(result1) == 3
    for row in result1:
        print(" ".join(row))

    # Test Case 2
    accounts2 = [
        ["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"],
        ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
        ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"],
        ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
        ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"],
    ]
    result2 = accountsMergeUF(accounts2)
    for row in result2:
        print(" ".join(row))

    print("All test cases passed!")
