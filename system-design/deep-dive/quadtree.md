---
description: >-
  A data structure that is commonly used to partition a two-dimensional space by
  recursively subdividing it into four quadrants until content of grids meet
  certain criteria.
---

# Quadtree

## Overview

Although similar to geohashing, quadtree is a in-memory solution, not a database solution.&#x20;

<img src="../../.gitbook/assets/file.excalidraw (1).svg" alt="quadtree structure" class="gitbook-drawing">

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
