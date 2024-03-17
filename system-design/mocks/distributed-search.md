# Distributed Search

{% embed url="https://www.youtube.com/watch?v=0LTXCcVRQi0&t=2s" %}

## Functional Requirements:

1. User enters search query
2. Search engine finds relevant feeds.
3. User can see a list of feeds.

## Non-functional Requirement

* Highly available
* Low latency
* Low cost

## Scale

### QPS

DAU is 3M for search. The number of requests a single server can handle is 1000.

3k servers.

### Storage

The size of a single document: 100 KB

Number of unique terms from a document: 1000

Index table storage: 100 bytes per term

One document storage = 100KB + 1000\*100B = 200KB

6000 documents a day = 6000\*200KB = 12\*10^5KB = 12\*10^8 = 1.2GB

### Blob Storage Size

100B pages \* (2MB / page) = 200PB

### Sharding

Sharding by url.

Use global index to map hash onto a url.

Use inverted index to map searched words onto feeds.



## API

1. Get page by URL
2. Get page by hash
3. Search for a word.

## Schema

| Name                   | Description                            |
| ---------------------- | -------------------------------------- |
| Term                   | list of term to                        |
| \[doc, freq, location] |                                        |
| doc                    | identifier of the document             |
| freq                   | frequency of the term in the document  |
| location               | positions of the term in the document. |



## [O2 search engine](https://betterprogramming.pub/how-we-built-o2-the-distributed-search-engine-based-on-apache-lucene-382e060a5328)

1. Separate base-search for storing index and keep them in k8s StatefulSet -> Low Latency. (hard drive storing search index)
2. Reorder using L2 ranking in midway search. midway search communicates with Redis cluster for information. This information contains key: product\_id, value: float array for product feature.



<figure><img src="../../.gitbook/assets/Screenshot 2023-11-23 at 8.15.45 AM.png" alt=""><figcaption></figcaption></figure>

## [Search engine](https://medium.com/double-pointer/system-design-interview-search-engine-edb66b64fd5e)

## [Search System: Design that scales](https://blog.devgenius.io/search-system-design-that-scales-2fdf407a2d34)

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

<img src="../../.gitbook/assets/file.excalidraw (3).svg" alt="" class="gitbook-drawing">

### Indexer component:

build reverse index / lucene index. It gets JSON document as an input and release index segments as an output.

#### Inverted Index:

An inverted index is a hashmap that employs a document-term matrix.

key: term, value: list of \[doc, freq, location]

doc: a list of documents in which term appeared.

freq: a list that counts frequency with which the term appears in each document.

loc: a two-dimensional list that pinpoints the position of the term in each document.

### How indexing work?

The mapreduce framework is implemented with help of a cluster manager and a set of worker nodes as mappers and reducers.

#### Cluster manager

The manager initiates the process by assigning a set of partitions to mappers. Once the mappers are done, the cluster manager assigns the output of mappers to reducers.

#### Mapper:

Extracts and filters terms from the partitions assigned to it by the cluster manager. These machines output inverted indexes in parallel which serve as input to reducers.

#### Reducers:

combines mappings for various terms to generate a summarized index.

### Search component:

posting lists traversal, text relevancy scores computation, data extraction from DocValue fields.

#### Posting lists traversal

similar to reverse index, the list contains information about each occurrence of the term in the document collection.

* Document ID where the term is found.
* The position of the term within the document (for phrase and proximity queries)
* Additional metadata like term frequency.

How does it work?

1. Query processing\
   When a search query is received, the search engine breaks it down into individual terms.
2. Retrival of Posting Lists\
   For each term in the query, the search engine retrieves the corresponding posting lists. This process involves accessing the index, on disk or on memory.
3. Traversal of Posting Lists\
   The engine traverses lists to identify documents contain the query terms.

#### Text Relevancy Score Computation

How does it work?

1. Term frequency (TF):\
   More often a term appears in a document, more relevant that document is to the term.
2. Inverse Document Frequency (IDF)\
   Measures how common or rare a term is across all documents in search index. Terms that appear in many documents are less significant for determining relevancy, so they receive a lower IDF scores.
3. This is a combination of TF and IDF. It is used to reduce the weight of terms that occur very frequently in the document set and increase the weight of terms that occur rarely. TF-IDF is one of the most traditional methods for computing text relevancy.
4. BM25: \
   A more advanced and widely used algorithm in modern search engines. It improves upon the basic TF-IDF model by incorporating probabilistic models and handling limitations like term saturation.

## Deep Dive

### Indexing

indexing is the organization and manipulation of data that's done to faciliate fast and accurate information retrieval.

### Inverted Index

An inverted index is a hashmap that employs a document-term matrix.

key: term, value: list of \[doc, freq, location]

doc: a list of documents in which term appeared.

freq: a list that counts frequency with which the term appears in each document.

loc: a two-dimensional list that pinpoints the position of the term in each document.

### Why use Lucene instead of Elasticsearch?

Give possibility to make improvements on whatever level.

### Why separation of search phases?

Independent layers allow you to scale them independently.&#x20;

### How efficiently the index can be updated if we add or remove a document?

The minimum part of the index is the Lucene segment. No way we can update a single document in place. The only option is commit a new index segment containing new and updated documents. Each new segment affect search latency since it adds computations.

To keep latency low, you have to index commits less often. which means there is a trade-off between latency and index update delay. Twitter engineers made a search engine called EarlyBird which solves this by implementing in-memory search in the not-yet committed segments.

On Elasticsearch, it employs techniques like merging smaller segments into larger ones, which can improve search performance but also introduce latency during merge process.

### Why introduce S3 and CDN for storing indexes?

To save the network bandwidth limitation for downloading indices from indexer to search layer.

### Why personalized ranking related to search engine?

It affect where you cache your search results. Previously we cache search result for "microwave" query for users in Moscow and resue these results for further requests.\
Now we want more refined cache. Bob prefer "Toschiba" and Alice prefer "Panasonic" in our ranking.&#x20;

We stopped using cache on search backend, but rather on ranking.



## Appendix

Lucene using LSM tree (Log structured merge tree)

Before segments are flushed or commited, data is stored in memory and is unsearchable.

[EarlyBird Paper](https://cs.uwaterloo.ca/\~jimmylin/publications/Busch\_etal\_ICDE2012.pdf)

* [ ] How much computer memory, RAM is required to keep the index. We keep the index in the RAM to support low latency search.
* [ ] How quickly we can find a word from an inverted index.
* [ ] How efficiently the index can be updated if we add or remove a document.
* [ ] How critical it is for service to remain reliable.
* [ ] How resilient the system can be against SEO?
