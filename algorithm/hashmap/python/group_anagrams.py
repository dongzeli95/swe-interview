"""
Group Anagrams
https://www.techiedelight.com/group-anagrams-together-given-list-words/

Given a list of words, efficiently group all anagrams.

Approaches:
1. Hash by character-count signature (encoded string of char + count for a-z, A-Z).
   Time: O(N * K) where N = number of words, K = max word length.
   Space: O(N * K) for the hash map storing all words grouped by signature.
"""

from collections import defaultdict
from typing import List


def encodeStr(s: str) -> str:
    m = defaultdict(int)
    for c in s:
        m[c] += 1

    res = []
    for i in range(26):
        c = chr(i + ord('a'))
        if c not in m:
            continue
        res.append(c)
        res.append(str(m[c]))

    for i in range(26):
        c = chr(i + ord('A'))
        if c not in m:
            continue
        res.append(c)
        res.append(str(m[c]))

    return ''.join(res)


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    if not strs:
        return []

    anagramMap = defaultdict(list)
    for s in strs:
        h = encodeStr(s)
        anagramMap[h].append(s)

    return [group for group in anagramMap.values()]


if __name__ == "__main__":
    input_words = ["CARS", "REPAID", "DUES", "NOSE", "SIGNED", "LANE", "PAIRED",
                   "ARCS", "GRAB", "USED", "ONES", "BRAG", "SUED", "LEAN",
                   "SCAR", "DESIGN"]
    expected_output = [
        ["CARS", "ARCS", "SCAR"],
        ["REPAID", "PAIRED"],
        ["DUES", "USED", "SUED"],
        ["NOSE", "ONES"],
        ["SIGNED", "DESIGN"],
        ["LANE", "LEAN"],
        ["GRAB", "BRAG"],
    ]

    result = groupAnagrams(input_words)

    # Sort the result and expected_output to compare them
    result_sorted = sorted([sorted(g) for g in result])
    expected_sorted = sorted([sorted(g) for g in expected_output])

    for group in result:
        print(" ".join(group))

    assert result_sorted == expected_sorted

    print("Test passed!")
