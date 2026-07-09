#include <vector>
#include <iostream>
#include <cassert>
#include <set>
#include <unordered_map>
#include <numeric>

using namespace std;

// ratios["chicken breast"] = 4;
// ratios["shrimp"] = 4;
// ratios["beef"] = 2;

// output1["chicken breast"] = 1;
// output1["shrimp"] = 48;
// output1["beef"] = 6;

// total = 55;

double calculateDeviation(unordered_map<string, int>& quantities,
                        unordered_map<string, int>& ratios) {
    double total = 0;
    for (auto i : quantities) total += i.second;

    double deviation = 0.0;
    for (auto i : quantities) {
        double actualRatio = total > 0 ? (double)i.second / total : 0;
        deviation += abs(actualRatio - (double)ratios[i.first] / 10);
    }

    return deviation;
}

void helper(vector<double>& macros, double target,
    vector<int>& curr,
    vector<vector<int>>& res,
    int idx) {

    if (target <= 10) {
        res.push_back(curr);
        return;
    }

    int n = macros.size();
    if (idx >= n) {
        return;
    }

    int multiplier = 1;
    while (multiplier * macros[idx] < target) {
        curr[idx] = multiplier;
        helper(macros, target - multiplier * macros[idx], curr, res, idx + 1);
        curr[idx] = 1;
        multiplier++;
    }
}

// as long as the we are within 10g of target, we count it as a result.
unordered_map<string, int> macroFiller(unordered_map<string, double>& ingredients, 
                                        unordered_map<string, int>& ratios,
                                                double target) {
    int n = ingredients.size();
    unordered_map<int, string> idx_macro;
    vector<double> macros;
    int idx = 0;
    for (auto i : ingredients) {
        idx_macro[idx++] = i.first;
        macros.push_back(i.second);
    }

    vector<int> curr(n, 0);
    vector<vector<int>> res;
    helper(macros, target, curr, res, 0);

    vector<unordered_map<string, int>> outputs;
    for (vector<int> i : res) {
        unordered_map<string, int> m;
        for (int j = 0; j < i.size(); j++) {
            m[idx_macro[j]] = i[j];
        }
        outputs.push_back(m);
    }

    // for (unordered_map<string, int> i : outputs) {
    //     for (auto j : i) {
    //         cout << j.first << ": " << j.second << endl;
    //     }
    //     cout << endl;
    // }

    double minDeviation = std::numeric_limits<double>::max();
    unordered_map<string, int> resMap;
    for (unordered_map<string, int> i : outputs) {
        double d = calculateDeviation(i, ratios);
        // cout << "min deviation: " << minDeviation << endl;
        if (d <= minDeviation) {
            minDeviation = d;
            resMap = i;
            // for (auto j : i) {
            //     cout << j.first << ": " << j.second << endl;
            // }
            // cout << endl;
        }
    }

    return resMap;
}

int main() {
    unordered_map<string, double> ingredients;
    ingredients["chicken breast"] = 2.33; // 10g
    ingredients["shrimp"] = 2.4;
    ingredients["beef"] = 3.07;

    unordered_map<string, int> ratios;
    ratios["chicken breast"] = 4;
    ratios["shrimp"] = 4;
    ratios["beef"] = 2;
    // ingredients["Quinoa"] = 6.4;
    // ingredients["Noodle"] = 7;
    unordered_map<string, int> res = macroFiller(ingredients, ratios, 140);
    // cout << outputs.empty() << endl;

    // unordered_map<string, int> output1;
    // output1["chicken breast"] = 1;
    // output1["shrimp"]= 48;
    // output1["beef"]= 6;

    // double d = calculateDeviation(output1, ratios);
    // cout << "d: " << d << endl;

    for (auto j : res) {
        cout << j.first << ": " << j.second << endl;
    }
    cout << endl;

    return 0;
}