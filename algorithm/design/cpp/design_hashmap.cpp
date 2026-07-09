// https://leetcode.com/problems/design-hashmap/description/

/*
Design a HashMap without using any built-in hash table libraries.

Implement the MyHashMap class:

MyHashMap() initializes the object with an empty map.
void put(int key, int value) inserts a (key, value) pair into the HashMap. 
If the key already exists in the map, update the corresponding value.
int get(int key) returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key.
void remove(key) removes the key and its corresponding value if the map contains the mapping for the key.

Ex1:
Input
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
Output
[null, null, null, 1, -1, null, 1, null, -1]

Explanation
MyHashMap myHashMap = new MyHashMap();
myHashMap.put(1, 1); // The map is now [[1,1]]
myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
myHashMap.get(1);    // return 1, The map is now [[1,1], [2,2]]
myHashMap.get(3);    // return -1 (i.e., not found), The map is now [[1,1], [2,2]]
myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (i.e., update the existing value)
myHashMap.get(2);    // return 1, The map is now [[1,1], [2,1]]
myHashMap.remove(2); // remove the mapping for 2, The map is now [[1,1]]
myHashMap.get(2);    // return -1 (i.e., not found), The map is now [[1,1]]

*/

/*
In this case, we can use a hashing function to convert the key into an integer within the bounds of our hashmap array's index range. 
In an ideal situation, that would allow us to reduce the size of the hashmap array to the maximum number of entries, which is 10^4. 
Unfortunately, however, it's always possible for collisions to exist when two keys devolve to the same integer via the hashing function.
To deal with collisions, we can just make each of our hashmap array's elements a linked list. 
This will allow us to treat them like a simple stack, where we look first at the most recently added node and then move to the next until we find the correct key.
Since navigating a linked list will drop our lookup time past O(1), 
the goal of a good hashing function is to randomize the keys' hashes enough to limit collisions 
as much as possible for a given hashmap array size, thus keeping down the average lookup time complexity.

Therefore, the size of our hashmap array should probably be at least equal to the number of entries. 
Increasing the size of the hashmap array will naturally reduce collisions (and therefore time complexity) 
at the expense of space complexity, and vice versa. The tradeoff is highly dependent on the quality of the 
hashing function.

There are many, many hashing functions out there, but for this problem we'll use a very simple multiplicative 
hashing function utilizing a large prime multiplier and then modulo the result to the desired size 
(also a prime) of our hashmap array. This should hopefully result in an even distribution of the entries 
throughout the hashmap array.

The get() method is fairly easy, then. We just hash() our key, access the corresponding bucket in our hashmap
 array (data), and navigate through the linked list (if necessary) and return the correct val, or -1 if 
 the key is not found.

For the put() method, we should first remove() any earlier instance of that key to avoid chaining multiple
 versions of a key definition in our linked list. Then we simply form a new ListNode at the head of the proper
  hashmap bucket, pushing any others back.

The remove() method will be similar to the get() method, except that we need to find and stitch together 
the nodes on either side of the node that matches the key, removing it from the linked list entirely.

*/

class MyHashMap {
public:
    int data[1000001];
    MyHashMap() {
        fill(data, data + 1000000, -1);
    }
    void put(int key, int val) {
        data[key] = val;
    }
    int get(int key) {
        return data[key];
    }
    void remove(int key) {
        data[key] = -1;
    }
};

struct Node {
public:
    int key, val;
    Node* next;
    Node(int k, int v, Node* n) {
        key = k;
        val = v;
        next = n;
    }
};
class MyHashMap {
public:
    const static int size = 19997;
    const static int mult = 12582917;
    Node* data[size] = {};

    int hash(int key) {
        return (int)((long)key * mult % size);
    }

    void put(int key, int val) {
        remove(key);
        int h = hash(key);
        Node* node = new Node(key, val, data[h]);
        data[h] = node;
    }

    int get(int key) {
        int h = hash(key);
        Node* node = data[h];
        for (; node != NULL; node = node->next)
            if (node->key == key) return node->val;
        return -1;
    }

    void remove(int key) {
        int h = hash(key);
        Node* node = data[h];
        if (node == NULL) return;
        if (node->key == key) {
            data[h] = node->next;
            delete node;
        }
        else for (; node->next != NULL; node = node->next)
            if (node->next->key == key) {
                Node* temp = node->next;
                node->next = temp->next;
                delete temp;
                return;
        }
    }
};