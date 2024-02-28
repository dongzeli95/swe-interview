```cpp
/*
Part 2:
You will notice each chunk looks similar to the previous challenge with one addition
the first line is the (0-based) index of the password character.

In our example
- First chunk: password character index 1, character at [5, 6] is I.
- Second chunk: password character index 0, character at [0, 1] is H.

Once you have processed all of the chunks you have the entire password and
should print it to STDOUT, in our example the password is HI.
*/

#include <iostream>
#include <vector>
#include <string>
#include <sstream>

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
    vector<pair<int, char>> chunkResults; // To store results of each chunk

    try {
        while (cin.peek() != EOF && cin.peek() != '\n') {
            chunkResults.push_back(processChunk());
        }

        // Initialize password vector with the correct size
        password.resize(chunkResults.size());

        // Assign characters to their positions in the password
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

int main() {
    string password = constructPassword();
    cout << password << endl; //BHI
    return 0;
}```
