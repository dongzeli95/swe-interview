---
description: >-
  Design a scalable backend system "Nearby Friends". For an opt-in user who
  grants permission to access their location, the mobile client presents a list
  of friends who are geographically nearby.
---

# Nearby Friends

## Functional Requirements

* User will be able to see a list of nearby friends.
* When new user come online/offline, we need to update as real time as possible.
* When user revoke the location permission, we would need to update.
* What search radius should we support? - 5 miles for example.
* Is distance calculated based on straight line distance? - Yes
* Store location history.
* Do we need to worry about privacy and data laws? - No

## Non-functional Requirement

* Highly available
* Low latency, see location updates from friends without delay.
* Availability > consistency, location history data doesn't have to be real-time.
* Read == Write

## Scale

* 100M active daily users.
* 10% concurrent user = 10M
* User report location every 30 seconds.
* QPS = 10M / 30s = 334000

### Traffic Estimation Method

| Peak Load (10% of DAU concurrent users)                                                                                                                        | Average Load (Use 10^5 sec a day as divider)                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| <mark style="background-color:green;">Takes into account the potential spikes in usage and ensures that your system is designed to handle maximum load.</mark> | <mark style="background-color:red;">Might not accurately capture sudden spikes in usage during specific times of the day.</mark> |
| <mark style="background-color:red;">Might overestimate the load during regular periods when not all users are active.</mark>                                   | <mark style="background-color:green;">Provides a more smoothed out estimation of load over a day.</mark>                         |

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (2) (1) (1).svg" alt="Architecture" class="gitbook-drawing">

## Websocket Diagram

User1's friends: User2, User3 and User4

User5's friends: User4, User6

<img src="../../.gitbook/assets/file.excalidraw (3).svg" alt="" class="gitbook-drawing">

We assign channel to every user who uses "nearby" feature. A user would, upon app initialization, subscribe to each friend's channel regardless whether the friend is online or not.

We trade memory for simpler architecture in this case.

## E2E

1. Client send both http/Websocket request to API Gateway with its own location.
   1. http request for fetching friends' list.
   2. websocket request for publishing its own location as well as subscribe to friends' channels.
2. API Gateway routes Websocket request onto Websocket servers and http request onto API servers.
3. Websocket services:
   * Fetch friends' locations, filter out friends out of radius.
   * Subscribe to friends' channels based on friend list.
   * Publish user's location to Redis pub/sub, this message got broadcasted to all subscribers channels.
   * Store user's location onto location cache.
   * On receiving broadcast messages from Redis Pub/Sub, connection handler computes the distance between two users, if distance is out of radius, the update is dropped.
4. HTTP services
   * Fetch all of friend list of the user.
   * Add/Remove friends -> api service calls websocket service to notify client a friend is added or removed (event handler from websocket) -> client sends back websocket request to subscribe/unsubscribe channels.
   * Store location into location history DB.

## API

### Websocket

* Websocket initialization (onConnect)
  * Request: Client send latitude, longitude and timestamp.
  * Response: Friend location with timestamp.

User subscribe to all of his/her friends' channels on connection.

* Periodic location update
  * Request: Client send latitude, longitude and timestamp.
  * Response: Nothing
* Client receives location updates
  * Event: Friend location with timestamp.
* Subscribe to a friend
  * Request: friend ID
  * Response: friend's location with timestamp

Subscribe to friend's channel.

* Unsubscribe a friend
  * Request: friend ID
  * Response: Nothing.

Unsubscribe to a friend's channel.

## Data Model

### Location Cache

| key      | value                            |
| -------- | -------------------------------- |
| user\_id | {latitude, longitude, timestamp} |

Use TTL to automatically purge inactive user's location, this helps prevent user receive location data from inactive friends.

## Scale

### API servers

stateless servers, auto-scale the clusters based on CPU, load or I/O.

### Websocket servers

> Effective auto-scaling of stateful servers is the job of a good load balancer.

They are stateful. Before a node can be removed, all existing connections should be allowed to drain. Mark the node at the load balancer so no new websocket connections will be routed to the draining server.

### User database

The user database holds two distinct sets of data: user profiles and friendships. Data is horizontally scalable by sharing based on User ID.

### Location Cache

<mark style="color:blue;">**Memory**</mark>:

10M active users \* 100 bytes = 1GB

<mark style="color:orange;">**QPS**</mark>:

10M active users, update every 30s = 334k per seconds.

QPS is too high, we need to shard location data based on user ID and replicate location data on each shard to improve availability.

Read replicas are not enough because the write QPS is large.

### Redis Pub/Sub Server

<mark style="color:blue;">**Memory**</mark>:

1B users \* 10% = 100M users = 100M channels.

20 bytes to track each subscriber using hash table and linked list.

On average, each user has around 100 friends.

100M channels \* 20 bytes \* 100 friends / 10^9 = 200 GB

We need **2 Redis Pub/Sub** servers with 100 GB

<mark style="color:orange;">**QPS**</mark>:

10M active users + update every 30 seconds = 334k QPS.

On average user have 400 friends, only 10% online and nearby:

334K \* 400 \* 10% = 14M location pushes.

Assume a modern server with a gigabit network can handle 100k push per second.

14M / 100k = 140 Redis servers.

#### Distributed Redis Pub/Sub server

Use some service discovery component like etcd, ZooKeeper to:

1. Keep a list of servers, a simple UI or API to update it.

```
Key: /config/pub_sub_ring
Value: ["p_1", "p_2", "p_3", "p_4"]
```

2. For client (websocket servers) to subscribe to any updates to the "Value" (a list of Redis Pub/Sub servers)

<img src="../../.gitbook/assets/file.excalidraw (4).svg" alt="" class="gitbook-drawing">

## FAQ

* [ ] Why not use socketio room with certain geo\_locations? And when user comes in, we just check see if this person A and person B's friend? What's the pros and cons of this way vs using each user as a room.
* [ ] Can i use the same redis instance for both pub/sub and cache?
* [ ] Websocket diagram.
* [ ] Deep-dive and scale.
