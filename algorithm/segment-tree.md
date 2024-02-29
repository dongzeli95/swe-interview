# Segment Tree

A _segment tree_ is a full binary tree where each node represents an interval. Generally, a node would store one or more properties of an interval that can be queried later.

```
{1, 3, 5, 7, 9, 11}
```

<img src="../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

### BUILD()

We visit each leaf of the _Segment Tree_. That makes **n** leaves. Also, there will be **n-1** internal nodes. So we process about **2 \* n** nodes. This makes the Build process run in O(n) linear complexity.

### Update()

The update process discards half of the range for every level of Recursion to reach the appropriate leaf in the tree. This is similar to binary search and takes logarithmic time. After the leaf is updated, its direct ancestors at each level of the tree are updated. This takes time linear to the height of the tree. So the complexity will be O(log(n))

### Query()

The query process traverses depth-first through the tree looking for the node(s) that match exactly with the queried range. At best, we query for the entire range and get our result from the root of the segment tree itself. At worst, we query for an interval or range of size **1** (which corresponds to a single element), and we end up traversing through the height of the tree. This takes time linear to the height of the tree. So the complexity will be O(log(n)).
