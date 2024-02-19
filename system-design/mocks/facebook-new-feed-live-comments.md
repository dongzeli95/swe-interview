# Facebook New Feed Live Comments

Q:

1. How much is the scale? 1M DAU
2. How soon can user see the comments? ASAP

## Functional Requirements

1. User can send live comments
2. User can see other's made comments within couple of seconds.

## Non-functional Requirements

1. High availability
2. Low latency
3. Durability - user comments won't be lost.

## Scale

1. 1M DAU
2. 1M / 10^5 \* 5 = 50 QPS
3. Read: 50 QPS
4. Write: 5 QPS

Redis PubSub

1 server can have 100GB storage and 100k push per second.

N users commenting on M posts = N\*M channels

20 bytes per channel = 20M\*N channels

N = 1M, M = 1M = 20\*10^12 / 10^9 = 20\* 10^3 = 20000GB = 200 servers.

## API

Send live comments

v1/comment?uid=xxx\&message=xxx

Read live comments

v1/comments?post\_id=xxx

Web socket

wss://xxx-api.com

## Data Model

comments: uid, message, post\_id, parent\_comment, reply\_to

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (2) (1).svg" alt="" class="gitbook-drawing">

## E2E

1. Client A send a comment on post X.
2. Client B view a post comments on post X, created websocket connection and joined post X's channel.
3. the request routes through API Gateway onto specific backend pod.
4. Comment service do the following:\
   1\. publish new comment to post channel \
   2\. Talk to DB and store the comment onto comments table.

## Deep Dive

1. how to scale websocket server?

Before a node can be removed, all existing connections should be allowed to drain. Mark the node at the load balancer so no new connection is route to draining server.

2. what if DB is offline?

We can add a Kafka message queue to make sure the comment is saved when DB is back online.

3. Do we need to separate websocket server with query service?

Yes websocket servers have state where api servers don't.

4. How to scale Kafka?

Add more topics, add more partitions.

5. How to ensure message got sent at-least once or exactly-once?

We&#x20;

### Redis Pub/Sub Server

<mark style="color:blue;">**Memory**</mark>:

1M posts -> 1M channels

From one user to other users.

20 bytes to track each users on post using hash table and linked list.

On average, each user has around 100 friends.

1M channels \* 20 bytes \* 100 friends / 10^9 = 2GB

We need 1 **Redis Pub/Sub** servers with 100 GB

<mark style="color:orange;">**QPS**</mark>:

how many comments on post a day?

1M DAU \* 10%\*5 = 500000 comments

5\*10^5 / 10^6 = 0.5 QPS

0.5 QPS \* 100users on a post = 50 QPS

A modern server with a gigabit network can handle 100k push per second.

#### Distributed Redis Pub/Sub server

Use some service discovery component like etcd, ZooKeeper to:

1. Keep a list of servers, a simple UI or API to update it.

```
Key: /config/pub_sub_ring
Value: ["p_1", "p_2", "p_3", "p_4"]
```

2. Given a channel key (post id), websocket server need to figure out which redis pub/sub server to talk to for push and subscribe.

