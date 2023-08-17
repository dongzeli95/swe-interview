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

* 100M active daily users.&#x20;
* 10% concurrent user = 10M
* User report location every 30 seconds.
* QPS = 10M / 30s = 334000

### Traffic Estimation Method

| Peak Load (10% of DAU concurrent users)                                                                                                                        | Average Load (Use 10^5 sec a day as divider)                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| <mark style="background-color:green;">Takes into account the potential spikes in usage and ensures that your system is designed to handle maximum load.</mark> | <mark style="background-color:red;">Might not accurately capture sudden spikes in usage during specific times of the day.</mark> |
| <mark style="background-color:red;">Might overestimate the load during regular periods when not all users are active.</mark>                                   | <mark style="background-color:green;">Provides a more smoothed out estimation of load over a day.</mark>                         |

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (2).svg" alt="Architecture" class="gitbook-drawing">

## Websocket Diagram

User1's friends: User2, User3 and User4

User5's friends: User4, User6

<img src="../../.gitbook/assets/file.excalidraw (3).svg" alt="" class="gitbook-drawing">

## E2E

1. Client send both http/Websocket request to API Gateway with its own location.
   1. http request for fetching friends' locations.
   2. websocket request for publishing its own location as well as subscribe to friends' locations.
2. API Gateway routes Websocket request onto Websocket servers and http request onto API servers.
3. Websocket services:
   * Fetch all of friend list of the user.
   * Subscribe to friends' channels based on friend list.
   * Publish user's location to Redis pub/sub, this message got broadcasted to all subscribers channels.
   * Subscribe to all friends' location channels.
   * Store user's location onto location cache.
   * On receiving broadcast messages from Redis Pub/Sub, connection handler computes the distance between two users, if distance is out of radius, the update is dropped.
4. HTTP services
   * Fetch friends' locations, filter out friends out of radius.
   * Add/Remove friends -> calls websocket service to notify client a friend is added or removed -> client sends back websocket request to subscribe/unsubscribe.
   * Store location into location history DB.

## FAQ

* [ ] Why not use socketio room with certain geo\_locations? And when user comes in, we just check see if this person A and person B's friend? What's the pros and cons of this way vs using each user as a room.
* [ ] Can i use the same redis instance for both pub/sub and cache?
* [ ] Websocket diagram.
* [ ] Deep-dive and scale.
