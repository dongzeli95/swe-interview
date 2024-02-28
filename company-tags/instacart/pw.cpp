/*
Part 1:
For this challenge, you will need to parse data from STDIN to find a character in a matrix.
Below is an example of the input you will receive from STDIN:

[2, 4]
AFKPU
BGLQV
CHMRW
DINSX
EJOTY

The first line is the [X, Y] coordinates of the character in the matrix.
([0, 0] is the bottom left character)

The remaining lines contain a matrix of random characters, with a character located at the coordinates 
from line 1. so in the example above, we are looking for a character at the coordinates [2, 4]
Moving right 2 spaces, and up 4, we find the character K. so K is the character.

Please write a program that read from stdin and prints the answer to stdout

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

int main() {
    string line;
    getline(cin, line); // Read the first line

    // Extract coordinates from the line
    istringstream iss(line);
    int x, y;
    char delim; // To consume the comma and space in "[x, y]"
    iss >> delim >> x >> delim >> y >> delim; // Expecting format "[x, y]"

    std::vector<std::string> matrix;

    // Read the matrix
    while (cin >> line) {
        matrix.push_back(line);
    }

    try {
        // Call the function and print the result
        char result = findCharacterInMatrix(matrix, x, y);
        cout << result << endl;
    } catch (const out_of_range& e) {
        cout << e.what() << endl;
    }

    return 0;
}