"""
Piled Boxes (Maximum Stacked Boxes)

Given a list of boxes with 2 dimensions (width, height), return the maximum
number of boxes that can be stacked on each other. A box may be rotated
(so [3, 2] can become [2, 3]). A box can only be placed on top of another
if its width is strictly less than the width of the box below it. The same
physical box cannot be used twice in a stack (even in different orientations).

Approaches:
    1. maxStackedBoxes - O(n^2) DP over all orientations sorted by width,
       tracking original box index to prevent reusing the same physical box.
"""

from typing import List


class Box:
    def __init__(self, w: int, h: int, idx: int) -> None:
        self.width = w
        self.height = h
        self.index = idx  # index of the original physical box


def maxStackedBoxes(boxes: List[Box]) -> int:
    # Create a list of all orientations
    all_orientations: List[Box] = []
    for i, b in enumerate(boxes):
        all_orientations.append(Box(b.width, b.height, i))
        all_orientations.append(Box(b.height, b.width, i))

    # Sort by width (ties broken by original box index), so that a box can
    # only be stacked on top of one whose width is strictly greater.
    all_orientations.sort(key=lambda b: (b.width, b.index))

    # DP table: dp[i] = max stack height ending with orientation i on top
    dp = [1] * len(all_orientations)

    max_count = 0
    for i in range(len(all_orientations)):
        for j in range(i):
            print(
                f"box i width: {all_orientations[i].width}, "
                f"box j width: {all_orientations[j].width} dp[j]: {dp[j]}"
            )
            # Box j can be placed on top of box i and they're not the same physical box
            if (
                all_orientations[j].width < all_orientations[i].width
                and all_orientations[j].index != all_orientations[i].index
            ):
                dp[i] = max(dp[i], dp[j] + 1)

        print(f"i: {i}, dp[i]: {dp[i]}")
        max_count = max(max_count, dp[i])

    return max_count


if __name__ == "__main__":
    # boxes = [Box(2, 2, 0), Box(3, 2, 1), Box(3, 4, 2), Box(4, 3, 3)]
    # print(maxStackedBoxes(boxes))

    boxes2 = [Box(5, 1, 0), Box(4, 3, 1), Box(3, 2, 2)]
    print(maxStackedBoxes(boxes2))
