"""
Removing Stars From a String
https://leetcode.com/problems/removing-stars-from-a-string

Approaches:
    1. Stack-based scan: push non-star chars, pop on '*'. Time: O(N), Space: O(N).
"""


# Time: O(N), Space: O(N)
def removeStars(s: str) -> str:
    if not s:
        return ""

    stack: list[str] = []

    for ch in s:
        if ch == '*' and stack:
            stack.pop()
        else:
            stack.append(ch)

    return "".join(stack)


if __name__ == "__main__":
    s1 = "leet**cod*e"
    assert removeStars(s1) == "lecoe"

    s2 = "erase*****"
    assert removeStars(s2) == ""
