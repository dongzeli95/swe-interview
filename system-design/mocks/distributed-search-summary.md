# Distributed Search Summary

## Functional Requirements:

1. User can search with a query keyword, it returns relevant posts/feeds/websites

## Non-Functional Requirements:

1. Highly available.
2. Low latency
3. Relevant feeds got returned in search result in a timely manner.

## Scale

### QPS:

Search API: 3M DAU = 3\*10^6 / 10^6 = 3 QPS \* 10(peak) = 30 QPS

### Data Size:

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (15).svg" alt="" class="gitbook-drawing">

How does each component work?

### Indexer component:

build reverse index / lucene index. It gets JSON document as an input and release index segments as an output.

#### Inverted Index:

An inverted index is a hashmap that employs a document-term matrix.

key: term, value: list of \[doc, freq, location]

doc: a list of documents in which term appeared.

freq: a list that counts frequency with which the term appears in each document.

loc: a two-dimensional list that pinpoints the position of the term in each document.

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
