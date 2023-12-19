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

#### Search component:

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
