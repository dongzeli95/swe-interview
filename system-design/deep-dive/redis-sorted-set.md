# Redis Sorted Set

## Overview

A Redis sorted set is a collection of unique strings ordered by an associated score. When more than one string has the same score, the strings are ordered lexicographically.

Typical use cases:

1. Leaderboard
2. Rate limiter: You can use a sorted set to build a sliding-window rate limiter to prevent excessive API requests.

Sorted Sets is a mix between a Set and a Hash.&#x20;

Sorted sets are implemented via a dual-ported data structure contains both a skip list and a hash table, so add operation takes O(logN) time.&#x20;

When we read sorted elements, the operation is O(1). ZRANGE order is low to high, ZREVRANGE order is high to low.

ZREVRANK is available to get rank, considering the elements sorted in descending way.&#x20;
