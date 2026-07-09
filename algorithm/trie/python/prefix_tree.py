"""
LeetCode 208: Implement Trie (Prefix Tree)
https://leetcode.com/problems/implement-trie-prefix-tree

Approaches:
1. Trie with fixed-size (26) children array per node
   - insert: Time O(n), Space O(n)
   - search / startsWith: Time O(n), Space O(1)
   - Total Space: O(n*k) where n = number of nodes, k = alphabet size (26)
"""


class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.isWord = False


# n is the number of nodes in the trie.
# k is the total number of unique characters in the alphabet.
# Total Space: O(n*k)
class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Time: O(n), Space: O(n)
    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            idx = ord(ch) - ord('a')
            if curr.children[idx] is None:
                curr.children[idx] = TrieNode()
            curr = curr.children[idx]
        curr.isWord = True

    def search(self, word: str) -> bool:
        res = self.find(word)
        return res is not None and res.isWord

    def startsWith(self, prefix: str) -> bool:
        res = self.find(prefix)
        return res is not None

    # Time: O(n), Space: O(1)
    def find(self, word: str):
        curr = self.root
        for ch in word:
            idx = ord(ch) - ord('a')
            nxt = curr.children[idx]
            if nxt is None:
                return None
            curr = nxt
        return curr


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    print("All assertions passed.")
