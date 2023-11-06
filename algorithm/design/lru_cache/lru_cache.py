# https://leetcode.com/problems/lru-cache/

# Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

# Implement the LRUCache class:

# LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
# int get(int key) Return the value of the key if the key exists, otherwise return -1.
# void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
# The functions get and put must each run in O(1) average time complexity.

# Ex1:
# Input
# ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
# [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
# Output
# [null, null, null, 1, null, -1, null, -1, 3, 4]

# Explanation
# LRUCache lRUCache = new LRUCache(2);
# lRUCache.put(1, 1); // cache is {1=1}
# lRUCache.put(2, 2); // cache is {1=1, 2=2}
# lRUCache.get(1);    // return 1
# lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
# lRUCache.get(2);    // returns -1 (not found)
# lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
# lRUCache.get(1);    // return -1 (not found)
# lRUCache.get(3);    // return 3
# lRUCache.get(4);    // return 4

class DDLNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev, self.next = None, None

class DDL:
    def __init__(self):
        self.head = DDLNode(-1, -1)
        self.tail = DDLNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.m = {}
        self.ddl = DDL()

    def remove(self, node):
        node.next.prev = node.prev
        node.prev.next = node.next

    def insert_end(self, node):
        node.next = self.ddl.tail
        node.prev = self.ddl.tail.prev
        self.ddl.tail.prev.next = node
        self.ddl.tail.prev = node


    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.m:
            return -1
        
        node = self.m[key]
        # Remove from front and insert to the back.
        self.remove(node)
        self.insert_end(node)

        return node.val
        


    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """

        if key in self.m:
            self.get(key)
            self.m[key].val = value
            return
        
        new_node = DDLNode(key, value)
        self.insert_end(new_node)
        self.m[key] = new_node

        if len(self.m) > self.capacity:
            node = self.ddl.head.next
            self.remove(node)
            self.m.pop(node.key)

        return

def main():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    
    lru.put(3, 3)
    assert lru.get(2) == -1
    
    lru.put(4, 4)
    assert lru.get(1) == -1
    assert lru.get(3) == 3
    assert lru.get(4) == 4


if __name__ == "__main__":
    main()