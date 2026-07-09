"""
Online Stock Span (LeetCode 901).

Approaches:
    1. StockPlanner       - Parallel arrays of prices and spans, jump backward
                            by previous spans. Time: O(n) amortized, Space: O(n).
    2. StockPlannerWithStack - Monotonic decreasing stack of (price, span) pairs,
                            pop while current price >= top price.
                            Time: O(n) amortized, Space: O(n).
"""


# Time: O(n), Space: O(n)
class StockPlanner:
    def __init__(self):
        self.prices: list[int] = []
        self.spans: list[int] = []

    def next(self, price: int) -> int:
        if not self.prices:
            self.prices.append(price)
            self.spans.append(1)
            return 1

        span = 1
        prev_idx = len(self.prices) - 1
        while prev_idx >= 0 and price >= self.prices[prev_idx]:
            span += self.spans[prev_idx]
            prev_idx -= self.spans[prev_idx]

        self.prices.append(price)
        self.spans.append(span)
        return span


# Improvement: Use a stack to store (price, span) pairs.
# We don't need to store every price and span in the vector, if the current span
# is greater than the previous span, we can pop the previous span.
# Time: O(n), Space: O(n)
class StockPlannerWithStack:
    def __init__(self):
        # Each entry: (price, span)
        self.st: list[tuple[int, int]] = []

    def next(self, price: int) -> int:
        if not self.st:
            self.st.append((price, 1))
            return 1

        span = 1
        while self.st:
            curr_price, curr_span = self.st[-1]
            if price < curr_price:
                break
            span += curr_span
            self.st.pop()

        self.st.append((price, span))
        return span


if __name__ == "__main__":
    stock_planner = StockPlanner()
    assert stock_planner.next(100) == 1
    assert stock_planner.next(80) == 1
    assert stock_planner.next(60) == 1
    assert stock_planner.next(70) == 2
    assert stock_planner.next(60) == 1
    assert stock_planner.next(75) == 4
    assert stock_planner.next(85) == 6

    stock_planner_with_stack = StockPlannerWithStack()
    assert stock_planner_with_stack.next(100) == 1
    assert stock_planner_with_stack.next(80) == 1
    assert stock_planner_with_stack.next(60) == 1
    assert stock_planner_with_stack.next(70) == 2
    assert stock_planner_with_stack.next(60) == 1
    assert stock_planner_with_stack.next(75) == 4
    assert stock_planner_with_stack.next(85) == 6
