"""
LeetCode 71: Simplify Path
https://leetcode.com/problems/simplify-path/

Given a string path (Unix-style absolute path), return the simplified canonical path.
Rules:
    - '.'  refers to the current directory (skip)
    - '..' refers to the parent directory (pop)
    - multiple consecutive '/' are treated as a single '/'
    - anything else (including '...') is a valid file/directory name.

Approaches:
    1. simplifyPath: Split path by '/' and use a stack.
       Time: O(n), Space: O(n)
"""

from typing import List


# Time: O(n), Space: O(n)
def simplifyPath(path: str) -> str:
    if not path:
        return ""

    st: List[str] = []
    for token in path.split('/'):
        if token == "" or token == ".":
            continue
        if token == "..":
            if st:
                st.pop()
        else:
            st.append(token)

    return "/" + "/".join(st)


if __name__ == "__main__":
    res = simplifyPath("/home/")
    print(res)

    res = simplifyPath("/../")
    print(res)

    res = simplifyPath("/home//foo/")
    print(res)
