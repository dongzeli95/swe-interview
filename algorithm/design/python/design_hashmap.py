"""
LeetCode 706 - Design HashMap
https://leetcode.com/problems/design-hashmap/description/

Design a HashMap without using any built-in hash table libraries.

Approaches (mirroring the C++ source 1-to-1):
    1. MyHashMap (direct-address table): allocate a fixed-size array of size
       1_000_001 initialized to -1 and index directly by the key.
       - put/get/remove: O(1) time, O(N) space where N = key range (10^6).
    2. MyHashMap (separate chaining with linked lists): a fixed-size bucket
       array (size = 19997) with a multiplicative hash (mult = 12582917), each
       bucket holding a singly-linked list of Node(key, val, next).
       - put/get/remove: O(1) average time, O(size + n) space where n is the
         number of entries. Worst-case O(n) per op on hash collisions.
"""


# -------------------------- Approach 1: direct-address table --------------------------
class MyHashMap:
    def __init__(self):
        # Direct-address table: index by key directly (0 <= key <= 10^6).
        self.data = [-1] * 1_000_001

    def put(self, key: int, val: int) -> None:
        self.data[key] = val

    def get(self, key: int) -> int:
        return self.data[key]

    def remove(self, key: int) -> None:
        self.data[key] = -1


# -------------------------- Approach 2: separate chaining --------------------------
class Node:
    def __init__(self, k: int, v: int, n: "Node | None"):
        self.key = k
        self.val = v
        self.next = n


class MyHashMap2:
    size = 19997
    mult = 12582917

    def __init__(self):
        self.data: list[Node | None] = [None] * MyHashMap2.size

    def hash(self, key: int) -> int:
        return (key * MyHashMap2.mult) % MyHashMap2.size

    def put(self, key: int, val: int) -> None:
        # Remove any earlier instance of that key to avoid duplicate chains.
        self.remove(key)
        h = self.hash(key)
        node = Node(key, val, self.data[h])
        self.data[h] = node

    def get(self, key: int) -> int:
        h = self.hash(key)
        node = self.data[h]
        while node is not None:
            if node.key == key:
                return node.val
            node = node.next
        return -1

    def remove(self, key: int) -> None:
        h = self.hash(key)
        node = self.data[h]
        if node is None:
            return
        if node.key == key:
            self.data[h] = node.next
            return
        while node.next is not None:
            if node.next.key == key:
                node.next = node.next.next
                return
            node = node.next
