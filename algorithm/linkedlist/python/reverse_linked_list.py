"""
Reverse Linked List
https://leetcode.com/problems/reverse-linked-list

Given the head of a singly linked list, reverse the list, and return the reversed list.

Approaches:
    1. Iterative pointer reversal - Time: O(n), Space: O(1)
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int):
        self.val = val
        self.next: Optional["ListNode"] = None


# Time: O(n), Space: O(1)
def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    prev: Optional[ListNode] = None
    cur: Optional[ListNode] = head
    next_node: Optional[ListNode] = None

    while cur:
        next_node = cur.next
        cur.next = prev
        prev = cur
        cur = next_node

    return prev


# Helper function to create a linked list from a list
def createLinkedList(nums: List[int]) -> Optional[ListNode]:
    if not nums:
        return None

    head = ListNode(nums[0])
    current = head

    for i in range(1, len(nums)):
        current.next = ListNode(nums[i])
        current = current.next

    return head


# Helper function to compare two linked lists
def compareLinkedLists(l1: Optional[ListNode], l2: Optional[ListNode]) -> bool:
    while l1 and l2:
        if l1.val != l2.val:
            return False
        l1 = l1.next
        l2 = l2.next

    return l1 is None and l2 is None  # ensure both lists are exhausted


if __name__ == "__main__":
    # Test case 1
    l1 = createLinkedList([1, 2, 3, 4, 5])
    reversed1 = reverseList(l1)
    assert compareLinkedLists(reversed1, createLinkedList([5, 4, 3, 2, 1]))

    # Test case 2
    l2 = createLinkedList([1, 2])
    reversed2 = reverseList(l2)
    assert compareLinkedLists(reversed2, createLinkedList([2, 1]))

    # Test case 3
    l3 = createLinkedList([])
    reversed3 = reverseList(l3)
    assert compareLinkedLists(reversed3, createLinkedList([]))
