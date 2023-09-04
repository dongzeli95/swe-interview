---
description: >-
  Replication means keeping a copy of the same data on multiple machines that
  are connected via a network.
---

# Chapter 5: Replication

## Why replicate data?

* Keep data geographically close to users, for example: CDN, edge cache (reduce latency)
* Increase availability if some part of system failed.
* Increase read throughput.

## Common Topics

* Synchronous vs Asynchronous Replication
* How to handle failed replicas

## Single Leader

1. One of the replicas is designated the _leader_ (_master_ or _primary_). Writes to the database must send requests to the leader.
2. Other replicas are known as _followers_ (_read replicas_, _slaves_, _secondaries_ or _hot stanbys_). The leader sends the data change to all of its followers as part of a _replication log_ or _change stream_.
3. Reads can be query the leader or any of the followers, while writes are only accepted on the leader.

Examples:

* MySQL, MongoDB, Kafka, RabbitMQ

### Sync vs Async replication

| Sync                                                                     | Async                                                     |
| ------------------------------------------------------------------------ | --------------------------------------------------------- |
| <mark style="background-color:green;">Up-to-date copy of data</mark>     | Stale data                                                |
| Block the write if follower doesn't responde or crash                    | <mark style="background-color:green;">Non-blocking</mark> |
| <mark style="background-color:green;">Strong durability guarantee</mark> | Weakening durability if leader fails without recovery     |

> If you enable synchronous replication on database, it means one of the replica is synchronous. This guarantee up-to-date data copy on **two** nodes. semi-synchronous
>
> Weakening durability might sound bad but it's widely used.

### Setting up new follower

Copying data files from one node to another is typically not sufficient.

Setting up a follower can usually be done without downtime. The process looks like:

1. Take a snapshot of the leader’s database
2. Copy the snapshot to the follower node
3. Follower requests data changes that have happened since the snapshot was taken
4. Once follower processed the backlog of data changes since snapshot, it has _caught up_.

### Handling node outages

How does high availability works with leader-based replication?

#### follower failure

On local disk, the follower keeps a log of data changes received from leader. It can connect to the leader and request all data changes occurred during the downtime.

#### leader failure

One of the followers needs to be promoted to be the new leader, clients need to be reconfigured to send their writes to the new leader and followers need to start consuming data changes from the new leader.

Automatic failover consists:

1. Determining that the leader has failed. If a node does not respond in a period of time it’s considered dead.
2. Choosing a new leader. The best candidate for leadership is usually the replica with the most up-to-date changes from the old leader.
3. Reconfiguring the system to use the new leader. The system needs to ensure that the old leader becomes a follower and recognises the new leader.

Things that could go wrong:

* When a new leader is chosen after the failure of the old leader, there are two potential issues:
  1. **Incomplete Writes:** The new leader may not have received all the writes that were originally made to the old leader before it failed. This can lead to missing or inconsistent data if the new leader starts processing requests before catching up with all the previous writes.
  2. **Conflicting Writes:** During the leader transition, there's a possibility that both the old leader and the new leader receive writes concurrently. If these writes conflict (e.g., updating the same piece of data), it can result in data inconsistencies.

<mark style="color:yellow;">To handle conflicting writes, the system needs to have mechanisms in place to resolve these conflicts. One common approach is to timestamp each write and choose the write with the highest timestamp as the valid one. Another approach is to prioritize writes based on some predefined rules. Conflict resolution can also involve human intervention, especially in cases where automated resolution might not be sufficient.</mark>

<mark style="color:yellow;">In some cases, synchronous replication might be used, where writes are not acknowledged until they have been replicated to a certain number of nodes. This can help prevent data loss during leader transitions.</mark>

* Discarding writes is especially dangerous if other storage systems outside of the database need to be coordinated with the database contents.

<mark style="color:yellow;">Implementing two-phase commits or transactional mechanisms can ensure that changes across multiple storage systems are coordinated and atomic. Two-phase commit protocols involve a distributed transaction coordinator that ensures all involved systems commit or rollback changes together. This helps maintain data integrity across different systems.</mark>

* It could happen that two nodes both believe that they are the leader (_split brain_). Data is likely to be lost or corrupted.

<mark style="color:yellow;">To prevent split brain scenarios, distributed systems often use quorum-based approaches. Quorums ensure that a majority of nodes must agree on the status of the leader before any decisions are made. This prevents the formation of multiple leaders simultaneously. For instance, a majority of nodes (N/2 + 1) must agree on a leader to avoid split brain scenarios in a cluster of N nodes.</mark>

