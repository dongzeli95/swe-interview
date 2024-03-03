```cpp

// 经典dashmart题

// [' ', 'X', 'D']
// [' ', ' ', 'D']
// [' ', 'X', ' ']
// 给一个char[][] = { {' ', 'X', 'D'},{' ', ' ', 'D'},{' ', 'X', ' '}, }  和location array = { {0,0},{1,0} }
// X不能通过，D代表dashmart位置，返回location array中每个location与离它最近的dashmart的距离
// output = { 3,2 }

// 然后还问了follow up，如果char[][]里有'C'代表customer，
// customer会选择离他最近的dashmart，求有最多的customers的‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌dashmart
// 不用写，描述一下solution 分析一下time complexity就行了

// Intuition: start with D, dfs or bfs

#include <vector>
#include <queue>
#include <iostream>

using namespace std;

struct Loc {
public:
  int x;
  int y;
  int dist;
  pair<int, int> origin;
  Loc(int x, int y, int dist):x(x), y(y), dist(dist), origin({-1, -1}) {}
  Loc(int x, int y, int dist, pair<int, int> origin) :x(x), y(y), dist(dist), origin(origin) {}
};

// Time: O(m*n), Space: O(m*n)
vector<int> getDistances(vector<vector<char>>& grid, vector<pair<int, int>>& dashes) {
    int m = grid.size();
    int n = grid[0].size();

    vector<int> neighbors {0, -1, 0, 1, 0};
    vector<vector<int>> dist(m, vector<int>(n, -1));

    queue<Loc> q;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 'D') {
                dist[i][j] = 0;
                q.push(Loc(i, j, 0));
            }
        }
    }

    while (!q.empty()) {
        Loc curr = q.front();
        q.pop();

        int x = curr.x;
        int y = curr.y;
        int dis = curr.dist;

        for (int i = 0; i < 4; i++) {
            int tempX = x + neighbors[i];
            int tempY = y + neighbors[i+1];

            if (tempX < 0 || tempY < 0 || tempX >= m || tempY >= n) continue;
            if (grid[tempX][tempY] == 'X') continue;
            if (dist[tempX][tempY] != -1 && dis + 1 > dist[tempX][tempY]) continue;

            dist[tempX][tempY] = dis+1;
            q.push(Loc(tempX, tempY, dis+1));
        }
    }

    vector<int> res;
    for (int i = 0; i < dashes.size(); i++) {
        int x = dashes[i].first;
        int y = dashes[i].second;
        res.push_back(dist[x][y]);
    }

    return res;
}

pair<int, int> parse(string k) {
    size_t pos = k.find('#');
    string x_str = k.substr(0, pos);
    string y_str = k.substr(pos+1);

    return {stoi(x_str), stoi(y_str)};
}

// Time: O(m*n), Space: O(m*n)
pair<int, int> getDashWithMostCustomers(vector<vector<char>>& grid) {
    int m = grid.size();
    int n = grid[0].size();

    vector<int> neighbors{ 0, -1, 0, 1, 0 };
    vector<vector<int>> dist(m, vector<int>(n, -1));

    vector<vector<pair<int, int>>> originMap(m, vector<pair<int, int>>(n, { -1, -1 }));

    queue<Loc> q;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 'D') {
                dist[i][j] = 0;
                q.push(Loc(i, j, 0, { i, j }));
            }
        }
    }

    while (!q.empty()) {
        Loc curr = q.front();
        q.pop();

        int x = curr.x;
        int y = curr.y;
        int dis = curr.dist;
        pair<int, int> ori = curr.origin;

        for (int i = 0; i < 4; i++) {
            int tempX = x + neighbors[i];
            int tempY = y + neighbors[i + 1];

            if (tempX < 0 || tempY < 0 || tempX >= m || tempY >= n) continue;
            if (grid[tempX][tempY] == 'X') continue;
            if (dist[tempX][tempY] != -1 && dis + 1 > dist[tempX][tempY]) continue;
            originMap[tempX][tempY] = ori;
            dist[tempX][tempY] = dis + 1;
            q.push(Loc(tempX, tempY, dis + 1, ori));
        }
    }

    unordered_map<string, int> customers;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 'C') {
                pair<int, int> d = originMap[i][j];
                string k = to_string(d.first) + "#" + to_string(d.second);
                customers[k]++;
            }
        }
    }

    int mxCustomers = 0;
    pair<int, int> candidate = {-1, -1};
    for (auto i : customers) {
        if (i.second > mxCustomers) {
            mxCustomers = i.second;
            candidate = parse(i.first);
        }
    }

    return candidate;
}

void debug(vector<int>& res) {
    for (int i = 0; i < res.size(); i++) {
        cout << res[i] << " ";
    }
    cout << endl;
}

int main() {
    // vector<vector<char>> grid{{' ', 'X', 'D'},
    //                          {' ', ' ', 'D'},
    //                          {' ', 'X', ' '}};
    // vector<pair<int, int>> dashes {{0, 0}, {1, 0}};
    // vector<int> res = getDistances(grid, dashes);
    // debug(res);

    // vector<vector<char>> grid{ 
    //                     {' ', 'X', 'D'},
    //                     {' ', ' ', 'D'},
    //                     {'D', 'X', ' '} };
    // vector<pair<int, int>> dashes{ {0, 0}, {1, 0} };
    // vector<int> res = getDistances(grid, dashes);
    // debug(res);


    // vector<vector<char>> grid{
    //                     {'D', 'D'},
    //                     {'D', 'D'} };
    // vector<pair<int, int>> dashes{ {0, 0}, {0, 1} };
    // vector<int> res = getDistances(grid, dashes);
    // debug(res);

    vector<vector<char>> grid{ 
                    {' ', 'X', 'D'},
                    {'C', ' ', 'D'},
                    {' ', 'C', ' '} };
    pair<int, int> res = getDashWithMostCustomers(grid);
    cout << "x: " << res.first << " y: " << res.second << endl;

    return 0;
}```
