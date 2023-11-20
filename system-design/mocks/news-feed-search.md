# News Feed Search

## Functional Requirement

1. User can search relevant news feed.
2. User's news feed post can get indexed.

## Non-functional requirement

1. Highly available
2. Low latency
3. Availability > Consistency

## Scale

3M DAU = 3\*10^6 / 10^6 = 3 QPS = 30 QPS

## API

```
/v1/search?keyword=xxx
```

## Data Schema

Elastic Search + MySQL

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (13).svg" alt="" class="gitbook-drawing">
