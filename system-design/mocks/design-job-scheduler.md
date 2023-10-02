---
description: Design a job scheduler that runs jobs at a scheduled interval.
---

# Design Job Scheduler

[Link](https://www.linkedin.com/pulse/system-design-distributed-job-scheduler-keep-simple-stupid-ismail/)

* Design a system for payment processing. (monthly/weekly/daily payout etc)
* Design a code deployment system.&#x20;

## Functional Requirements

1. **Submit task**: allow the user to submit their tasks for execution.
2. **Allocate resources**: allocate require resources to each task.
3. **Remove tasks**: should allow cancel submitted tasks.
4. **Monitor task execution**: should be adequately monitored and rescheduled if the task fails to execute.
5. **Show task status**: User can view the status of a executed job.
6. User can schedule a cron job with a schedule.
7. For scheduled jobs, user can limit its max concurrency.
8. Support different languages.

## Non-functional Requirement

1. Submitted job cannot be lost. Durability.
2. Availability.
3. Scalability: should be able to schedule and execute an ever-increasing number of tasks per day.
4. Reliability - retry
5. Efficient resource utilization.
6. **Release resources**: after executing a task, the system should take back resources assigned to the task.

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (8).svg" alt="" class="gitbook-drawing">

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

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

### Job Executor Flow

1. When a job is picked up from the queue, consumer's master updates JOB db attribution execution\_status = CLAIMED
2. When worker process picks up the work, it updates execution\_status = PROCESSING and continuously send health check to local DB.
3. Upon completion of a job, worker process will push the result inside S3, update JOB db execution\_status = COMPLETED and local db with the status.
4. Both worker processes and master will update the health check inside local database.
