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

<img src="../../.gitbook/assets/file.excalidraw (2).svg" alt="" class="gitbook-drawing">

## FAQ

* [ ] Why not use socketio room with certain geo\_locations? And when user comes in, we just check see if this person A and person B's friend? What's the pros and cons of this way vs using each user as a room.
* [ ] Can i use the same redis instance for both pub/sub and cache?
