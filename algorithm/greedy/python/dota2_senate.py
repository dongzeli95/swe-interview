"""
Dota2 Senate — https://leetcode.com/problems/dota2-senate

Approaches:
1. predictPartyVictory: Greedy with a single queue and "floating ban" counters.
   Time O(n), Space O(n) — each senator is processed at most twice on the queue.
"""

from collections import deque


def predictPartyVictory(senate: str) -> str:
    # Number of Senators of each party
    r_count = 0
    d_count = 0

    # Floating Ban Count
    d_floating_ban = 0
    r_floating_ban = 0

    # Queue of Senators
    q: deque = deque()
    for c in senate:
        q.append(c)
        if c == 'R':
            r_count += 1
        else:
            d_count += 1

    # While any party has eligible Senators
    while r_count and d_count:
        # Pop the senator with turn
        curr = q.popleft()

        # If eligible, float the ban on the other party, enqueue again.
        # If not, decrement the floating ban and count of the party.
        if curr == 'D':
            if d_floating_ban:
                d_floating_ban -= 1
                d_count -= 1
            else:
                r_floating_ban += 1
                q.append('D')
        else:
            if r_floating_ban:
                r_floating_ban -= 1
                r_count -= 1
            else:
                d_floating_ban += 1
                q.append('R')

    # Return the party with eligible Senators
    return "Radiant" if r_count else "Dire"


if __name__ == "__main__":
    senate1 = "RD"
    senate2 = "RDD"
    senate3 = "DDRRR"

    assert predictPartyVictory(senate1) == "Radiant"
    assert predictPartyVictory(senate2) == "Dire"
    assert predictPartyVictory(senate3) == "Dire"
