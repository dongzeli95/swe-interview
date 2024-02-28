/*
Part 3:
The chunks look the same as before, but now rather than a single password the input
contains a series of passwords, one follow the other. You will know one password has ended
and the next begun when you see an index repeated. Read only enough of the steram to 
find the first password and print it out.
*/

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_set>

using namespace std;

// Function to find the character
char findCharacterInMatrix(const vector<string>& matrix, int x, int y) {
    // Adjust the coordinates
    int adjusted_x = x;
    int adjusted_y = matrix.size() - 1 - y;

    // Check for valid coordinates and return the character
    if (adjusted_y >= 0 && adjusted_y < matrix.size() &&
        adjusted_x >= 0 && adjusted_x < matrix[adjusted_y].length()) {
        return matrix[adjusted_y][adjusted_x];
    }
    else {
        throw out_of_range("Invalid coordinates");
    }
}

// Function to process a single chunk of input
pair<int, char> processChunk() {
    string line;

    // Extract password character index
    getline(cin, line);
    int passwordIndex;
    stringstream ss(line);
    ss >> passwordIndex;

    // Extract coordinates
    getline(cin, line);
    istringstream iss(line);
    int x, y;
    char delim; // To consume the comma and space in "[x, y]"
    iss >> delim >> x >> delim >> y >> delim; // Expecting format "[x, y]"

    // Read the matrix
    vector<string> matrix;
    while (getline(cin, line) && !line.empty()) {
        matrix.push_back(line);
    }

    char result = findCharacterInMatrix(matrix, x, y);
    return { passwordIndex, result };
}

string constructPassword() {
    vector<char> password; // To store password characters
    unordered_set<int> seen; // To track seen indices
    int maxIndex = -1; // To track the highest index encountered
    vector<pair<int, char>> chunkResults;

    try {
        while (cin.peek() != EOF && cin.peek() != '\n') {
            auto [index, character] = processChunk();
            chunkResults.push_back({index, character});
            // Check if the index has already been seen
            if (seen.count(index)) {
                // fix to put back
                // cin.putback('\n');
                // for (auto it = line.rbegin(); it != line.rend(); ++it) {
                //     cin.putback(*it);
                // }
                break; // An index is repeated, indicating a new password has started
            }
            seen.insert(index);
            maxIndex = max(maxIndex, index);
        }

        password.resize(maxIndex + 1);
        for (const auto& [index, character] : chunkResults) {
            password[index] = character;
        }
    }
    catch (const out_of_range& e) {
        cout << e.what() << endl;
    }

    // Convert password vector to string and return
    return string(password.begin(), password.end());
}

vector<string> parseAllPasswords() {
    vector<string> passwords;
    while (cin.peek() != EOF) {
        string password = constructPassword();
        if (!password.empty()) {
            passwords.push_back(password);
        }
    }
    return passwords;
}

int main() {
    vector<string> passwords = parseAllPasswords();
    for (const auto& password : passwords) {
        cout << password << endl;
    }
    return 0;
}