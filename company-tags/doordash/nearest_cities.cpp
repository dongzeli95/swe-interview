// A number of cities are arranged on a graph that has been divided up like an ordinary Cartesian plane.
// Each city is located at an integral(x, y) coordinate intersection.

// City names and locations are given in the form of three arrays : c, x, and y, which are aligned by the index to provide the city name(c[i]), and its coordinates, (x[i], y[i]).
// Determine the name of the nearest city that shares either an x or a y coordinate with the queried city.

// If no other cities share an x or y coordinate, return 'NONE'.

// If two cities have the same distance to the queried city, q[i], consider the one with an alphabetically shorter name(i.e. 'ab' < 'aba' < 'abb') as the closest choice.
// The distance is the Manhattan distance, the absolute difference in x plus the absolute difference in y.

// The time complexity for my solution is O(NlogK) for processing input + O(QlogK) for returning the result for all the given queries,
// where N is the number of cities, K is the max number of cities with same x or y coordinate and Q is the number of queries.

// 题目就是给两个城市的list，一个是所有城市c[c1, c2, c3, c4]，x[4, 7, 9], y[1, 2, 3]，一个是需要query求距离的城市q[c3, c4]，求q里面每个城市到x或者y坐标重合（指 x相等或者y相等）的城市到最短距离
// 解法就是用map记录{ x1: [c1, c2, c3] }  c1, c2, c3都有相同x1，sorted by y value in the list, 在query 一个城市q(qx, qy)的时候，求qx‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌在map对应的list里面离qy最近的距离，用二分法求

// 给一组城市name 坐标x 坐标y 输入一系列query name 返回相同x或者相同y的最近city name
// every city name is guaranteed to be unique and no 2 cities will have same coordinates

// 如果没有则返回\'NONE\'
// 注意如果有相同的最近的城市，返回alphabet更小的城市
// 我的做法 复杂度nlog(n)

#include <iostream>
#include <vector>
#include <map>
#include <limits>
#include <string>
#include <cmath>

using namespace std;

struct CityDist {
    double dist;
    string city;

    CityDist(double dist, string city) : dist(dist), city(city) {}
};
class NearestCity {
public:
    // Time: O(nlogn), Space: O(n)
    vector<string> getNearestCities(vector<string>& names, vector<int>& x, vector<int>& y, vector<string>& query) {
        unordered_map<int, map<int, string>> sameXCityMap;
        unordered_map<int, map<int, string>> sameYCityMap;
        unordered_map<string, pair<int, int>> nameToXYMap;

        for (size_t i = 0; i < names.size(); ++i) {
            sameXCityMap[x[i]][y[i]] = names[i];
            sameYCityMap[y[i]][x[i]] = names[i];
            nameToXYMap[names[i]] = { x[i], y[i] };
        }

        vector<string> res;
        for (const string& queriedCity : query) {
            CityDist minCityDist(std::numeric_limits<double>::max(), "NONE");
            auto queriedLocation = nameToXYMap[queriedCity];
            int queriedX = queriedLocation.first, queriedY = queriedLocation.second;

            updateCloserCity(sameXCityMap[queriedX], queriedY, minCityDist);
            updateCloserCity(sameYCityMap[queriedY], queriedX, minCityDist);

            res.push_back(minCityDist.city);
        }
        return res;
    }

    void updateCloserCity(const map<int, string>& cities, int queriedCoord, CityDist& minCityDist) {
        auto lower = cities.lower_bound(queriedCoord);
        auto upper = cities.upper_bound(queriedCoord);

        if (lower != cities.begin()) {
            --lower;
            double dist = abs(lower->first - queriedCoord);
            if (dist < minCityDist.dist || (dist == minCityDist.dist && lower->second < minCityDist.city)) {
                minCityDist.dist = dist;
                minCityDist.city = lower->second;
            }
        }

        if (upper != cities.end()) {
            double dist = abs(upper->first - queriedCoord);
            if (dist < minCityDist.dist || (dist == minCityDist.dist && upper->second < minCityDist.city)) {
                minCityDist.dist = dist;
                minCityDist.city = upper->second;
            }
        }
    }
};

int main() {
    // city1: (1, 1)
    // city2: (1, 5)
    // city3: (2, 3)
    // city4: (3, 1)
    NearestCity solver1;
    vector<string> names1 = { "city1", "city2", "city3", "city4" };
    vector<int> x1 = { 1, 1, 2, 3 };
    vector<int> y1 = { 1, 5, 3, 1 };
    vector<string> query1 = { "city1", "city2", "city3", "city4" };

    vector<string> nearestCities1 = solver1.getNearestCities(names1, x1, y1, query1);

    cout << "Test Case 1:" << endl;
    for (const auto& city : nearestCities1) {
        cout << city << endl;
    }
    cout << endl;

    // alpha: (0, 0): beta
    // beta: (0, 2): alpha
    // gamma: (2, 2): beta
    // delta: (2, 0): alpha
    NearestCity solver2;
    vector<string> names2 = { "alpha", "beta", "gamma", "delta" };
    vector<int> x2 = { 0, 0, 2, 2 };
    vector<int> y2 = { 0, 2, 2, 0 };
    vector<string> query2 = { "alpha", "beta", "gamma", "delta" };

    vector<string> nearestCities2 = solver2.getNearestCities(names2, x2, y2, query2);

    cout << "Test Case 2:" << endl;
    for (const auto& city : nearestCities2) {
        cout << city << endl;
    }
    cout << endl;

    // north: (5, 10): center
    // south: (5, 5) : center
    // east: (10, 5) : south
    // west: (0, 5) : south
    // center: (5, 6) : south
    NearestCity solver3;
    vector<string> names3 = { "north", "south", "east", "west", "center" };
    vector<int> x3 = { 5, 5, 10, 0, 5 };
    vector<int> y3 = { 10, 5, 5, 5, 6 };
    vector<string> query3 = { "north", "south", "east", "west", "center" };

    vector<string> nearestCities3 = solver3.getNearestCities(names3, x3, y3, query3);

    cout << "Test Case 3:" << endl;
    for (const auto& city : nearestCities3) {
        cout << city << endl;
    }
    cout << endl;

    return 0;
}

