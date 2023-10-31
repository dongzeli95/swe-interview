// https://leetcode.com/problems/lfu-cache/
/*
Design and implement a data structure for a Least Frequently Used (LFU) cache.

Implement the LFUCache class:

LFUCache(int capacity) Initializes the object with the capacity of the data structure.
int get(int key) Gets the value of the key if the key exists in the cache. Otherwise, returns -1.
void put(int key, int value) Update the value of the key if present, or inserts the key if not already present. 
When the cache reaches its capacity, it should invalidate and remove the least frequently used key before inserting a new item. 
For this problem, when there is a tie (i.e., two or more keys with the same frequency), the least recently used key would be invalidated.
To determine the least frequently used key, a use counter is maintained for each key in the cache. 
The key with the smallest use counter is the least frequently used key.

When a key is first inserted into the cache, its use counter is set to 1 (due to the put operation). 
The use counter for a key in the cache is incremented either a get or put operation is called on it.

The functions get and put must each run in O(1) average time complexity.

Ex1:
Input
["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, 3, null, -1, 3, 4]

Explanation
// cnt(x) = the use counter for key x
// cache=[] will show the last used order for tiebreakers (leftmost element is  most recent)
LFUCache lfu = new LFUCache(2);
lfu.put(1, 1);   // cache=[1,_], cnt(1)=1
lfu.put(2, 2);   // cache=[2,1], cnt(2)=1, cnt(1)=1
lfu.get(1);      // return 1
                 // cache=[1,2], cnt(2)=1, cnt(1)=2
lfu.put(3, 3);   // 2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
                 // cache=[3,1], cnt(3)=1, cnt(1)=2
lfu.get(2);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,1], cnt(3)=2, cnt(1)=2
lfu.put(4, 4);   // Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
                 // cache=[4,3], cnt(4)=1, cnt(3)=2
lfu.get(1);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,4], cnt(4)=1, cnt(3)=3
lfu.get(4);      // return 4
                 // cache=[4,3], cnt(4)=2, cnt(3)=3

                
*/

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <list>
#include <iostream>
#include <cassert>

using namespace std;

class DLLNode {
public:
    int key;
    int value;
    int count;
    DLLNode* prev;
    DLLNode* next;
    DLLNode() {}
    DLLNode(int k, int v, int c) : key(k), value(v),
        count(c), next(nullptr), prev(nullptr) {}
};

class DLL {
public:
    DLLNode* head;
    DLLNode* tail;
    DLL() {
        head = new DLLNode(-1, -1, -1);
        tail = new DLLNode(-1, -1, -1);
        head->next = tail;
        tail->prev = head;
    }
};

// Intuition: every frequency, we store a doubly linked list for k,v pair
class LFUCache {
public:
    unordered_map<int, DLLNode*> m;
    unordered_map<int, DLL*> freqs;
    int mn;
    int cap;
    int count;
    LFUCache(int capacity) {
        cap = capacity;
        mn = 0;
        count = 0;
    }

    int get(int key) {
        if (!m.count(key)) {
            return -1;
        }
        DLLNode* node = m[key];
        remove(node);
        insert(node->count + 1, node);
        node->count++;
        return node->value;
    }

    void insert(int f, DLLNode* node) {
        if (!freqs.count(f)) {
            freqs[f] = new DLL();
        }
        node->next = freqs[f]->head->next;
        node->prev = freqs[f]->head;
        freqs[f]->head->next->prev = node;
        freqs[f]->head->next = node;
    }

    void remove(DLLNode* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
        node->prev = nullptr;
        node->next = nullptr;
        if (freqs[node->count]->head->next ==
            freqs[node->count]->tail) {
            freqs.erase(node->count);
            if (mn == node->count) {
                mn++;
            }
        }
    }

    void removeLF() {
        if (!freqs.count(mn)) return;
        DLL* dll = freqs[mn];
        DLLNode* node = dll->tail->prev;
        remove(node);
        m.erase(node->key);
        count--;
    }

    void put(int key, int value) {
        if (cap == 0) return;
        if (!m.count(key)) {
            if (count == cap) {
                removeLF();
            }
            m[key] = new DLLNode(key, value, 1);
            insert(1, m[key]);
            count++;
            mn = 1;
            return;
        }
        m[key]->value = value;
        remove(m[key]);
        m[key]->count++;
        insert(m[key]->count, m[key]);
    }
};

int main() {
    LFUCache lfu(2);
    lfu.put(1, 1);   // cache=[1,_], cnt(1)=1
    lfu.put(2, 2);
    assert(lfu.get(1) == 1);

    lfu.put(3, 3);   // 2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
    assert(lfu.get(2) == -1);
    assert(lfu.get(3) == 3);

    lfu.put(4, 4);   // Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
    assert(lfu.get(1) == -1);
    assert(lfu.get(3) == 3);
    assert(lfu.get(4) == 4);

    return 0;
}