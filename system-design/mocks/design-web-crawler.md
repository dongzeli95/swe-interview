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

Scheduler: used to schedule crawling events on URLs that are stored in its database.

DNS: needed to get IP address resolution of the web pages.

Cache: utilized in storing fetched documents for quick access by all processing modules.

Blob store: store crawled content permanently for indexing.

HTML fetcher: establishes a network communication connection between crawler and web hosts.

Service host: manages crawling operation among workers.

Extractor: extracts embedded URLs and document from web page.

Duplicate eliminator: dedup testing on incoming URLs and documents.

## E2E

1. Assignment to a worker\
   The crawler (service host) initiates the process by loading a URL from scheduler's priority queue and assigns it to the available worker.
2. DNS resolution\
   The worker sends the incoming URL for DNS resolution. DNS resolver checks the cache and returns the requested IP address if it's found. Otherwise, it determines the IP address, sends it back to the worker instance of the crawler and store the result in the cache.
3. Communication by HTML fetcher\
   initiate communication between the crawler and host server.
4. Content extraction\
   worker establishes communication, the worker extracts URLs and HTML document from web pages and places the document in a cache for other components to process it.
5. Dedup testing\
   dedup eliminator calculates and compare checksum of both URL and document.
6. Content storing\
   The extractor sends the newly discovered URLs to scheduler. Save then in DB and sets value for priority.
7. Recrawling\
   Once a cycle is complete, the crawler goes back to first point and repeats the same process until URL frontier query is empty.\
