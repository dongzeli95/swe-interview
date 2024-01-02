// https://leetcode.com/problems/palindrome-linked-list/description/

/*
Given the head of a singly linked list, return true if it is a
palindrome
 or false otherwise.

Ex1:
Input: head = [1,2,2,1]
Output: true

Ex2:
Input: head = [1,2]
Output: false
*/
struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};

ListNode* reverseList(ListNode* head) {
    if (!head || !head->next) {
        return head;
    }

    ListNode* prev = nullptr;
    ListNode* cur = head;
    ListNode* next = nullptr;

    while (cur) {
        next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
    }

    return prev;
}

bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;
    ListNode* slow = head, * fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    ListNode* secondHalf = reverseList(slow->next);

    while (secondHalf) {
        if (head->val != secondHalf->val) return false;
        secondHalf = secondHalf->next;
        head = head->next;
    }
    return true;
}