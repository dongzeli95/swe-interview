# Distributed Message Queue

## Functional Requirement

* Able to send task to message queue and get immediate response. (producer)
* Able to subscribe and fetch task from message queue. (consumer)
* Support topic? Yes
* Support ordering? Yes
* Delivery guarantee - Messages can be consumed repeatedly or only once.
  * at-least once, at-most once or exactly once, configurable.
* Message size? kb range.

## Non-functional Requirement

* Highly available
* Low latency
* Durable, message should not be missed.
  * Data should be persisted on disk and replicated on multiple nodes.

## API

```
publishMessage(string payload)
subscribeMessage()
```

## Data Schema

* Messages
* Write-ahead Log

Why use write-ahead log? Pros??

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (7).svg" alt="" class="gitbook-drawing">

### Components

* Producer: pushes messages to specific topics.
* Consumer group: subscribes to topics and consumes messages.
* Broker: holds multiple partitions. A partition holds a subset of messages for a topic.
* Storage:
  * Data storage: messages are persisted in data storage in partitions.
  * State storage: manages consumer states
    * The mapping between partitions and consumers.
    * The last consumed offset of consumer groups for each partition.
  * Metadata storage: persists configuration and properties of topics.
    * The number of partitions.
    * Retention period
    * Distribution of replicas.
* Coordination service:
  * Service discovery: which brokers are alive.
  * Leader election: one of the brokers is selected as active controller responsible for assigning partitions.
  * Apache ZooKeeper or etcd are commonly used for electing a controller.

## E2E

Producer

1. Producer sends messages to the routing layer.
2. The routing layer reads the replica distribution plan from metadata storage and caches it locally. When a message arrives, it routes the message to leader replica of that topic/partition.
3. The leader replica receives message and follower replicas pull data from leader.
4. When enough replicas have synced, the leader commits the data, the message is ready to be consumed, and it respondes to producer.

Consumer

1. A new consumer wants to join group-1 and subscribes to Topic-A, finding the coordinator broker of group-1.
2. The coordinator confirms that consumer has joined and assign partition to consumer.
3. Consumer fetches messages from last consumed offset, managed by state storage.
4. Consumer processes messages and commits offset back to broker.&#x20;
   1. Delivery semantics:\
      order of data processing\
      offset commiting

## Questions

* [ ] Why allowing multiple consumers to consume on same partition will break ordering guarantee? Why would it matter since the task can be subscribed by multiple consumers anyways?
