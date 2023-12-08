```cpp
// https://leetcode.com/problems/merge-k-sorted-lists/

/*
You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Ex1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6

Ex2:
Input: lists = []
Output: []


Ex3:
Input: lists = [[]]
Output: []

*/

// [4, 5, 6]

#include <vector>
#include <queue>
#include <iostream>

using namespace std;

class ListNode {
public:
    int val;
    ListNode* next;

    ListNode(int v) : val(v), next(nullptr) {}
};

// Time: O(nlogk), Space: O(k)
ListNode* mergeKLists(vector<ListNode*>& lists) {
    if (lists.empty()) {
        return nullptr;
    }

    ListNode* head = new ListNode(-1);
    ListNode* cursor = head;
    auto cmp = [](ListNode* l1, ListNode* l2) {
        return l1->val > l2->val;
    };

    priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
    int n = lists.size();
    for (int i = 0; i < n; i++) {
        if (!lists[i]) continue;
        pq.push(lists[i]);
    }

    while (!pq.empty()) {
        ListNode* curr = pq.top();
        pq.pop();

        // cout << curr->val << endl;

        if (curr->next) {
            pq.push(curr->next);
        }

        curr->next = nullptr;
        cursor->next = curr;
        cursor = cursor->next;
    }

    return head->next;
}

int main() {
    ListNode* l1 = new ListNode(1);
    l1->next = new ListNode(4);
    l1->next->next = new ListNode(5);

    ListNode* l2 = new ListNode(1);
    l2->next = new ListNode(3);
    l2->next->next = new ListNode(4);

    ListNode* l3 = new ListNode(2);
    l3->next = new ListNode(6);

    vector<ListNode*> lists{l1, l2, l3};
    ListNode* res = mergeKLists(lists);
    while (res) {
        cout << res->val << endl;
        res = res->next;
    }
    return 0;
}```
