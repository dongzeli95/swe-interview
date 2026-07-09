"""
LeetCode 1268: Search Suggestions System
https://leetcode.com/problems/search-suggestions-system

Given an array of product strings and a searchWord, return, after each
prefix of searchWord, up to 3 lexicographically-smallest products that
share that prefix.

Approaches:
    1. Trie with stateful current-node pointer + DFS for up to 3 words.
       Build: O(sum(len(p)) for p in products), each query step: O(1) to
       descend one char + O(1) amortized DFS bounded by 3 * (max word len).
"""

from typing import List


class TrieNode:
    def __init__(self) -> None:
        self.isWord: bool = False
        self.val: str = ""
        self.children: List["TrieNode | None"] = [None] * 26


class Trie:
    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()
        self.curr: TrieNode | None = None

    def addProduct(self, p: str) -> None:
        curr = self.root
        for ch in p:
            idx = ord(ch) - ord('a')
            if curr.children[idx] is None:
                curr.children[idx] = TrieNode()
            curr = curr.children[idx]  # type: ignore[assignment]
        curr.isWord = True
        curr.val = p

    def dfs(self, curr: TrieNode, res: List[str]) -> None:
        if len(res) == 3:
            return

        if curr.isWord:
            res.append(curr.val)

        for i in range(26):
            if curr.children[i] is None:
                continue
            self.dfs(curr.children[i], res)  # type: ignore[arg-type]

    def searchWords(self, c: str) -> List[str]:
        if self.curr is None:
            self.curr = self.root

        idx = ord(c) - ord('a')
        if self.curr.children[idx] is None:
            return []

        self.curr = self.curr.children[idx]
        res: List[str] = []
        self.dfs(self.curr, res)  # type: ignore[arg-type]
        return res


def suggestedProducts(products: List[str], searchWord: str) -> List[List[str]]:
    res: List[List[str]] = []
    if not products or not searchWord:
        return res

    t = Trie()
    for p in products:
        t.addProduct(p)

    for ch in searchWord:
        res.append(t.searchWords(ch))

    return res


if __name__ == "__main__":
    products1 = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    searchWord1 = "mouse"
    res = suggestedProducts(products1, searchWord1)
    expected = [
        ["mobile", "moneypot", "monitor"],
        ["mobile", "moneypot", "monitor"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
    ]
    assert res == expected, f"Test 1 failed: {res}"

    products2 = ["havana"]
    searchWord2 = "havana"
    res = suggestedProducts(products2, searchWord2)
    expected = [
        ["havana"],
        ["havana"],
        ["havana"],
        ["havana"],
        ["havana"],
        ["havana"],
    ]
    assert res == expected, f"Test 2 failed: {res}"

    print("All tests passed.")
