
```python
import itertools
from collections.abc import Iterator

# https://realpython.com/python-iterators-iterables/#understanding-iteration-in-python
# Difference between iterable and iterator?

# Iterators take responsibility for two main actions:

# 1. Returning the data from a stream or container one item at a time
# 2. Keeping track of the current and visited items

# Note: In Python, you’ll commonly use the term generators to collectively refer to two separate concepts: 
# the generator function and the generator iterator. 
# The generator function is the function that you define using the yield statement. 
# The generator iterator is what this function returns.

# sequence_iter.py

class SequenceIterator(Iterator):
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._sequence):
            item = self._sequence[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration
        
class ReusableRange:
    def __init__(self, start=0, stop=None, step=1):
        if stop is None:
            stop, start = start, 0
        self._range = range(start, stop, step)
        self._iter = iter(self._range)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._iter)
        except StopIteration:
            self._iter = iter(self._range)
            raise

class ResumableIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.generator = self._create_generator(iterable)
        self.state = 0

    def _create_generator(self, iterable):
        for item in iterable:
            yield item

    def next(self):
        try:
            value = next(self.generator)
            self.state += 1
            return value
        except StopIteration:
            raise

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.generator = self._create_generator(self.iterable)
        next(itertools.islice(self.generator, self.state, self.state), None)

class Iterable:
    def __init__(self, sequence):
        self.sequence = sequence

    def __iter__(self):
        return SequenceIterator(self.sequence)

if __name__ == "__main__":
    for item in SequenceIterator(["1", 2, 3, 4, 5]):
        print(item)

    numbers_iter = SequenceIterator([1, 2, 3, 4, 5])
    print(next(numbers_iter))
    print(next(numbers_iter))
    print(next(numbers_iter))
    print(next(numbers_iter))
    print(next(numbers_iter))
    # print(next(numbers_iter)) StopIteration

# # Example usage
# iterable = [1, 2, 3, 4, 5]
# iterator = ResumableIterator(iterable)

# print(iterator.next())  # Outputs: 1
# print(iterator.next())  # Outputs: 2

# # Save state
# state = iterator.get_state()

# print(iterator.next()) # Outputs: 3

# # Restore state
# iterator.set_state(state)
# print(iterator.next())  # Outputs: 3
# print(iterator.next())  # Outputs: 4
# print(iterator.next())  # Outputs: 5```
