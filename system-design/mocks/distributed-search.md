# Distributed Search

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

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

<img src="../../.gitbook/assets/file.excalidraw (1).svg" alt="" class="gitbook-drawing">

### How indexing work?

The mapreduce framework is implemented with help of a cluster manager and a set of worker nodes as mappers and reducers.

#### Cluster manager

The manager initiates the process by assigning a set of partitions to mappers. Once the mappers are done, the cluster manager assigns the output of mappers to reducers.

#### Mapper:

Extracts and filters terms from the partitions assigned to it by the cluster manager. These machines output inverted indexes in parallel which serve as input to reducers.

#### Reducers:

combines mappings for various terms to generate a summarized index.
