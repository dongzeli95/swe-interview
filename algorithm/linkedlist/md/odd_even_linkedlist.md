```cpp
// https://leetcode.com/problems/odd-even-linked-list

/*
Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.
The first node is considered odd, and the second node is even, and so on.
Note that the relative order inside both the even and odd groups should remain as it was in the input.
You must solve the problem in O(1) extra space complexity and O(n) time complexity.

Ex1:
Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]

Ex2:
Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]
*/

// 2 3 6 7

// [2, 3, 1, 5, 6, 4, 7]
// [2, 3, 6, 1, 5, 4, 7]

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
ListNode* oddEvenList(ListNode* head) {
    if (!head || !head->next) {
        return head;
    }

    ListNode* odd = head;
    ListNode* even = head->next;
    ListNode* evenHead = even;

    while (even && even->next) {
        odd->next = even->next;
        odd = odd->next;
        even->next = odd->next;
        even = even->next;
    }

    odd->next = evenHead;
    return head;
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
    vector<int> nums = {1,2,3,4,5};
    ListNode* head = createLinkedList(nums);
    ListNode* res = oddEvenList(head);
    ListNode* expected = createLinkedList({1,3,5,2,4});
    assert(compareLinkedLists(res, expected));

    nums = {2,1,3,5,6,4,7};
    head = createLinkedList(nums);
    res = oddEvenList(head);
    expected = createLinkedList({2,3,6,7,1,5,4});
    assert(compareLinkedLists(res, expected));

    return 0;
}```
