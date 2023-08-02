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

