"""
Most Profit Assigning Work
https://leetcode.com/problems/most-profit-assigning-work/

Given jobs with (difficulty[i], profit[i]) and workers with ability worker[j]
(a worker can only complete a job with difficulty at most worker[j]), return
the maximum total profit. Each worker takes at most one job; a job can be
taken by multiple workers.

Approaches:
    1. Two pointer greedy: sort jobs by difficulty and workers by ability,
       sweep through jobs while tracking the best profit seen so far.
       Time:  O(n log n + q log q)  (n = #jobs, q = #workers)
       Space: O(n)
"""

from typing import List


# Two pointer, greedy.
# Time:  O(n log n + q log q), n is number of jobs and q is number of workers.
# Space: O(n) number of jobs.
def maxProfitAssignment(
    difficulty: List[int], profit: List[int], worker: List[int]
) -> int:
    jobs = sorted(zip(difficulty, profit))
    worker.sort()
    N = len(profit)
    res = 0
    i = 0
    best = 0
    for ability in worker:
        while i < N and ability >= jobs[i][0]:
            best = max(jobs[i][1], best)
            i += 1
        res += best
    return res
