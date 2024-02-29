# Message Queue

## Why to use message queue?

* Decoupling. Message queues eliminate the tight coupling between components so they can be updated independently.
* Improved scalability. We can scale producers and consumers independently based on traffic load. For example, during peak hours, more consumers can be added to handle the increased traffic.
* Increased availability. If one part of the system goes offline, the other components can continue to interact with the queue.
* Better performance. Message queues make asynchronous communication easy. Producers can add messages to a queue without waiting for the response and consumers consume messages whenever they are available.

## Why to use Kafka vs SQS or other message brokers?

JMS(Java Message Service) vs AMQP (Advanced Message Queuing Protocol)

Traditional message brokers: ActiveMQ, SQS, RabbitMQ

Log-based message brokers: Kafka, Amazon Kinesis.

Log-based message brokers uses write-ahead mechanism to persist logs in disk.

<mark style="color:blue;">Pros:</mark>

* It supports fan-out messaging (Multiple consumers subscribe to the same topic) naturally, because several consumers can independently read the log and it won't delete the log.
* Ordering is guaranteed for nodes consuming on a single partition.

<mark style="color:red;">Cons:</mark>

* The number of nodes sharing the work of consuming a topic can be at most the number of partitions in that topic. Because a node will have to consume all the messages within a partition, you can't split messages from a single partitions to multiple nodes.

> Except, you can manually make one node only read odd numbers and another read only even numbered offset messages. Or use thread pool but that is complicated and not recommended.

* If a single message is slow to process, it holds up the processing of subsequent messages in that partition.

## When to use Kafka?

* Message is fast to process.
* Need some ordering guarantee.

## When to use traditional message broker? SQS & ActiveMQ?

* Message is expensive to process and want to parallelize processing on a message-by message basis.
* Order is not important.

## Kafka

### Topics

Topics is a particular stream of data. It consists of one or more partitions, ordered, immutable sequences of messages.

### Partitions and Offset

Topics are split in partitions. Each message within a partition get an incremental id, called offset.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-25 at 10.20.56 AM.png" alt=""><figcaption></figcaption></figure>

### Brokers

A Kafks cluster consists of one or more brokers. Partitions are spread across brokers, After connecting to any broker, you have connectivity to the entire cluster, you can basically request all brokers with partitions info.

### Lag

A consumer is lagging when it's unable to keep up with producers messages. Lag is expressed as the number of offset that are behind the head of partition.

```
recover time = messages / (consume message per second - produce message per second)
```

### Consumer Group

Consumers can be grouped together for a given topic for maximizing the read throughput. Each consumer in a group read from mutually exclusive partitions. The horizontal scaling on a consumer group is bounded by number of partitions.&#x20;

We use multiple consumer group when we need to perform different operations on same topics. For example, some consumers might do some real-time analysis with data.&#x20;

### Vertical Scaling

Single-threaded ensures processing order guarantees.

AWS kinesis allow you to change batch size that can be sent to your lambda function.

Multi-threaded model:

1. Offset might be committed before a record is processed by consumers.
2. Message processing order can't be guaranteed since messages from the same partition could be processed in parallel.

## How to scale SQS?
