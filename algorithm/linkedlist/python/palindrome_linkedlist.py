"""
LeetCode 234: Palindrome Linked List
https://leetcode.com/problems/palindrome-linked-list/

Given the head of a singly linked list, return True if it is a palindrome,
False otherwise.

Approaches:
    1. Solution.isPalindrome — Fast/slow pointers to find the middle, reverse
       the second half in place, then compare with the first half.
       Time: O(n), Space: O(1).
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        prev: Optional[ListNode] = None
        cur: Optional[ListNode] = head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        return prev

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True

        # Find the middle (slow ends at the middle for odd length, or at the
        # end of the first half for even length).
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # Reverse the second half.
        second_half = self.reverseList(slow.next)

        # Compare first half with the reversed second half.
        first_half: Optional[ListNode] = head
        while second_half:
            if first_half.val != second_half.val:
                return False
            second_half = second_half.next
            first_half = first_half.next
        return True
