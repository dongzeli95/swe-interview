# Proximity Service

### Functional Requirements

1. Who are our end users? two sides: toB and toC
2. Serving side and ingestion side.
3. What is the search radius? What's the maximum radius allow?
4. How instantly do we want to update the business information

### Non-functional Requirements

1. Highly available
2. Low latency
3. consistency requirements?
4. Read > write

### QPS

Assuming we have 100M users and 5 search queries a day.

100M \* 5 / 10^5 = 10^8 \* 5 / 10^5 = **5000 QPS**

### APIs

```
GET v1/places?longitude=xxx&latitude=xxx&radius=xxx
```

Response:

\[business1, business2, business3 ...]

### Data Schema

#### Design Options

***

**Option 1: Store the business with only longitude and latitude**

Plain query over longitude and latitude for:

```
user_longitude-radius <= longitude <= user_longitude+radius
user_latitude-radius <= latitude <= user_latitude+radius
```

***

**Option 2: Evenly divided grid**

Segment the entire map into number of evenly divided grid.

Query -> We will just look for the segment that user location belongs to.

Pros:

* More efficient compared to option 1.

Cons:

* For each grid, there might be unevenly distributed number of businesses.
* If user zoom in/out, this is not very flexible to show number of businesses at different zoom level.

***

**Option 3:** [**Geohashing**](../deep-dive/geospatial-indexing/geohash.md)

Reducing the two-dimensional longitude and latitude data into one-dimensional string of letters and digits. Recursively dividing the world into smaller and smaller grids with each additional bit.

Pros:

* Very efficient and can fit any precision use cases.
* Not very straightforward to implement but luckily we have a lot of out-of-box libraries/solutions.

#### Option 4: [Quadtree](../deep-dive/quadtree.md)

Build a in-memory quadtree by partitioning the two-dimensional space by recursively subdividing it into four quadrants until the content of the grid meet a certain criteria, for example, 100 businesses maximum.

#### Geohash vs Quadtree

| Geohash                                                                                                                                           | Quadtree                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <mark style="background-color:green;">Easy to use and implement, No need to build a tree</mark>                                                   | <mark style="background-color:red;">Need to build a tree, harder to implement</mark>                                                                                                                                                                                                                                                                                                      |
| <mark style="background-color:red;">Grid size is fixed. Support returning businesses within a specific radius but not k-nearest businesses</mark> | <mark style="background-color:green;">Good fit for k-nearest businesses it can automatically adjust the query range until it returns k results.</mark>                                                                                                                                                                                                                                    |
| <mark style="background-color:red;">Precision is fixed, grid size is fixed, cannot adjust grid size based on item density.</mark>                 | <mark style="background-color:green;">Dynamically adjust the grid size based on population density.</mark>                                                                                                                                                                                                                                                                                |
| <mark style="background-color:green;">Update/Remove a business is as easy as deleting that geohash record.</mark>                                 | <p><mark style="background-color:red;">Updating index is more complicated than geohash.</mark><br><br>If a business is removed, we need to traverse from root to leaf node in order to remove business. Locking mechanism is also required if multiple threads are modifying it.<br><br>Also need to think about rebalancing the tree, A possible fix is to over-allocate the ranges.</p> |

***

#### Business Table

| Column    | Type   |
| --------- | ------ |
| id        | string |
| name      | string |
| longitude | float  |
| latitude  | float  |
| geohash   | string |

#### Serving Algorithm

1. Convert user's location to a geohash with a precision based on the radius.
2. Start with geohashes with same prefix as user's location, calculate neighboring geohashes and add them to a list.
3. For each geohash in the list, fetch businesses:

```
SELECT * FROM geohash_index WHERE geohash LIKE '9q8zn%'
```

4. Filter these results by calculating distance between each business to user's location and only keep businesses that are within the search radius.
5. Rank result list and return to client.

### High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

### Caching

Caching is not a solid win because:

* The workload is read-heavy, the dataset is relatively small. The data could fit in the working set of any modern database server. (1.7GB), the queries are not I/O bound and they should run almost as fast as in-memory cache.
* If read is bottleneck, we can add more read replicas to improve read throughput.

#### Cache key selection

*   _<mark style="color:blue;">**Location coordinates**</mark>_ (latitude, longitude).

    Cons:

    * location returned from device not always accurate, will change slightly every time.
    * user can move
    * hit rate is terrible if we use location.
* _<mark style="color:blue;">**Geohash and business id**</mark>_

| Key         | Value                  |
| ----------- | ---------------------- |
| geohash     | a list of business ids |
| business id | business entity        |

According to requirements, user can select different radius: 500m, 1km, 2km and 5km. Those radius mapped to 4, 5, 5, and 6 for geohash length. We can cache data on geohash#precision like geohash\_4, geohash\_5 and geohash\_6.

#### Memory

Redis storage: 8 bytes x 200M x 3 precisions = 5GB
