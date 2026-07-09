"""
Guess the Word (LeetCode 843)
https://leetcode.com/problems/guess-the-word/description/

Approaches (mirroring the C++ source 1-to-1):
  1. Solution  - Score-based minimax-ish greedy: on each round pick the word whose
                 total match-score against the remaining candidates is highest,
                 then filter by the returned match count. O(N^2) per round.
  2. Solution2 - Weight-and-sort heuristic: precompute per-position letter
                 frequencies, sort words by "similarity to the corpus", then
                 guess in that order and filter by match count. O(N log N) sort
                 plus O(N) filter per round.
  3. Solution3 - Wordle-style match function (two-pass) that returns a response
                 string using green/yellow/gray coloring; O(L) per call where
                 L is the word length.
"""

from collections import defaultdict
from typing import List


# ---------------------------------------------------------------------------
# Approach 1: Using score
# ---------------------------------------------------------------------------
class Solution:
    def match(self, s1: str, s2: str) -> int:
        return sum(1 for i in range(6) if s1[i] == s2[i])

    def score(self, s: str, words: List[str]) -> int:
        res = 0
        for w in words:
            if s == w:
                continue
            res += self.match(s, w)
        return res

    def findSecretWord(self, words: List[str], master) -> None:
        possible_words = list(words)
        while True:
            candidate = possible_words[0]
            mx_score = self.score(candidate, possible_words)
            for i in range(1, len(possible_words)):
                s = self.score(possible_words[i], possible_words)
                if s > mx_score:
                    candidate = possible_words[i]
                    mx_score = s

            matches = master.guess(candidate)
            if matches == 6:
                break

            filtered = []
            for w in possible_words:
                if w == candidate:
                    continue
                if self.match(w, candidate) != matches:
                    continue
                filtered.append(w)

            possible_words = filtered


# ---------------------------------------------------------------------------
# Approach 2: Using weight and sort
# ---------------------------------------------------------------------------
# We eliminate more words by choosing words that are more similar to the rest
# of the wordlist. Sort by "similarity to the corpus" where each letter at each
# position contributes a weight equal to its per-position frequency.
class Solution2:
    def match(self, s1: str, s2: str) -> int:
        return sum(1 for i in range(6) if s1[i] == s2[i])

    def findSecretWord(self, words: List[str], master) -> None:
        possible_words = list(words)

        # weights[j][c] = number of times letter c appears at position j
        weights = [[0] * 26 for _ in range(6)]
        for w in words:
            for j, ch in enumerate(w):
                weights[j][ord(ch) - ord('a')] += 1

        def weight_of(word: str) -> int:
            return sum(weights[i][ord(word[i]) - ord('a')] for i in range(len(word)))

        # Descending sort by similarity to the corpus.
        possible_words.sort(key=weight_of, reverse=True)

        while True:
            candidate = possible_words[0]
            matches = master.guess(candidate)
            if matches == 6:
                break

            filtered = []
            for w in possible_words:
                if w == candidate:
                    continue
                if self.match(w, candidate) != matches:
                    continue
                filtered.append(w)

            possible_words = filtered


# ---------------------------------------------------------------------------
# Approach 3: Wordle-style two-pass match (from a wordle solver)
# ---------------------------------------------------------------------------
# First pass: mark exact position matches and count unmatched real characters.
# Second pass: mark wrong-position matches by decrementing the counter; anything
# left is a "miss".
class Solution3:
    # Response colors: [green, yellow, gray] equivalent
    response_colors = ['G', 'Y', 'X']
    word_length = 6

    def match(self, real: str, attempt: str) -> str:
        ret = ['0'] * self.word_length

        # To count unmatched occurrences.
        cnt = defaultdict(int)

        # First pass: exact character matches; count unmatched real characters.
        for i in range(self.word_length):
            if real[i] == attempt[i]:
                ret[i] = self.response_colors[0]
            else:
                cnt[real[i]] += 1

        # Second pass: mark characters at wrong positions.
        for i in range(self.word_length):
            if ret[i] != '0':
                continue
            if cnt[attempt[i]]:
                ret[i] = self.response_colors[1]
                cnt[attempt[i]] -= 1
            else:
                ret[i] = self.response_colors[2]

        return ''.join(ret)
