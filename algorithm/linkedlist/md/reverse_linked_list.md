```cpp
// https://leetcode.com/problems/reverse-linked-list

/*
Given the head of a singly linked list, reverse the list, and return the reversed list.

Ex1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Ex2:
Input: head = [1,2]
Output: [2,1]

Ex3:
Input: head = []
Output: []

*/

#include <cassert>
#include <vector>

using namespace std;

class ListNode {
public:
    int val;
    ListNode* next;
    ListNode(int val) {
        this->val = val;
        this->next = nullptr;
    }
};

// Time: O(n), Space: O(1)
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

// Helper function to create a linked list from a vector
ListNode* createLinkedList(const vector<int>& nums) {
    if (nums.empty()) return nullptr;

    ListNode* head = new ListNode(nums[0]);
    ListNode* current = head;

    for (int i = 1; i < nums.size(); i++) {
        current->next = new ListNode(nums[i]);
        current = current->next;
    }

    return head;
}

// Helper function to compare two linked lists
bool compareLinkedLists(ListNode* l1, ListNode* l2) {
    while (l1 && l2) {
        if (l1->val != l2->val) return false;
        l1 = l1->next;
        l2 = l2->next;
    }

    return l1 == nullptr && l2 == nullptr;  // ensure both lists are exhausted
}

int main() {
    // Test case 1
    ListNode* l1 = createLinkedList({ 1, 2, 3, 4, 5 });
    ListNode* reversed1 = reverseList(l1);
    assert(compareLinkedLists(reversed1, createLinkedList({ 5, 4, 3, 2, 1 })));

    // Test case 2
    ListNode* l2 = createLinkedList({ 1, 2 });
    ListNode* reversed2 = reverseList(l2);
    assert(compareLinkedLists(reversed2, createLinkedList({ 2, 1 })));

    // Test case 3
    ListNode* l3 = createLinkedList({});
    ListNode* reversed3 = reverseList(l3);
    assert(compareLinkedLists(reversed3, createLinkedList({})));

    return 0;
}```
