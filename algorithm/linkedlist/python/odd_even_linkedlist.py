"""
Odd Even Linked List
https://leetcode.com/problems/odd-even-linked-list

Given the head of a singly linked list, group all the nodes with odd indices
together followed by the nodes with even indices, and return the reordered list.

Approaches:
    1. oddEvenList: Two-pointer in-place weaving. Time O(n), Space O(1).
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int):
        self.val = val
        self.next: Optional["ListNode"] = None


# Time: O(n), Space: O(1)
def oddEvenList(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    odd = head
    even = head.next
    even_head = even

    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next

    odd.next = even_head
    return head


# Helper function to create a linked list from a list
def create_linked_list(nums: List[int]) -> Optional[ListNode]:
    if not nums:
        return None

    head = ListNode(nums[0])
    current = head

    for i in range(1, len(nums)):
        current.next = ListNode(nums[i])
        current = current.next

    return head


# Helper function to compare two linked lists
def compare_linked_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> bool:
    while l1 and l2:
        if l1.val != l2.val:
            return False
        l1 = l1.next
        l2 = l2.next

    return l1 is None and l2 is None


if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]
    head = create_linked_list(nums)
    res = oddEvenList(head)
    expected = create_linked_list([1, 3, 5, 2, 4])
    assert compare_linked_lists(res, expected)

    nums = [2, 1, 3, 5, 6, 4, 7]
    head = create_linked_list(nums)
    res = oddEvenList(head)
    expected = create_linked_list([2, 3, 6, 7, 1, 5, 4])
    assert compare_linked_lists(res, expected)
