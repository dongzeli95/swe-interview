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

### APIs

```
GET v1/places?longitude=xxx&latitude=xxx&radius=xxx
```

Response:

\[business1, business2, business3 ...]

### Data Schema

#### Design Options

Option 1: Store the business with only longitude and latitude

Plain query over longitude and latitude for:

```
user_longitude-radius <= longitude <= user_longitude+radius
user_latitude-radius <= latitude <= user_latitude+radius
```

Option 2: Evenly divided grid

Segment the entire map into number of evenly divided grid.

When&#x20;

#### Business Table

| Column    | Type   |
| --------- | ------ |
| id        | string |
| name      | string |
| longitude | float  |
| latitude  | float  |
| geohash   | string |

<img src=".gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

