---
description: Design a job scheduler that runs jobs at a scheduled interval.
---

# Design Job Scheduler

[Link](https://www.linkedin.com/pulse/system-design-distributed-job-scheduler-keep-simple-stupid-ismail/)

[Medium Link2](https://medium.com/@mesutpiskin/building-a-distributed-job-scheduler-for-microservices-8b7ab2ce5f91)

## Topics:

1. RDBMS vs NoSQL?
2. SQS vs Kafka?
3. How to handle at-least once?
4. How to make sure no concurrent worker working on same job? Task idempotency?
5. Execution Cap?
6. How to do prioritization? Using different queue?

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

&#x20;

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

## E2E

1. User submit/get job connecting to API Gateway.
2. Request get persisted in DB, acknowledgement get sent back to user.
3. Job executor service will continuously poll the due jobs from DB and insert entries into the queue.
4. Job executor service execute the business logic and update final result onto file system and update the status as COMPLETED.

## Data Schema

```
Job Execution Table (for quickly fetching jobs that needs to be executed)
next_execution
job_id
(job_id+next_execution_bucket) partiton key
created_at (sort key)

Job Table (for updating status and job details)
job_id (partition_key)
created_at (sort_key)
user_id
execution_cap
scheduling_type
total_attempts
script_path
resource_req {Basic, Regular, Premium}
status: {CLAIMED, PROCESSING, FAILED, SUCCEED}

Job History Table (for quickly lookup jobs history user executed)
user_id (partition_key)
created_at (sort_key)
job_id
retry_cnt
created
interval: 3hr, -1
```

| Column               | Datatype | Description                                                                                |
| -------------------- | -------- | ------------------------------------------------------------------------------------------ |
| TaskID               | String   | Uniquely identifies each task                                                              |
| UserID               | String   | UUID of user                                                                               |
| SchedulingType       | String   | {once, daily, weekly, monthly, anually}                                                    |
| TotalAttempts        | Integer  | maximum number of retries in case a task execution fails.                                  |
| ResourceRequirements | String   | {Basic, Regular, Premium}                                                                  |
| ExecutionCap         | Time     | maximum time allowed for task execution.                                                   |
| DelayTolerance       | Time     | indicates how much delay we can sustain before starting a task.                            |
| ScriptPath           | String   | The path of the script needs to be executed. The script is a file placed in a file system. |

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

1. When a job is picked up from the queue, consumer's master updates JOB db attribution execution\_status = CLAIMED.
2. When worker process picks up the work, it updates execution\_status = PROCESSING and continuously send health check to local DB.
3. Upon completion of a job, worker process will push the result inside S3, update JOB db execution\_status = COMPLETED and local db with the status.
4. Both worker processes and master will update the health check inside local database.
