"""
Can Place Flowers - https://leetcode.com/problems/can-place-flowers/

Approaches:
1. canPlaceFlower: Greedy single-pass scan planting whenever both neighbors
   are empty. Time: O(n), Space: O(1).
"""

from typing import List


# Time: O(n), Space: O(1)
def canPlaceFlower(flowerbed: List[int], n: int) -> bool:
    if not flowerbed:
        return n == 0

    capacity = 0
    s = len(flowerbed)
    for i in range(s):
        if flowerbed[i] == 0:
            if (i - 1 < 0 or flowerbed[i - 1] == 0) and \
               (i + 1 >= s or flowerbed[i + 1] == 0):
                capacity += 1
                flowerbed[i] = 1

    return capacity >= n


if __name__ == "__main__":
    # 0 0 0 0 0
    f1 = [0, 0]
    print(canPlaceFlower(f1, 1))  # True

    f2 = [1, 0, 0, 0, 1]
    print(canPlaceFlower(f2, 2))  # False

    f3 = [0, 0, 1, 0, 1]
    print(canPlaceFlower(f3, 1))  # True

    f4 = [0, 0, 0, 0, 0]
    print(canPlaceFlower(f4, 3))  # True

    f5 = [1, 0, 0, 0, 0]
    print(canPlaceFlower(f5, 3))  # False

    f6 = [1, 0, 0, 0, 0, 1]
    print(canPlaceFlower(f6, 2))  # False
