"""
LFU Cache - https://leetcode.com/problems/lfu-cache/

Design a Least Frequently Used (LFU) cache with O(1) get and put.

Approaches:
  1. LFUCache: HashMap {key -> node} + HashMap {freq -> doubly linked list of nodes}.
     Track minimum frequency `mn` for O(1) eviction of the LFU (and LRU on tie) key.
     Time: O(1) for both get and put. Space: O(capacity).
"""


class DLLNode:
    def __init__(self, k: int = -1, v: int = -1, c: int = -1) -> None:
        self.key = k
        self.value = v
        self.count = c
        self.prev: "DLLNode | None" = None
        self.next: "DLLNode | None" = None


class DLL:
    def __init__(self) -> None:
        self.head = DLLNode(-1, -1, -1)
        self.tail = DLLNode(-1, -1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head


# Intuition: every frequency, we store a doubly linked list for k,v pair
class LFUCache:
    def __init__(self, capacity: int):
        self.m: dict[int, DLLNode] = {}
        self.freqs: dict[int, DLL] = {}
        self.mn = 0
        self.cap = capacity
        self.count = 0

    def get(self, key: int) -> int:
        if key not in self.m:
            return -1
        node = self.m[key]
        self._remove(node)
        self._insert(node.count + 1, node)
        node.count += 1
        return node.value

    def _insert(self, f: int, node: DLLNode) -> None:
        if f not in self.freqs:
            self.freqs[f] = DLL()
        dll = self.freqs[f]
        node.next = dll.head.next
        node.prev = dll.head
        dll.head.next.prev = node
        dll.head.next = node

    def _remove(self, node: DLLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        dll = self.freqs[node.count]
        if dll.head.next is dll.tail:
            del self.freqs[node.count]
            if self.mn == node.count:
                self.mn += 1

    def _remove_lf(self) -> None:
        if self.mn not in self.freqs:
            return
        dll = self.freqs[self.mn]
        node = dll.tail.prev
        self._remove(node)
        del self.m[node.key]
        self.count -= 1

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key not in self.m:
            if self.count == self.cap:
                self._remove_lf()
            self.m[key] = DLLNode(key, value, 1)
            self._insert(1, self.m[key])
            self.count += 1
            self.mn = 1
            return
        self.m[key].value = value
        self._remove(self.m[key])
        self.m[key].count += 1
        self._insert(self.m[key].count, self.m[key])


if __name__ == "__main__":
    lfu = LFUCache(2)
    lfu.put(1, 1)   # cache=[1,_], cnt(1)=1
    lfu.put(2, 2)
    assert lfu.get(1) == 1

    lfu.put(3, 3)   # 2 is the LFU key, invalidate 2.
    assert lfu.get(2) == -1
    assert lfu.get(3) == 3

    lfu.put(4, 4)   # Both 1 and 3 have same cnt, but 1 is LRU, invalidate 1.
    assert lfu.get(1) == -1
    assert lfu.get(3) == 3
    assert lfu.get(4) == 4

    print("All assertions passed.")
