```cpp
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

#include <unistd.h>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

class Entity {
public:
    int x;
    int y;
    int idx;
    vector<string> board;

    Entity() : x(-1), y(-1), idx(-1), board({}) {}
    Entity(int x, int y, vector<string>& board) : x(x), y(y), idx(-1), board(board) {}
    Entity(int x, int y, int idx, vector<string>& board) : x(x), y(y), idx(idx), board(board) {}

    char get() {
        int m = board.size();
        int n = board[0].size();
        int tx = x;
        int ty = m - 1 - y;

        if (tx < 0 || ty < 0 || tx >= n || ty >= m) {
            throw runtime_error("x, y out of bounds!");
        }

        return board[ty][tx];
    }

    void debug() {
        cout << "x: " << x << " y:" << y << endl;
        cout << "index: " << idx << endl;
        cout << "board: " << endl;
        for (int i = 0; i < board.size(); i++) {
            cout << board[i] << endl;
        }
    }
};

class Parser {
public:
    Parser(string filename) : filename(filename) {}

    Entity parse() {
        ifstream file(filename);
        if (!file.is_open()) {
            cout << "Fail to open" << endl;
            return Entity();
        }

        vector<string> res;
        string line;
        getline(file, line);

        // Parse x, y
        char delim;
        int x, y;
        istringstream iss(line);
        iss >> delim >> x >> delim >> y >> delim;

        while (getline(file, line)) {
            res.push_back(line);
        }

        file.close();
        return Entity(x, y, res);
    }

    Entity parseUtil(ifstream& file) {
        vector<string> res;
        string line;

        // Parse index
        getline(file, line);
        int idx;
        istringstream iss_idx(line);
        iss_idx >> idx;

        // Parse x, y
        getline(file, line);
        char delim;
        int x, y;
        istringstream iss(line);
        iss >> delim >> x >> delim >> y >> delim;

        while (getline(file, line) && !line.empty()) {
            res.push_back(line);
        }

        return Entity(x, y, idx, res);
    }

    vector<Entity> parseList() {
        ifstream file(filename);
        if (!file.is_open()) {
            return {};
        }

        vector<Entity> res;
        while (file.peek() != EOF && file.peek() != '\n') {
            res.push_back(parseUtil(file));
        }

        file.close();
        return res;
    }

private:
    string filename;
};

void debug(vector<string>& file) {
    cout << file.empty() << endl;
    for (int i = 0; i < file.size(); i++) {
        cout << file[i] << endl;
    }
}

int main() {
    Parser parser = Parser("company-tags/instacart/part2_test1.txt");
    vector<Entity> entityList = parser.parseList();
    // for (Entity e: entityList) {
    //     e.debug();
    // }

    string res = string(entityList.size(), ' ');
    for (Entity e: entityList) {
        char c = e.get();
        res[e.idx] = c;
    }

    cout << res << endl;

    return 0;
}```
