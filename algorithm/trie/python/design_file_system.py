"""
LeetCode 1166: Design File System
https://leetcode.com/problems/design-file-system/description/

Approaches:
1. Trie of path components:
   - createPath: O(T) where T is the number of components in the path.
   - get:        O(T) where T is the number of components in the path.
   - Space:      O(T) per unique path stored in the trie.
"""

from typing import Dict, List


class TrieNode:
    __slots__ = ("child", "isFile", "content")

    def __init__(self) -> None:
        self.child: Dict[str, "TrieNode"] = {}
        self.isFile: bool = False
        self.content: int = -1


# Time: O(T) to add a path to the trie if it contains T components
# Space: O(T) for each unique path.
class FileSystem:
    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def _split(self, path: str) -> List[str]:
        result: List[str] = []
        cur = ""
        # Skip the leading '/'; mirror the C++ loop starting at index 1.
        for i in range(1, len(path)):
            c = path[i]
            if c == '/':
                result.append(cur)
                cur = ""
            else:
                cur += c
        result.append(cur)
        return result

    def _insert(self, path: List[str], value: int) -> bool:
        n = len(path)
        cur = self.root
        for i in range(n):
            if path[i] not in cur.child:
                if i != n - 1:
                    return False
                cur.child[path[i]] = TrieNode()
            else:
                if i == n - 1:
                    return False  # the path already exists
            cur = cur.child[path[i]]
        cur.isFile = True
        cur.content = value
        return True

    def _find(self, path: List[str]) -> int:
        cur = self.root
        for comp in path:
            if comp not in cur.child:
                return -1
            cur = cur.child[comp]
        return cur.content

    def create(self, path: str, value: int) -> bool:
        p = self._split(path)
        return self._insert(p, value)

    # LeetCode's official signature is `createPath`; alias for API parity.
    def createPath(self, path: str, value: int) -> bool:
        return self.create(path, value)

    def get(self, path: str) -> int:
        p = self._split(path)
        return self._find(p)
