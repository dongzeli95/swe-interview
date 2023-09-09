```cpp
// https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list

/*
You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list.
The middle node of a linked list of size n is the ⌊n / 2⌋th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.
For n = 1, 2, 3, 4, and 5, the middle nodes are 0, 1, 1, 2, and 2, respectively.

Ex1:
Input: head = [1,3,4,7,1,2,6]
Output: [1,3,4,1,2,6]
Explanation:
The above figure represents the given linked list. The indices of the nodes are written below.
Since n = 7, node 3 with value 7 is the middle node, which is marked in red.
We return the new list after removing this node.

// 1 1
// 3 4
// 4 1
// 7 6

Ex2:
Input: head = [1,2,3,4]
Output: [1,2,4]
Explanation:
The above figure represents the given linked list.
For n = 4, node 2 with value 3 is the middle node, which is marked in red.

// 1 1
// 2 4

Ex3:
Input: head = [2,1]
Output: [2]
Explanation:
The above figure represents the given linked list.
For n = 2, node 1 with value 1 is the middle node, which is marked in red.
Node 0 with value 2 is the only node remaining after removing node 1.

// 2 2
// 1 

*/

#include <cassert>
#include <iostream>
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

int count(ListNode* head) {
    ListNode* curr = head;
    int res = 0;
    // cout << 1 << endl;
    while (curr) {
        res++;
        // cout << curr->val << endl;
        curr = curr->next;
    }

    return res;
}

// Time: O(n), Space: O(1)
ListNode* deleteMiddle(ListNode* head) {
    if (!head || !head->next) {
        return nullptr;
    }

    ListNode* slow = head;
    ListNode* fast = head;
    ListNode* prev = nullptr;

    while (fast->next && fast->next->next) {
        prev = slow;
        slow = slow->next;
        fast = fast->next->next;
    }

    int n = count(head);
    if (n % 2 == 0) {
        prev = slow;
        slow = slow->next;
    }

    prev->next = slow->next;
    slow->next = nullptr;

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
    vector<int> nums1 = {1, 3, 4, 7, 1, 2, 6};
    vector<int> expected1 = {1, 3, 4, 1, 2, 6};
    ListNode* head1 = createLinkedList(nums1);
    ListNode* result1 = deleteMiddle(head1);
    assert(compareLinkedLists(result1, createLinkedList(expected1)));

    vector<int> nums2 = {1, 2, 3, 4};
    vector<int> expected2 = {1, 2, 4};
    ListNode* head2 = createLinkedList(nums2);
    ListNode* result2 = deleteMiddle(head2);
    assert(compareLinkedLists(result2, createLinkedList(expected2)));

    vector<int> nums3 = {2, 1};
    vector<int> expected3 = {2};
    ListNode* head3 = createLinkedList(nums3);
    ListNode* result3 = deleteMiddle(head3);
    assert(compareLinkedLists(result3, createLinkedList(expected3)));

    return 0;
}```
