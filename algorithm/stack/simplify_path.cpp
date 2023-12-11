// https://leetcode.com/problems/simplify-path/

/*
Given a string path, which is an absolute path (starting with a slash '/') to a file or directory in a Unix-style file system, 
convert it to the simplified canonical path.

In a Unix-style file system, a period '.' refers to the current directory, 
a double period '..' refers to the directory up a level, and any multiple consecutive slashes (i.e. '//') are treated as a single slash '/'. For this problem, any other format of periods such as '...' are treated as file/directory names.

The canonical path should have the following format:

The path starts with a single slash '/'.
Any two directories are separated by a single slash '/'.
The path does not end with a trailing '/'.
The path only contains the directories on the path from the root directory to the target file or directory (i.e., no period '.' or double period '..')
Return the simplified canonical path.

Ex1:
Input: path = "/home/"
Output: "/home"
Explanation: Note that there is no trailing slash after the last directory name.

Ex2:
Input: path = "/../"
Output: "/"
Explanation: Going one level up from the root directory is a no-op, as the root level is the highest level you can go.

Ex3:
Input: path = "/home//foo/"
Output: "/home/foo"
Explanation: In the canonical path, multiple consecutive slashes are replaced by a single one.

*/

// 1. ./
// 2. ../
// 3. doesn't end with /
// 4. // make it a /
// 5. how about ///home/etc/

// [home]
// [".."]
// [home, "", "foo"]

#include <iostream>
#include <string>
#include <sstream>

using namespace std;

// Time: O(n), Space: O(n)
string simplifyPath(string path) {
    if (path.empty()) {
        return "";
    }

    string token;
    stringstream ss(path);
    vector<string> st;
    while (getline(ss, token, '/')) {
        if (token.empty() || token == ".") continue;
        if (token == "..") {
            if (!st.empty()) {
                st.pop_back();
            }
        } else {
            st.push_back(token);
        }
    }

    string res = "/";
    int n = st.size();
    for (int i = 0; i < n; i++) {
        res += st[i];
        if (i != n-1) {
            res.push_back('/');
        }
    }

    return res;
}

int main() {
    string res = simplifyPath("/home/");
    cout << res << endl;

    res = simplifyPath("/../");
    cout << res << endl;

    res = simplifyPath("/home//foo/");
    cout << res << endl;

    return 0;
}
