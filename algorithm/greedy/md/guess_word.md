```cpp
// https://leetcode.com/problems/guess-the-word/description/

/*
You are given an array of unique strings words where words[i] is six letters long. One word of words was chosen as a secret word.

You are also given the helper object Master. You may call Master.guess(word) where word is a six-letter-long string, and it must be from words. Master.guess(word) returns:

-1 if word is not from words, or
an integer representing the number of exact matches (value and position) of your guess to the secret word.
There is a parameter allowedGuesses for each test case where allowedGuesses is the maximum number of times you can call Master.guess(word).

For each test case, you should call Master.guess with the secret word without exceeding the maximum number of allowed guesses. You will get:

"Either you took too many guesses, or you did not find the secret word." if you called Master.guess more than allowedGuesses times or if you did not call Master.guess with the secret word, or
"You guessed the secret word correctly." if you called Master.guess with the secret word with the number of calls to Master.guess less than or equal to allowedGuesses.
The test cases are generated such that you can guess the secret word with a reasonable strategy (other than using the bruteforce method).

Ex1:
Input: secret = "acckzz", words = ["acckzz","ccbazz","eiowzz","abcczz"], allowedGuesses = 10
Output: You guessed the secret word correctly.
Explanation:
master.guess("aaaaaa") returns -1, because "aaaaaa" is not in wordlist.
master.guess("acckzz") returns 6, because "acckzz" is secret and has all 6 matches.
master.guess("ccbazz") returns 3, because "ccbazz" has 3 matches.
master.guess("eiowzz") returns 2, because "eiowzz" has 2 matches.
master.guess("abcczz") returns 4, because "abcczz" has 4 matches.
We made 5 calls to master.guess, and one of them was the secret, so we pass the test case.

Ex2:
Input: secret = "hamada", words = ["hamada","khaled"], allowedGuesses = 10
Output: You guessed the secret word correctly.
Explanation: Since there are two words, you can guess both.

*/

#include <vector>
#include <string>

using namespace std;

// Using score
int match(string s1, string s2) {
    int res = 0;
    for (int i = 0; i < 6; i++) {
        if (s1[i] == s2[i]) res++;
    }
    return res;
}
int score(string& s, vector<string>& words) {
    int res = 0;
    for (int i = 0; i < words.size(); i++) {
        if (s == words[i]) continue;
        res += match(s, words[i]);
    }
    return res;
}
void findSecretWord(vector<string>& words, Master& master) {
    vector<string> possibleWords = words;
    while (true) {
        string candidate = possibleWords[0];
        int mxScore = score(candidate, possibleWords);
        for (int i = 1; i < possibleWords.size(); i++) {
            int s = score(possibleWords[i], possibleWords);
            if (s > mxScore) {
                candidate = possibleWords[i];
                mxScore = s;
            }
        }
        int matches = master.guess(candidate);
        if (matches == 6) {
            break;
        }

        vector<string> filter;
        for (int i = 0; i < possibleWords.size(); i++) {
            if (candidate == possibleWords[i]) continue;
            if (match(possibleWords[i], candidate) != matches) continue;
            filter.push_back(possibleWords[i]);
        }

        possibleWords = filter;
    }
}

// Using weight and sort
// 2. We eliminate more words by choosing words that are more similar to the rest of the wordlist

// If guess("xyz") > 0 then we can eliminate words that are dissimilar to "xyz" (see above).
// But we can elminate words that are similar to "xyz" if guess("xyz") is == 0. 
// For large wordlists, the overwhelming fraction of words in wordlist will have a score of 0. 
// (Fun problem : compute this fraction for a randomly generated wordlist of size N.)

// Given guess() returns 0 most of the time for large wordlists, we can, 
// on average eliminate more words per guess by choosing words that are more similar to the rest ofthe corpus.

// We can do this by sorting the words in order of "similarity to the rest of the corpus".
// You can do this pretty much any reasonable way and pass the LeetCode testcases.
// But just as an example, here's a solution in which we assign each letter at each position a "weight" 
// equal to the number of times that letter occurs at that position across entire wordlist. 
// Each word's similarity to the rest of the corpus is then the sum of these weights for its letters.
int match(string s1, string s2) {
    int res = 0;
    for (int i = 0; i < 6; i++) {
        if (s1[i] == s2[i]) res++;
    }
    return res;
}

void findSecretWord(vector<string>& words, Master& master) {
    vector<string> possibleWords = words;
    vector<vector<int>> weights(6, vector<int>(26, 0));
    for (int i = 0; i < words.size(); i++) {
        for (int j = 0; j < words[i].size(); j++) {
            int idx = words[i][j] - 'a';
            weights[j][idx]++;
        }
    }

    auto compare = [&weights](const std::string& a, const std::string& b) {
        int weightA = 0, weightB = 0;
        for (int i = 0; i < a.size(); ++i) {
            weightA += weights[i][a[i] - 'a'];
        }
        for (int i = 0; i < b.size(); ++i) {
            weightB += weights[i][b[i] - 'a'];
        }

        return weightA > weightB;
        };

    sort(possibleWords.begin(), possibleWords.end(), compare);

    while (true) {
        string candidate = possibleWords[0];
        int matches = master.guess(candidate);
        if (matches == 6) {
            break;
        }

        vector<string> filter;
        for (int i = 0; i < possibleWords.size(); i++) {
            if (candidate == possibleWords[i]) continue;
            if (match(possibleWords[i], candidate) != matches) continue;
            filter.push_back(possibleWords[i]);
        }

        possibleWords = filter;
    }
}


// From my wordle solver : One solution is to do two passes over the words.
// In the first pass, mark the matched characters and increment count for unmatched characters in answer.
// Then, in the second pass, mark the characters in input if their count is nonzero, and decrement the count.

// Find the response on playing <attempt> to the word <real>
std::string GameBase::match(const std::string & real, const std::string & attempt) {
    std::string ret(word_length, '0');

    // To count unmatched occurreces
    std::unordered_map<char, int> cnt;

    // First look for exact character matches
    // And increment counter of unmatched characters
    for (int i = 0; i < word_length; ++i) {
        if (real[i] == attempt[i])
            ret[i] = responsecolors[0];
        else
            ++cnt[real[i]];
    }

    // Now mark all the characters at wrong positions
    for (int i = 0; i < word_length; ++i) {
        if (ret[i] != '0') continue;

        if (cnt[attempt[i]])
            ret[i] = responsecolors[1], --cnt[attempt[i]];
        else
            ret[i] = responsecolors[2];
    }

    return ret;
}```
