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
#include <deque>

using namespace std;

// 1: B -> P -> A -> I
// 2: [MH]

class Entity {
public:
    int x;
    int y;

    Entity(int x, int y) : x(x), y(y) {}

    void add(string str) {
        if (x >= str.size()) {
            throw runtime_error("x out of bounds");
        }

        dq.push_back(str[x]);
        if (dq.size() > y+1) {
            dq.pop_front();
        }
    }

    char get() {
        if (dq.size() != y+1) {
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
            cout << "Fail to open" << endl;
            return Entity(-1, -1);
        }

        vector<string> res;
        string line;
        getline(file, line);

        // Parse x, y
        char delim;
        int x, y;
        istringstream iss(line);
        iss >> delim >> x >> delim >> y >> delim;

        Entity e = Entity(x, y);
        while (getline(file, line)) {
            e.add(line);
        }

        file.close();
        return e;
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
    // Print current directory.
    // char cwd[256];
    // if (getcwd(cwd, sizeof(cwd)) != NULL) {
    //     std::cout << "Current working dir: " << cwd << std::endl;
    // }
    // else {
    //     perror("getcwd() error");
    // }

    Parser parser = Parser("company-tags/instacart/test1.txt");
    Entity entity = parser.parse();
    cout << entity.get() << endl;
    // entity.debug();

    return 0;
}```
