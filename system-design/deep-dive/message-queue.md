# Message Queue

## Why to use message queue?

* Decoupling. Message queues eliminate the tight coupling between components so they can be updated independently.
* Improved scalability. We can scale producers and consumers independently based on traffic load. For example, during peak hours, more consumers can be added to handle the increased traffic.
* Increased availability. If one part of the system goes offline, the other components can continue to interact with the queue.
* Better performance. Message queues make asynchronous communication easy. Producers can add messages to a queue without waiting for the response and consumers consume messages whenever they are available.&#x20;

## Why to use Kafka vs SQS or other message brokers?

JMS(Java Message Service) vs AMQP (Advanced Message Queuing Protocol)

Traditional message brokers: ActiveMQ, SQS, RabbitMQ

Log-based message brokers: Kafka, Amazon Kinesis.&#x20;

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
* Order is not  important.
