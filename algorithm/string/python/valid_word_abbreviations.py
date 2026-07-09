"""
Valid Word Abbreviation
https://leetcode.com/problems/valid-word-abbreviation/

A string can be abbreviated by replacing any number of non-adjacent, non-empty
substrings with their lengths. The lengths should not have leading zeros.

Given a string `word` and an abbreviation `abbr`, return whether the string
matches the given abbreviation.

Approaches:
    1. Two-pointer scan (isValid): walk both strings with pointers i (abbr) and
       j (word). When a digit run starts in abbr, parse the integer and jump j
       forward. Reject leading zeros. Otherwise compare characters one-to-one.
       Time: O(m + n), Space: O(1) extra (ignoring the parsed number substring).
"""


def isnum(c: str) -> bool:
    return '0' <= c <= '9'


def isValid(abbreviation: str, word: str) -> bool:
    m = len(word)
    n = len(abbreviation)
    if n > m:
        return False

    i = 0
    j = 0
    while i < n:
        if j >= m:
            return False

        if isnum(abbreviation[i]):
            if abbreviation[i] == '0':
                return False

            idx = i + 1
            while idx < n and isnum(abbreviation[idx]):
                idx += 1

            num = int(abbreviation[i:idx])
            i = idx
            j += num

        if (i >= n and j < m) or (i < n and j >= m):
            return False

        if i >= n and j >= m and i - n != j - m:
            return False

        if j < m and i < n and word[j] != abbreviation[i]:
            return False

        i += 1
        j += 1

    if j < m:
        return False

    return True


if __name__ == "__main__":
    # "s10n" ("s ubstitutio n")
    # "sub4u4" ("sub stit u tion")
    # "12" ("substitution")
    # "su3i1u2on" ("su bst i t u ti on")
    # "substitution" (no substrings replaced)
    print(int(isValid("s10n", "substitution")))  # 1
    print(int(isValid("12", "substitution")))  # 1
    print(int(isValid("sub4u4", "substitution")))  # 1
    print(int(isValid("su3i1u2on", "substitution")))  # 1
    print(int(isValid("substitution", "substitution")))  # 1

    print(int(isValid("s55n", "substitution")))  # 0
    print(int(isValid("s010n", "substitution")))  # 0
    print(int(isValid("s0ubstitution", "substitution")))  # 0

    # Input: word = "internationalization", abbr = "i12iz4n"
    print(int(isValid("i12iz4n", "internationalization")))  # 1
    # Input: word = "apple", abbr = "a2e"
    print(int(isValid("a2e", "apple")))  # 0
