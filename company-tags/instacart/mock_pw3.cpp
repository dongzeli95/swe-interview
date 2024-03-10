/*
Part 3:
The chunks look the same as before, but now rather than a single password the input
contains a series of passwords, one follow the other. You will know one password has ended
and the next begun when you see an index repeated. Read only enough of the steram to
find the first password and print it out.
*/

#include <unistd.h>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_set>

using namespace std;

class EncryptChar {
public:
    EncryptChar(vector<string>& board) : board(board) {}

    char getChar(int x, int y) {
        int m = board.size();
        int n = board[0].size();
        int tx = x;
        int ty = m - 1 - y;

        if (tx < 0 || ty < 0 || tx >= n || ty >= m) {
            throw runtime_error("x, y out of bounds!");
        }

        return board[ty][tx];
    }

private:
    vector<string> board;
};

class Entity {
public:
    int x;
    int y;
    int idx;
    vector<string> board;

    Entity() : x(-1), y(-1), idx(-1), board({}) {}
    Entity(int x, int y, vector<string>& board) : x(x), y(y), idx(-1), board(board) {}
    Entity(int x, int y, int idx, vector<string>& board) : x(x), y(y), idx(idx), board(board) {}

    char getChar() {
        EncryptChar ec = EncryptChar(board);
        return ec.getChar(x, y);
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

vector<string> getPW() {
    Parser parser = Parser("company-tags/instacart/part3_test1.txt");
    vector<Entity> entityList = parser.parseList();
    vector<string> res;
    string curr = string(entityList.size(), ' ');
    int count = 0;
    for (Entity e : entityList) {
        char c = e.getChar();
        if (curr[e.idx] != ' ') {
            res.push_back(curr.substr(0, count));
            curr = string(entityList.size(), ' ');
            count = 0;
        }
        curr[e.idx] = c;
        count++;
    }

    string pw = curr.substr(0, count);
    if (!pw.empty()) {
        res.push_back(pw);
    }

    return res;
}

int main() {
    vector<string> res = getPW();
    for (int i = 0; i < res.size(); i++) {
        cout << res[i] << " ";
    }
    cout << endl;
    return 0;
}