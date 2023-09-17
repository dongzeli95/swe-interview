---
description: Design a job scheduler that runs jobs at a scheduled interval.
---

# Design Job Scheduler

[Link](https://www.linkedin.com/pulse/system-design-distributed-job-scheduler-keep-simple-stupid-ismail/)

* Design a system for payment processing. (monthly/weekly/daily payout etc)
* Design a code deployment system.&#x20;

## Functional Requirements

1. User can schedule a task one time with retry.
2. User can schedule a cron job with a schedule.
3. User can view the status of a executed job.
4. For scheduled jobs, user can limit its max concurrency.
5. Support different languages.

## Non-functional Requirement

1. Submitted job cannot be lost. Durability.
2. Availability.
3. Reliability - retry

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (8).svg" alt="" class="gitbook-drawing">

## E2E

1. User submit/get job connecting to API Gateway.
2. Request get persisted in DB, acknowledgement get sent back to user.
3. Job executor service will continuously poll the due jobs from DB and insert entries into the queue.
4. Job executor service execute the business logic and update final result onto file system and update the status as COMPLETED.

## Deep Dive

### Job Scheduling Flow

1. Every X minute, the master node creates an authoritative UNIX timestamp and assigns a shard\_id and schedule\_job\_execution\_time to each worker.
2. Worker node will execute DB query and push jobs inside the Kafka queue for execution.

```
SELECT * FROM ScheduledJob WHERE scheduled_job_execution_time == now() -X and shard_id = 1

SELECT * FROM ScheduledJob WHERE scheduled_job_execution_time == now() - X and shard_id = 2
```

### Fault-tolerance

* Master monitors health of workers and knows which worker is dead and how to re-assign the query to new worker
* If master dies, we can allocate other worker node as master. (Automatic fail-over)
* Introduce a local DB to track the status if worker has queries the DB and put the entry inside queue.
