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

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

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
