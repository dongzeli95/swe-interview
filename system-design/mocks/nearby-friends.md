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
* What search radius should we support?

## Non-functional Requirement

* Highly available
* Low latency
* Availability > consistency
* Read == Write

## Scale

1M active daily users. 10% use nearby friends 4 times a day.

0.4M / day = 0.4\*10^6 / 10^5 = 4 QPS.

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (2).svg" alt="" class="gitbook-drawing">

