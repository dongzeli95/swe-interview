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
  * State storage: manages consumer states.
  * Metadata storage: persists configuration and properties of topics.
* Coordination service:
  * Service discovery: which brokers are alive.
  * Leader election: one of the brokers is selected as active controller responsible for assigning partitions.
  * Apache ZooKeeper or etcd are commonly used for electing a controller.

## Questions

* [ ] Why allowing multiple consumers to consume on same partition will break ordering guarantee? Why would it matter since the task can be subscribed by multiple consumers anyways?
