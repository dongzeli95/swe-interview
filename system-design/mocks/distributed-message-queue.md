# Distributed Message Queue

## Functional Requirement

* Able to send task to message queue and get immediate response. (producer)
* Able to subscribe and fetch task from message queue. (consumer)
* Support topic?
* Support ordering?
* Delivery guarantee?

## Non-functional Requirement

* Highly available
* Low latency
* Durable, message should not be missed.

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
