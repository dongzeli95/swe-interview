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

/*
Part 3:
The chunks look the same as before, but now rather than a single password the input
contains a series of passwords, one follow the other. You will know one password has ended
and the next begun when you see an index repeated. Read only enough of the steram to
find the first password and print it out.
*/

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_set>
#include <deque>

using namespace std;

// class Entity {
// public:

//     Entity(int x, int y, vector<string>& board) : x(x), y(y), board(board) {}
//     // Part 2
//     Entity(int x, int y, int idx, vector<string>& board) : x(x), y(y), idx(idx), board(board) {}

//     char get() {
//         int m = board.size();
//         int n = board[0].size();
//         int tx = x;
//         int ty = m-1-y;

//         // check boundary
//         if (tx < 0 || ty < 0 || tx >= n || ty >= m) {
//             throw runtime_error("out of boundary");
//         }

//         return board[ty][tx];
//     }

//     void debug() {
//         cout << "x: " << x << " y: " << y << " idx: " << idx << endl;
//         for (int i = 0; i < board.size(); i++) {
//             cout << board[i] << endl;
//         }
//     }

//     int x = 0;
//     int y = 0;
//     vector<string> board;

//     // Part 2
//     int idx;
// };

class Entity {
public:
    int x;
    int y;
    int idx;

    Entity(int x, int y, int idx) : x(x), y(y), idx(idx) {}

    void add(string str) {
        if (x >= str.size()) {
            throw runtime_error("x out of bounds");
        }

        dq.push_back(str[x]);
        if (dq.size() > y + 1) {
            dq.pop_front();
        }
    }

    char get() {
        if (dq.size() != y + 1) {
            throw runtime_error("y out of bounds");
        }

        return dq.front();
    }

    deque<char> dq;
};

class Parser {
public:
    Parser(string filename) : filename(filename) {}

    Entity parse() {
        ifstream file(filename);
        if (!file.is_open()) {
            throw runtime_error("cannot open file");
        }

        vector<string> res;
        string line;
        getline(file, line);

        // Parse x, y
        char delim;
        int x, y;
        istringstream iss(line);
        iss >> delim >> x >> delim >> y >> delim;

        Entity e = Entity(x, y, -1);

        while (getline(file, line)) {
            // res.push_back(line);
            e.add(line);
        }

        file.close();
        // return 
        return e;
    }

    // Part 2
    Entity parseUtil(ifstream& file) {
        vector<string> res;
        string line;

        // Parse index
        getline(file, line);
        int idx;
        istringstream iss_idx(line);
        iss_idx >> idx;

        // Part 3
        if (seen.count(idx)) {
            vector<string> res;
            // return Entity(-1, -1, -1, res);
            return Entity(-1, -1, -1);
        }
        seen.insert(idx);

        // Parse x, y
        getline(file, line);
        char delim;
        int x, y;
        istringstream iss(line);
        iss >> delim >> x >> delim >> y >> delim;

        Entity e = Entity(x, y, idx);

        // Parse board portion, if digit means it's next chunk of entity.
        while (!isdigit(file.peek()) && getline(file, line) && !line.empty()) {
            // res.push_back(line);
            e.add(line);
        }

        // return Entity(x, y, idx, res);
        return e;
    }

    vector<Entity> parseList() {
        ifstream file(filename);
        if (!file.is_open()) {
            throw runtime_error("cannot open file");
        }

        vector<Entity> res;
        while (file.peek() != EOF && file.peek() != '\n') {
            Entity e = parseUtil(file);
            if (e.x == -1) break;
            res.push_back(e);
        }

        return res;
    }

    string filename;

    // Part 3
    unordered_set<int> seen;
};

string getPW() {
    Parser parser = Parser("company-tags/instacart/part2_test1.txt");
    vector<Entity> entityList = parser.parseList();

    string res = string(entityList.size(), ' ');
    for (Entity e: entityList) {
        char c = e.get();
        res[e.idx] = c;
    }

    return res;
}

char part1() {
    Parser parser = Parser("company-tags/instacart/test1.txt");
    Entity e = parser.parse();
    return e.get();
}

string getPW_Part3() {
    Parser parser = Parser("company-tags/instacart/part3_test1.txt");
    vector<Entity> entityList = parser.parseList();

    string res = string(entityList.size(), ' ');
    for (Entity e : entityList) {
        // e.debug();
        char c = e.get();
        res[e.idx] = c;
    }

    return res;
}

int main() {
    cout << part1() << endl;
    cout << getPW() << endl;
    // cout << getPW_Part3() << endl;
    return 0;
}```
