/*
You are given a list of boxes with 2 dimensions, width and height. Return the maximum number of boxes you can stack on each other. You can rotate the box so basically if you have a box with dimensions [3,2] you can turn it into [2,3]. You can only put the box on the top of the pile if the width is less than the width of the current box on the pile.

Ex:
input is [width,height]
[2,2],[3,2],[3,4],[4,3]: result=3, start with either of the boxes that have a 4, then take the [3,2] width 3, then take the [2,2] on top. Cannot use both the [3,4] and [4,3] regardless of rotation.
*/

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Box {
    int width, height, index;  // add an index to differentiate boxes of the same size
    Box(int w, int h, int idx) : width(w), height(h), index(idx) {}
};

int maxStackedBoxes(std::vector<Box>& boxes) {
    // Create a vector of all orientations
    std::vector<Box> all_orientations;
    for (size_t i = 0; i < boxes.size(); ++i) {
        all_orientations.push_back(Box(boxes[i].width, boxes[i].height, i));
        all_orientations.push_back(Box(boxes[i].height, boxes[i].width, i));
    }

    // Sort by width (considering that two boxes can be stacked if the width is less than the width of the current box on the pile)
    std::sort(all_orientations.begin(), all_orientations.end(), [](const Box& a, const Box& b) {
        return (a.width != b.width) ? (a.width < b.width) : (a.index < b.index);
        });

    // DP table
    std::vector<int> dp(all_orientations.size(), 1);

    int max_count = 0;
    for (size_t i = 0; i < all_orientations.size(); ++i) {
        for (size_t j = 0; j < i; ++j) {
            cout << "box i width: " << all_orientations[i].width << ", box j width: " << all_orientations[j].width << " dp[j]: " << dp[j] << endl;
            // Box j can be placed on top of box i and they're not the same physical box
            if (all_orientations[j].width < all_orientations[i].width && all_orientations[j].index != all_orientations[i].index) {
                dp[i] = std::max(dp[i], dp[j] + 1);
            }
        }

        cout << "i: " << i << ", dp[i]: " << dp[i] << endl;
        max_count = std::max(max_count, dp[i]);
    }

    return max_count;
}

int main() {
    // std::vector<Box> boxes = { {2, 2, 0}, {3, 2, 1}, {3, 4, 2}, {4, 3, 3} };
    // std::cout << maxStackedBoxes(boxes) << std::endl;

    vector<Box> boxes2 = {{5, 1, 0}, {4, 3, 1}, {3, 2, 2}};
    std::cout << maxStackedBoxes(boxes2) << std::endl;
    return 0;
}