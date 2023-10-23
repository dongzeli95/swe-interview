// https://www.techiedelight.com/group-anagrams-together-given-list-words/

/*
Given a list of words, efficiently group all anagrams.

The two strings, X and Y, are anagrams if by rearranging X's letters, we can get Y using all the original letters of X exactly once. 
For example, all these pairs are anagrams as lhs can be rearranged to rhs and vice-versa.

actors = costar
altered = related
auctioned = education
aspired = despair
mastering = streaming
recurd = secured

Ex1:
Input:

[CARS, REPAID, DUES, NOSE, SIGNED, LANE, PAIRED, ARCS, GRAB, USED, ONES, BRAG, SUED, LEAN, SCAR, DESIGN]

Output:
GRAB BRAG
CARS ARCS SCAR
REPAID PAIRED
LANE LEAN
SIGNED DESIGN
DUES USED SUED
NOSE ONES

*/

#include <vector>
#include <string>
#include <unordered_map>
#include <cassert>
#include <iostream>

using namespace std;

string encodeStr(string str) {
    unordered_map<char, int> m;
    int n = str.size();
    for (char c : str) {
        m[c]++;
    }

    string res;
    for (int i = 0; i < 26; i++) {
        char c = i + 'a';
        if (!m.count(c)) continue;
        res.push_back(c);
        res.push_back('0'+m[c]);
    }

    for (int i = 0; i < 26; i++) {
        char c = i + 'A';
        if (!m.count(c)) continue;
        res.push_back(c);
        res.push_back('0' + m[c]);
    }

    return res;
}

vector<vector<string>> groupAnagrams(vector<string> strs) {
    if (strs.empty()) {
        return {};
    }

    unordered_map<string, vector<string>> anagramMap;
    int n = strs.size();
    for (int i = 0; i < n; i++) {
        string hash = encodeStr(strs[i]);
        anagramMap[hash].push_back(strs[i]);
    }

    vector<vector<string>> res;
    for (auto i : anagramMap) {
        res.push_back(i.second);
    }

    return res;
}

int main() {
    vector<string> input = { "CARS", "REPAID", "DUES", "NOSE", "SIGNED", "LANE", "PAIRED", "ARCS", "GRAB", "USED", "ONES", "BRAG", "SUED", "LEAN", "SCAR", "DESIGN" };
    vector<vector<string>> expectedOutput = {
        {"CARS", "ARCS", "SCAR"},
        {"REPAID", "PAIRED"},
        {"DUES", "USED", "SUED"},
        {"NOSE", "ONES"},
        {"SIGNED", "DESIGN"},
        {"LANE", "LEAN"},
        {"GRAB", "BRAG"}
    };

    vector<vector<string>> result = groupAnagrams(input);

    // Sort the result and expectedOutput vectors to compare them
    sort(result.begin(), result.end());
    sort(expectedOutput.begin(), expectedOutput.end());

    for (int i = 0; i < result.size(); i++) {
        for (int j = 0; j < result[i].size(); j++) {
            cout << result[i][j] << " ";
        }
        cout << endl;
    }

    assert(result == expectedOutput);

    cout << "Test passed!" << endl;

    return 0;
}