* What is the right time before the leader is declared dead?

<mark style="color:yellow;">Implementing various timeout mechanisms can help in determining leader failure. For example, a leader heartbeat mechanism where nodes regularly send signals to indicate their liveliness can be used. If other nodes detect a prolonged absence of these signals, they might initiate leader election. Additionally, quorum-based approaches can be employed to ensure that a leader is only declared dead when a majority of nodes agree on it.</mark>

### Replication Logs

#### Statement replication

The leader logs every statement and sends it to its followers (every INSERT, UPDATE or DELETE)

Cons:

* Non-deterministic functions such as `NOW()` or `RAND()` will generate different values on replicas.
* Statements that depend on existing data, like auto-increments, must be executed in the same order in each replica.
* Statements with side effects (triggers, stored procedures) may result in different outcome on each replica.

Solution: replace any non-deterministic function with a fixed return value in the leader.

#### Write-ahead log (WAL)

The log is an append-only sequence of bytes containing all writes to the database. We cam ise exact same log to build a replica on another node. The leader writes the log to disk and send them across the network to its followers.

Examples: PostgreSQL, Oracle.

Cons:

Log describes data at a very low level (which bytes were changed in which disk blocks), making it tightly coupled with storage engine. It's not possible to run different versions, hence impossible to have zero-downtime upgrade of database.

#### Logical (row-based) log replication - Change Data Capture

A sequence of records describing writes to database table at granularity of a row.

* For an inserted row, the new values of all columns.
* For a deleted row, the log contain information uniquely identify the row, primary key or old values.
* For a updated row, new values of the columns.

Pros:

* Logical log is decoupled from storage engine internals, it's easier to make it backwards compatible.
* Easier to parse for external system like data warehouse for offline analysis, custom indexes and caches.

#### Trigger-based replication

A trigger lets you register custom application code that is automatically executed when a data change (write transaction) occurs. It's possible to log the change into a separate table which can be read by external process.&#x20;

Example: Oracle's Databus, Bucardo for Postgres.

Cons:

It's on application layer. Greater overhead than other replication methods. More prone to bugs but might be useful due to its flexibility.

### Replication Lag

If an application reads from an asynchronous follower, it may see outdated information if follower has fallen behind.&#x20;

#### Reading your own writes (read-after-write consistency)

Read from leader based on:

* If user modified the piece of information.
* time of latest update.

#### Monotonic reads (read order)

> A user first reads from a fresh replica, then from a stale replica. Time appears to go backward.

Monotonic Reads is a guarantee that "moving back in time" anomaly does not happen.

Make sure user always make their reads from the same replica. It can be chosen based on hash of user ID.&#x20;

#### Consistent prefix reads (write order)

> If some partitions are replicated slower than others, an observer may see the answer before they see the question.

This only happens in sharded db.

Writes casually related to each other are written to the same parition.

#### Solution for Replication Lag: <mark style="color:blue;">**Transactions**</mark>

## Multi-Leader Replication

Allow more than one node to accept writes. Each node processes a write will forward data change to all the other nodes.

### Use Cases

#### Multi-datacenter operation

Have a leader in each datacenter. Each datacenter leader replicates its change to the leaders in other datacenters.

|                                | Single-leader configuration                                                                                                                                | Multi-leader configuration                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Performance                    | <mark style="background-color:red;">Writes must go over internet to the datacenter with leader. Add significant latency if datacenter is not local.</mark> | <mark style="background-color:green;">Writes can be processed in local datacenter and replicated asynchronously to other datacenters. Performance is better.</mark> |
| Tolerance of datacenter outage | <mark style="background-color:red;">Failover to promote a follower in another datacenter as leader.</mark>                                                 | <mark style="background-color:green;">No Impact. Replication catches up when failed datacenter comes back online.</mark>                                            |

#### Clients with offline operation

If you have an application that needs to continue to work while it's offline. Every device that has a local database is a leader, and there will be some asynchronous multi-leader replication. (Imagine, a Calender app)

CouchDB is designed for this mode of operation.

#### Collaborative editing

> When one user wants to edits a document, the changes are instantly applied to local replica, and asynchronously replicated to other users.

Google Docs allow multiple people to concurrently edit a text document or spreadsheet using Automatic Conflict Resolution.&#x20;

For faster collaboration, you may want to avoid locking, but it also brings multi-leader replication challenge including requiring conflict resolution.

### Handling Write Conflicts

