# https://leetcode.com/problems/insert-delete-getrandom-o1/

# Implement the RandomizedSet class:

# RandomizedSet() Initializes the RandomizedSet object.
# bool insert(int val) Inserts an item val into the set if not present. 
# Returns true if the item was not present, false otherwise.

# bool remove(int val) Removes an item val from the set if present. 
# Returns true if the item was present, false otherwise.

# int getRandom() Returns a random element from the current set of elements (it's guaranteed that at least one element exists when this method is called). 
# Each element must have the same probability of being returned.

# You must implement the functions of the class such that each function works in average O(1) time complexity.

# Ex1:
# Input
# ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
# [[], [1], [2], [2], [], [1], [2], []]
# Output
# [null, true, false, true, 2, true, false, 2]

# Explanation
# RandomizedSet randomizedSet = new RandomizedSet();
# randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
# randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
# randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
# randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
# randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
# randomizedSet.insert(2); // 2 was already in the set, so return false.
# randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return 2.

# [1, 2, 3]

# Why we can't use similar hashmap + array to remove element in LRU cache problem?
# Because we need to insert on one side and remove on the other side.
# this means no matter how we optimize, we always ended up with O(n) time complexity for hashmap indices update.
# Not like in this problem, we only have one side to insert and remove, so hashmap indices update is O(1) time complexity.

import random

# Time: O(1), Space: O(n)
class RandomizedSet:
    def __init__(self):
        self.arr = []
        self.m = {}

    def insert(self, val: int) -> bool:
        if val in self.m:
            return False
        self.arr.append(val)
        idx = len(self.arr)-1
        self.m[val] = idx
        return True

    def remove(self, val: int) -> bool:
        if val not in self.m:
            return False
        
        idx = self.m[val]
        lastIdx = len(self.arr)-1
        self.m[self.arr[lastIdx]] = idx
        self.arr[idx], self.arr[lastIdx] = self.arr[lastIdx], self.arr[idx]
        self.arr.pop()
        del self.m[val]
        return True

    def getRandom(self) -> int:
        random_index = random.randint(0, len(self.arr) - 1)
        return self.arr[random_index]

def main():
    randomized_set = RandomizedSet()
    
    # Test insert operation
    assert randomized_set.insert(1) == True
    
    # Test remove operation when element is not present
    assert randomized_set.remove(2) == False
    
    # Test insert operation
    assert randomized_set.insert(2) == True
    
    # Can't assert getRandom because it's random
    _ = randomized_set.getRandom()
    
    # Test remove operation
    assert randomized_set.remove(1) == True
    
    # Test insert operation when element is already present
    assert randomized_set.insert(2) == False
    
    # Can't assert getRandom because it's random
    _ = randomized_set.getRandom()
    
    print("All tests passed!")

if __name__ == "__main__":
    main()