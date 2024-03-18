---
description: >-
  A data structure that is commonly used to partition a two-dimensional space by
  recursively subdividing it into four quadrants until content of grids meet
  certain criteria.
---

# Quadtree

## Overview

Although similar to geohashing, quadtree is a in-memory solution, not a database solution.

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="quadtree structure" class="gitbook-drawing">

## Algorithm

```java
public void buildQuadtree(TreeNode node) {
  if (countNumberOfBusinessesInCurrentGrid(node) > 100) {
    node.subdivide();
    for (TreeNode child : node.getChildren()) {
      buildQuadTree(child);
    }
  }
}
```

## Memory

#### Leaf Node Memory

| Name                                            | Size                   |
| ----------------------------------------------- | ---------------------- |
| Top-left and bottom-right to identify the grid  | 32 bytes (8 bytes x 4) |
| List of business IDs (for example: maximum 100) | 8 bytes x 100          |
| Total                                           | 832 bytes              |

#### Internal Node Memory

Internal nodes doesn't contain business list information, it only holds the four references to its children.

| Name                                  | Size                   |
| ------------------------------------- | ---------------------- |
| Top-left and bottom-right coordinates | 32 bytes (8 bytes x 4) |
| Pointer to 4 children                 | 32 bytes (8 bytes x 4) |
| Total                                 | 64 bytes               |

#### Total Memory Calculation

For example: 200 Million businesses to store and each leaf can only have maximum of 100 businesses.

No. of leaf nodes = 200M / 100 = 2M

No. of internal nodes = 1/3 \* 2M = 0.67M

Total = 2M \* 832 bytes + 0.67M \* 64 bytes = 1.71GB

The total memory can be stored in a single server, depending on use cases, we might need more read replicas.

## Latency

m = n / 100 where n is total number of businesses.

Time = m \* log(m)

Take a few minutes to build entire quadtree with 200M businesses.

## Operational Complexity

1. Rollout strategy is important, incremental rollout to avoid putting large read throughput onto database.
2. How to update quadtree as businesses are added / removed.
   1. Offline crob job, Incrementally rebuild the quadtree, a small subset at a time.
   2. Update on the fly. More complicated since multiple threads can access the quadtree. Need some locking mechanism.

```python
    def nearest_neighbors(self, point, count=10):
        """
        Returns the nearest points of a given point, sorted by distance
        (closest first).

        The desired point does not need to exist within the quadtree, but
        does need to be within the tree's boundaries.

        Args:
            point (Point): The desired location to search around.
            count (int): Optional. The number of neighbors to return. Default
                is `10`.

        Returns:
            list: The nearest `Point` neighbors.
        """
        # Algorithm description:
        # * Search down to find the smallest node around the desired point,
        #   retaining a stack of nodes visited on the way down.
        # * Reverse the visited stack, so that it's now in
        #   smallest/closest-to-largest/furthest order.
        # * Iterate over the node stack.
        #   * Collect the points from the current node & it's children.
        #   * Sort the points by euclidean distance, using
        #     `euclidean_compare`, since the actual distance doesn't matter
        #     for now.
        #   * Add them to the "found" results.
        #   * If the "found" count is greater-than-or-equal to the desired
        #     count, break out of the loop.
        # * If the stack is exhausted, we have all the points in the entire
        #   quadtree & can just return them.
        # * Otherwise, we now have a decent set of results, ordered by
        #   distance. But we are not done. It's possible/probable that there
        #   are other nearby quadnodes that weren't touched by the search
        #   BUT are physically closer.
        # * Take our furthest point and use it as a radius for a search
        #   "circle".
        #     * We'll actually just create a bounding box, which is
        #       computationally cheaper & we already have methods that
        #       support it.
        #     * Using that radius as a distance to the *edge* (not a corner),
        #       we create a box big enough to fit the search circle.
        # * Collect all the points within that bounding box.
        # * Re-sort them by euclidean distance (again, using
        #   `euclidean_compare`).
        # * Slice it to match the desired count & return them.

        point = self.convert_to_point(point)
        nearest_results = []

        # Check to see if it's within our bounds first.
        if not self._root.contains_point(point):
            return nearest_results

        # First, find the target node.
        node, searched_nodes = self._root.find_node(point)

        # Reverse the order, as they come back in coarse-to-fine order, which
        # is the opposite of nearby points.
        searched_nodes.reverse()
        seen_nodes = set()
        seen_points = set()

        # From here, we'll work our way backwards out through the nodes.
        for node in searched_nodes:
            # Mark the node as already checked.
            seen_nodes.add(node)
            local_points = []

            for pnt in node.all_points():
                if pnt in seen_points:
                    continue

                seen_points.add(pnt)
                local_points.append(pnt)

            local_points = sorted(
                local_points, key=lambda lpnt: euclidean_compare(point, lpnt)
            )
            nearest_results.extend(local_points)

            if len(nearest_results) >= count:
                break

        # Slice off any extras.
        nearest_results = nearest_results[:count]

        if len(seen_nodes) == len(searched_nodes):
            # We've exhausted everything. Return what we've got.
            return nearest_results[:count]

        search_radius = euclidean_distance(point, nearest_results[-1])
        search_bb = BoundingBox(
            point.x - search_radius,
            point.y - search_radius,
            point.x + search_radius,
            point.y + search_radius,
        )
        bb_results = self._root.within_bb(search_bb)
        nearest_results = sorted(
            bb_results, key=lambda lpnt: euclidean_compare(point, lpnt)
        )

        return nearest_results[:count]
```
