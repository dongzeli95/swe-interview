---
description: >-
  A data structure that is commonly used to partition a two-dimensional space by
  recursively subdividing it into four quadrants until content of grids meet
  certain criteria.
---

# Quadtree

## Overview

Although similar to geohashing, quadtree is a in-memory solution, not a database solution.

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1).svg" alt="quadtree structure" class="gitbook-drawing">

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
