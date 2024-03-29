# Design Web Crawler

## [Web Crawler Study Link](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system\_design/web\_crawler/README.md)

## [Web Crawler Medium Link](https://jc1175.medium.com/how-i-would-design-a-web-crawler-9013251fa9f3)

## Topics

1. Politeness / Crawl Rate
2. DNS query
3. Distributed Crawling
4. Priority Crawling
5. Duplicate detection

## Functional Requirements

1. Crawling: The system should scrape www, spanning from a queue of seed URLs provided initially by the system admin.\
   Two ways to get them: 1. manually create 2. scan IP address of web servers
2. Storing: The system should be able to extract and store content of a URL in a blob store. Make it processable by search engine for indexing and ranking.
3. Scheduling: Since crawling is a process that's repeated, the system should have regular scheduling to update its blob stores records.
4. Throttling on crawl speed / Politeness?
5. Crawling based on priority?
6. Deduplicate urls.
7. Do we think about search?

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

total = 5 Billion x 60ms = 0.3B seconds = 9.5 year

1 server = 3468 days.

we need 3468 servers to finish it in a day.

## API

```
CRUD

/v1/crawl/seeds POST
json {
  "urls": [url1, url2...],
}

/v1/crawl?url=xxx PUT
Response: 201

/v1/search?query=hello+world GET
```

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (14).svg" alt="" class="gitbook-drawing">

Scheduler: used to schedule crawling events on URLs that are stored in its database.

* Priority Queue (URL frontier): The queue hosts URLs that are made ready for crawling based on priority and update frequency.
* RDBMS: store urls with priority and update(recrawl) frequency.&#x20;

## E2E

1. Assignment to a worker\
   The crawler (service host) initiates the process by loading a URL from scheduler's priority queue and assigns it to the available worker.
2. DNS resolution\
   The worker sends the incoming URL for DNS resolution. DNS resolver checks the cache and returns the requested IP address if it's found. Otherwise, it determines the IP address, sends it back to the worker instance of the crawler and store the result in the cache.
3. Communication by HTML fetcher\
   initiate communication between the crawler and host server.
4. Content extraction\
   Once html fetcher get the web page, the next step would be to extract URLs and content from the webpage. The extractor sends the extracted URLs and content with document input stream (DIS) to duplicate eliminator. Once verified no duplicates, extractor store content in blob storage and send URL to URL frontier for recrawl.
5. Dedup testing\
   Duplicate eliminator calculates and compares checksum of both URL and document with checksum values that stored in DB.  It discards the incoming request in case of a match. If no match, it places new calculated checksum value in DB and gives go ahead to extractor.

Calculating checksum word by word for whole document is probably very time consuming

[minhash](https://en.wikipedia.org/wiki/MinHash) and [simhash](https://en.wikipedia.org/wiki/SimHash) (a method of seeing how close two sets are), [fuzzy search](https://en.wikipedia.org/wiki/Approximate\_string\_matching) (searching to see if the documents are roughly similar)

1. Content storing\
   The extractor sends the newly discovered URLs to scheduler. Save then in DB and sets value for priority.
2. Recrawling\
   Once a cycle is complete, the crawler goes back to first point and repeats the same process until URL frontier query is empty.\


## Deep dive

### How we get the seed URLs?

1. manually creat them
2. scan IP addresses for the presence of the web servers

seed URLs must be of good quality.

### Why we need DNS resolver:

1. We are crawling using a library but not from browser, avoid additional network hops.
2. DNS resolver is synchronous and not work with multi-thread worker architecture.

### Crawler Traps

a set of URLs that cause indefinite crawler resource exhaustion.

1. URLs with query parameters
2. URLs with internal links
3. URLs with dynamic content generation
4. URLs with repeated cyclic directories.

we need to identify them:

1. Analyze URL scheme, if URL is poor structured, we skip.

```
http://www.abc.com/first/second/first/second/...
```

1. Analyze the total number of web pages against a domain, set a cap.

### Robot.txt

This file contains DOs and DONTs for a crawler listed by web owner. This is called robots exclusion protocol. We need to respect it to only crawl only the allowed urls.

### URL Frontier

Front queues are for priorities, Back queues for politeness.

1. Priority

How to set priority:

* How frequently the site is changing?

2. Politeness

Put the url from same site onto same back queue to make sure we don't overwhelm it.

One back queue is associated with one worker thread.

* Instad of using static crawl speed for every domain, we can adjust crawl speed based on domain's time to first byte (TTFB) value. The higher the value, the slower the server is so we need to crawl slower.

3. Freshness



<img src="../../.gitbook/assets/file.excalidraw (30).svg" alt="" class="gitbook-drawing">

Partition metadata table

| Host           | Back queue ID |
| -------------- | ------------- |
| digit.com      | 5             |
| techcrunch.com | 1             |
| youtube.com    | 17            |

