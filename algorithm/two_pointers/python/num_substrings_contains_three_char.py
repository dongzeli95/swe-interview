"""
Number of Substrings Containing All Three Characters
https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/

Given a string s consisting only of characters 'a', 'b', and 'c', return the
number of substrings containing at least one occurrence of all three
characters.

Approaches:
    1. Sliding window with two pointers (char count map).
       Time: O(n), Space: O(1)
"""


# Time: O(n), Space: O(1)
def numberOfSubstrings(s: str) -> int:
    if not s:
        return 0

    char_map = [1, 1, 1]
    n = len(s)

    left, right = 0, 0
    match = 0
    res = 0
    while right < n:
        char_map[ord(s[right]) - ord('a')] -= 1
        if char_map[ord(s[right]) - ord('a')] == 0:
            match += 1

        while left < n and match == 3:
            res += (n - right)
            if char_map[ord(s[left]) - ord('a')] == 0:
                match -= 1
            char_map[ord(s[left]) - ord('a')] += 1
            left += 1

        right += 1

    return res


# abcabc
# left: 0, right: 0, match = 1
# left: 0, right: 1, match = 2
# left: 0, right: 2, match = 3


if __name__ == "__main__":
    s = "abcabc"
    print(numberOfSubstrings(s))

    s = "aaacb"
    print(numberOfSubstrings(s))

    s = "abc"
    print(numberOfSubstrings(s))
