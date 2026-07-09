"""
Merge k Sorted Lists — https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists, each sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Approaches:
    1. mergeKLists — min-heap over list heads. Time: O(N log k), Space: O(k).
"""

import heapq
from typing import List, Optional


class ListNode:
    def __init__(self, v: int):
        self.val = v
        self.next: Optional["ListNode"] = None


# Time: O(N log k), Space: O(k)
def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    if not lists:
        return None

    head = ListNode(-1)
    cursor = head

    # Python's heapq is a min-heap; use (val, tiebreaker, node) since ListNode
    # itself isn't comparable when vals tie.
    pq: List = []
    counter = 0
    for node in lists:
        if node is None:
            continue
        heapq.heappush(pq, (node.val, counter, node))
        counter += 1

    while pq:
        _, _, curr = heapq.heappop(pq)

        # print(curr.val)

        if curr.next is not None:
            heapq.heappush(pq, (curr.next.val, counter, curr.next))
            counter += 1

        curr.next = None
        cursor.next = curr
        cursor = cursor.next

    return head.next


if __name__ == "__main__":
    l1 = ListNode(1)
    l1.next = ListNode(4)
    l1.next.next = ListNode(5)

    l2 = ListNode(1)
    l2.next = ListNode(3)
    l2.next.next = ListNode(4)

    l3 = ListNode(2)
    l3.next = ListNode(6)

    lists = [l1, l2, l3]
    res = mergeKLists(lists)
    while res:
        print(res.val)
        res = res.next
