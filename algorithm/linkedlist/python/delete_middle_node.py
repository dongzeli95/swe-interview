"""
Delete the Middle Node of a Linked List
https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list

Approaches:
    1. deleteMiddle - Slow/fast pointer with length count adjustment. Time: O(n), Space: O(1).
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def count(head: Optional[ListNode]) -> int:
    curr = head
    res = 0
    while curr:
        res += 1
        curr = curr.next
    return res


# Time: O(n), Space: O(1)
def deleteMiddle(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return None

    slow = head
    fast = head
    prev: Optional[ListNode] = None

    while fast.next and fast.next.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    n = count(head)
    if n % 2 == 0:
        prev = slow
        slow = slow.next

    prev.next = slow.next
    slow.next = None

    return head


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

    return l1 is None and l2 is None


if __name__ == "__main__":
    nums1 = [1, 3, 4, 7, 1, 2, 6]
    expected1 = [1, 3, 4, 1, 2, 6]
    head1 = createLinkedList(nums1)
    result1 = deleteMiddle(head1)
    assert compareLinkedLists(result1, createLinkedList(expected1))

    nums2 = [1, 2, 3, 4]
    expected2 = [1, 2, 4]
    head2 = createLinkedList(nums2)
    result2 = deleteMiddle(head2)
    assert compareLinkedLists(result2, createLinkedList(expected2))

    nums3 = [2, 1]
    expected3 = [2]
    head3 = createLinkedList(nums3)
    result3 = deleteMiddle(head3)
    assert compareLinkedLists(result3, createLinkedList(expected3))
