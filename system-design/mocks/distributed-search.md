# Distributed Search

{% embed url="https://www.youtube.com/watch?v=0LTXCcVRQi0&t=2s" %}

## Functional Requirements:

1. User enters search query
2. Search engine finds relevant feeds.
3. User can see a list of feeds.

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (2).svg" alt="" class="gitbook-drawing">

## Scale

Database:

1. 1 Trilion pages
2. 100B unique pages
3. Each updated once every 10 days.
4. Average page is 2MB.

### Blob Storage Size

100B pages \* (2MB / page) = 200PB

### Database Storage Size

URL: 50B

hash: 16B

Blob: 16B

Last Updated: 8B

Title: 60B

Priority: 4B

Description: 150B

100B pages \* 340B / page = 31.4 TB

### Sharding

Sharding by url.

Use global index to map hash onto a url.

Use inverted index to map searched words onto feeds.



## API

1. Get page by URL
2. Get page by hash
3. Search for a word.

## Schema

url

site content

title&#x20;

description

hash

&#x20;last\_updated

priority



## [O2 search engine](https://betterprogramming.pub/how-we-built-o2-the-distributed-search-engine-based-on-apache-lucene-382e060a5328)

1. Separate base-search for storing index and keep them in k8s StatefulSet -> Low Latency. (hard drive storing search index)
2. Reorder using L2 ranking in midway search. midway search communicates with Redis cluster for information. This information contains key: product\_id, value: float array for product feature.



<figure><img src="../../.gitbook/assets/Screenshot 2023-11-23 at 8.15.45 AM.png" alt=""><figcaption></figcaption></figure>

## [Search engine](https://medium.com/double-pointer/system-design-interview-search-engine-edb66b64fd5e)

## [Search System: Design that scales](https://blog.devgenius.io/search-system-design-that-scales-2fdf407a2d34)

## Functional Requirement

User should get relevant content based on their search queries.

## Non-functional Requirement

* Highly available
* Low latency
* Low cost

## Scale

DAU: 3M = 3\*10^6 = 3 QPS = 30 QPS

one server can handle 1000 requests concurrently = 1 server

### Storage

The size of a single document: 100 KB

Number of unique terms from a document: 1000

Index table storage: 100 bytes per term

One document storage = 100KB + 1000\*100B = 200KB

6000 documents a day = 6000\*200KB = 12\*10^5KB = 12\*10^8 = 1.2GB

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1).svg" alt="" class="gitbook-drawing">

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

### How indexing work?

The mapreduce framework is implemented with help of a cluster manager and a set of worker nodes as mappers and reducers.

#### Cluster manager

The manager initiates the process by assigning a set of partitions to mappers. Once the mappers are done, the cluster manager assigns the output of mappers to reducers.

#### Mapper:

Extracts and filters terms from the partitions assigned to it by the cluster manager. These machines output inverted indexes in parallel which serve as input to reducers.

#### Reducers:

combines mappings for various terms to generate a summarized index.

## Deep Dive

### Indexing

indexing is the organization and manipulation of data that's done to faciliate fast and accurate information retrieval.

### Inverted Index

An inverted index is a hashmap that employs a document-term matrix.

key: term, value: list of \[doc, freq, location]

doc: a list of documents in which term appeared.

freq: a list that counts frequency with which the term appears in each document.

loc: a two-dimensional list that pinpoints the position of the term in each document.

### How efficiently the index can be updated if we add or remove a document?

The minimum part of the index is the Lucene segment. No way we can update a single document in place. The only option is commit a new index segment containing new and updated documents. Each new segment affect search latency since it adds computations.

To keep latency low, you have to index commits less often. which means there is a trade-off between latency and index update delay. Twitter engineers made a search engine called EarlyBird which solves this by implementing in-memory search in the not-yet committed segments.

In practice, we can use cache to make search results more stable.&#x20;

* [ ] How much computer memory, RAM is required to keep the index. We keep the index in the RAM to support low latency search.
* [ ] How quickly we can find a word from an inverted index.
* [ ] How efficiently the index can be updated if we add or remove a document.
* [ ] How critical it is for service to remain reliable.
* [ ] How resilient the system can be against SEO?
