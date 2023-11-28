# Design Web Crawler

## Functional Requirements

1. Crawling: The system should scrape www, spanning from a queue of seed URLs provided initially by the system admin.\
   Two ways to get them: 1. manually create 2. scan IP address of web servers
2. Storing: The system should be able to extract and store content of a URL in a blob store. Make it processable by search engine for indexing and ranking.
3. Scheduling: Since crawling is a process that's repeated, the system should have regular scheduling to update its blob stores records.

## Non-functional Requirements

1. Scalability: fetch hundreds of web documents.
2. Consistency: multiple crawling workers, having data consistency among all of them is necessary.
3. Performance: self throttling its crawling to a certain domain.

## Scale

1. 5 B web pages
2. text content per page is 2000 KB.
3. metadata for one web page is 500B.

Total storage: 5B x (2000kb + 500b) = 10PB

### Traversal time

total = 5 Billion x 60 = 0.3B seconds = 9.5 year

1 server = 3468 days.

we need 3468 servers to finish it in a day.

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (14).svg" alt="" class="gitbook-drawing">
