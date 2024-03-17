# Distributed Message Queue

## [Confluent Kafka Doc](https://docs.confluent.io/kafka/design/delivery-semantics.html)

## Topics:

1. Producer delivery ack mechanism: at least, at most, exactly once.
2. Consumer receipt: at least, at most, exactly once.
3. Ordering guarantee.
4. Retries?
5. Consumer rebalancing?
6. Topics? Partitions? Brokers? Replicas?
7. Message consumption: push or pull?

## Functional Requirement

* Able to send task to message queue and get immediate response. (producer)
* Able to subscribe and fetch task from message queue. (consumer)
* Support topic? Yes so message can be consumed repeatedly.
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

Read/Write pattern:

* Write-heavy, read-heavy
* No update or delete operations.
* Sequential read/write access.

| Database                                                                                                 | Write-ahead log (WAL)                                                                            |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| <mark style="background-color:red;">Can't support both write-heavy and read-heavy access pattern.</mark> | <mark style="background-color:green;">WAL has pure sequential read/write access pattern.</mark>  |
|                                                                                                          | <mark style="background-color:green;">Disk performance of sequential access is very good.</mark> |

For WAL, a file cannot grow infinitely, we need segments. New messages are appended only to active segment file. When it reaches to certain size, we create a new active segment to accept writes. Non-active segments only serve read requests.

| Field Name | Data Type | Description                                                                                                   |
| ---------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| key        | byte\[]   | used to determine the partition of the message                                                                |
| value      | byte\[]   | payload of a message                                                                                          |
| topic      | string    | the name of the topic                                                                                         |
| partition  | integer   | ID of the partition                                                                                           |
| offset     | long      | <p>the position of the message in the partition. We can find a message using:<br>topic, partition, offset</p> |
| timestamp  | long      | timestamp                                                                                                     |
| size       | integer   | size of message                                                                                               |

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1).svg" alt="Basic version" class="gitbook-drawing">

1. Scale message queue -> cluster of brokers coordinated by zookeeper for leader election.
2. Consumer -> consumer groups for better read throughput.

<img src="../../.gitbook/assets/file.excalidraw (7).svg" alt="Fully scaled" class="gitbook-drawing">

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
4. Consumer processes messages and commits offset back to broker.
   1. Delivery semantics:\
      order of data processing\
      offset commiting

## Deep Dive

### Routing Layer

Producer send message to routing layer. The routing layer reads replica distribution plan and cache it. The routing layer route message to broker leader.

Buffer component is introduced in producer to batch messages in memory and sends out larger batches in a single request, increase throughput.

| Producer built-in routing                       | Extra routing layer |
| ----------------------------------------------- | ------------------- |
| No network latency and additional network hops. |                     |
| Cannot do batching.                             |                     |

Trade off around batch size:

batch size large, throughput large, latency high

batch size small, throughput small, latency lower

### Consumer Delivery - Push vs Pull

from broker to consumer

| Push                                                                                                                | Pull                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <mark style="background-color:green;">Low latency - broker can push message instantly after receiving.</mark>       |                                                                                                                                                         |
| <mark style="background-color:red;">Consumption rate fall below producer rate, consumer will get overwhelmed</mark> | <mark style="background-color:green;">Consumer controls consumption rate. If the rate of consumption falls below producer rate, we can scale up.</mark> |

Message queue use pull model.

### Consumer Rebalancing

### Producer Ack

1. In-sync replicas
2. Ack 0

Fire and forget.&#x20;

Producer keep sending messages to leader without waiting for acks.

Low latency with possible data loss.

Great use case for collecting metrics, logging data.

3. Ack 1

Producer wait for leader broker to persist the message.

Leader might fail immediately after sending ack so still potential data loss.

3. Ack all

Producer wait for all in-sync replicas to persist the message.

Provide strong message durability but latency is high almoist 2.5 times the original latency.

> If topic is hot, we can add more partitions to reduce connection load to leader replica

> Reading from leader replica might not be the best option. We can enable consumer to subscribe to closest ISR.&#x20;
>
> ISR is determined by topic configuration.&#x20;
>
> replica.lag.max.messages = 4 meaning the follower is a ISR as long as it's lagged not more than 3 messages than leader.

### Consumer Receipt (Delivery)

1. At most once
   1. Producer ack = 0, fire and forget
   2. Consumer commit before process data.
2. At least once
   1. Producer ack = 1 or ack = all
   2. Consumer commit after processing data. Same data maybe processed twice.
3. [Exactly once](https://youtu.be/Ki2D2o9aVl8) (payment, trading, accounting)
   1. Ack = all
   2. idempotency key for message data.
   3. Use transaction coordinator to track pending status + abort marker if something goes wrong.
   4. two phase commit.

## Questions

* [ ] Why allowing multiple consumers to consume on same partition will break ordering guarantee? Why would it matter since the task can be subscribed by multiple consumers anyways?
