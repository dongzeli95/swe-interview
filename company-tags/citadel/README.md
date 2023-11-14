# Citadel

[longest\_non\_decreasing\_subarray.md](../../algorithm/dp/md/longest\_non\_decreasing\_subarray.md "mention")

[number\_of\_good\_binary\_strings.md](../../algorithm/dp/md/number\_of\_good\_binary\_strings.md "mention")

[minimum\_knight\_moves.md](../../algorithm/bfs/md/minimum\_knight\_moves.md "mention")

[delete\_and\_earn.md](../../algorithm/dp/md/delete\_and\_earn.md "mention")

[maximum\_path\_sum.md](../../algorithm/binary\_tree/md/maximum\_path\_sum.md "mention")

[lfu\_cache.md](../../algorithm/design/md/lfu\_cache.md "mention")

[lru\_cache.md](../../algorithm/design/lru\_cache/md/lru\_cache.md "mention")

[knight\_probability\_in\_board.md](../../algorithm/bfs/md/knight\_probability\_in\_board.md "mention")

[robot\_room\_cleaner.md](../../algorithm/dfs/md/robot\_room\_cleaner.md "mention")

[minimum\_height\_tree.md](../../algorithm/bfs/md/minimum\_height\_tree.md "mention")

[evaluate\_reverse\_polish\_notation.md](../../algorithm/stack/evaluate\_reverse\_polish\_notation/md/evaluate\_reverse\_polish\_notation.md "mention")

[get\_random.md](../../algorithm/design/md/get\_random.md "mention")

[validate\_bst.md](../../algorithm/binary\_search\_tree/md/validate\_bst.md "mention")

[find\_duplicate\_num.md](../../algorithm/array/md/find\_duplicate\_num.md "mention")

[permutations.md](../../algorithm/backtracking/md/permutations.md "mention")

[buy\_and\_sell\_stock.md](../../algorithm/dp/md/buy\_and\_sell\_stock.md "mention")

[house\_robber.md](../../algorithm/dp/md/house\_robber.md "mention")

[subarray\_sum\_k.md](../../algorithm/prefix\_sum/md/subarray\_sum\_k.md "mention")

[n\_queens.md](../../algorithm/backtracking/md/n\_queens.md "mention")

[range\_addition.md](../../algorithm/prefix\_sum/md/range\_addition.md "mention")

[minimum\_costs\_using\_train\_line.md](../../algorithm/dp/md/minimum\_costs\_using\_train\_line.md "mention")

[smallest\_range\_ii.md](../../algorithm/greedy/md/smallest\_range\_ii.md "mention")

[fibonacci.md](md/fibonacci.md "mention")

[pi.md](md/pi.md "mention")

[probability.md](md/probability.md "mention")

## Python

```python
nums = [1,2,3]
nums.append(1)
nums.pop()
nums.sort()

# Dictionary
dict = {'a':1,'b':2,'c':3}
dict.keys() # returns list of keys of dictionary
dict.values() # returns list of values of dictionary

dict.get('a') # returns value for any corresponding key
dict.items() # returns [('a',1),('b',2),('c',3)]
dict.pop(KEY) # pops key-value pair with that key

# A double-ended queue, or deque, has the feature of adding and removing elements from either end.
from collections import deque

queue = deque(['name','age','DOB'])

queue.append("append_from_right") # Append from right
queue.pop() # Pop from right

queue.appendleft("fromLeft") # Append from left
queue.popleft() # Pop from left

# min heap
nums = [5, 7, 9, 1, 3]
heapq.heapify(nums) # converts list into heap. Can be converted back to list by list(nums).
heapq.heappush(nums,element) # Push an element into the heap
heapq.heappop(nums)

# max heap
nums = [5, 7, 9, 1, 3]
nums = [-num for num in nums]  # Negate all elements
heapq.heapify(nums)  #
largest_element = -heapq.heappop(nums)


text = 'Python is a fun programming language'

# split the text from space
print(text.split(' '))
name = "M3onica Gell22er "
print(name.isalnum()) # Output : False
#The isalpha() method returns True if all characters in the string are alphabets. If not, it returns False
name = "Monica"
print(name.isalpha()) #output true

```
