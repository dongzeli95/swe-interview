# Top K / Ad Click Aggregation

Q:

1.  How are those ad click events stored and fetched?

    Log file located in different servers and events are append to the end of the file.&#x20;

```
ad_id, click_timestamp, user_id, ip, country
```

2. How much is the scale of the system? \
   1B ad clicks per day, 2M ads in total. Number of ad click events grows 30% year over year.
3. How often do we update it and how real time do we want the ad click report to be? Say an ad click is made 5 mins ago, how soon we want it to reflect in the aggregation?\
   A few minutes of end-to-end latency for ad click aggregation.\
   Real-time bidding less than a second.

## Functional Requirements:

1. Aggregate the number of clicks of ad\_id in the last M minutes.
2. Return the top 100 most clicked ad\_id every minute.
3. Support aggregation filtering by different attributes.

## Non-functional Requirements

1. Highly available
2. Highly scalable
3. Low latency, real-time experience
4. Properly handle delayed or duplicate events.

## Scale

1B users, 2 clicks a day = 2B clicks a day.

10^9\*2 / 10^5 = 2\*10^4 = 20000 QPS.

Peak ad click QPS = 20000 \* 5 = 100000 QPS

Assume a single ad click event occupies 0.1KB storage. Daily storage requirement is 0.1KB \* 1B = 100GB

## API

Aggregate the number of clicks of ad\_id in the last M minutes\
GET /v1/ads/{:ad\_id}/aggregated\_count

Return top N most clicked ad\_ids in the last M minutes\
GET /v1/ads/popular\_ads

## Data Schema

Raw data

<table><thead><tr><th width="95">ad_id</th><th width="159">click_timestamp</th><th width="149">user_id</th><th width="239">ip</th><th>country</th></tr></thead><tbody><tr><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>

Aggregated data

| ad\_id | click\_minute | count |
| ------ | ------------- | ----- |
|        |               |       |

Write load is heavy so use NoSQL like Cassandra or time series DB like influxDB

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (1).svg" alt="" class="gitbook-drawing">

## E2E

1. Log Watcher send logs to Kafka.
2. DB Writer pull logs from Kafka and store raw data to DB.
3. Aggregation service pulls commit offset from Kafka with micro-batch data.
4. Aggregation service aggregates the ad count using Flink.
5. Aggregation service fetches counter from Cassandra DB.
6. Aggregation service add the counter and update DB with latest result.
7. Aggregation service commit offset back to Kafka.

## Deep Dive

### How to make sure aggregated data are atomically committed?

Why do we need atomically committed?

If step 3 / 4 failed, the offset is not committed successfully back to Kafka, we would end up processing the same batch multiple times, leading over-counting data.

Solution, we store the Kafka offset as version for every Kafka partition within the DB, essentially making this process idempotent.

### Streaming vs Batching

<table><thead><tr><th width="172"></th><th width="143">Online Services</th><th width="203">Batch (Offline system)</th><th>Streaming (near real-time system)</th></tr></thead><tbody><tr><td>Responsiveness</td><td>Respond to client quickly</td><td>No response</td><td>No Response</td></tr><tr><td>Input</td><td>User requests</td><td>Bounded input with finite size.</td><td>Infinite streams</td></tr><tr><td>Output</td><td>Response</td><td>Aggregated Metrics / Materialized View</td><td>Aggregated Metrics / Materialized View</td></tr><tr><td>Performance measurement</td><td>Availability, latency</td><td>Throughput</td><td>Throughput, latency</td></tr><tr><td>Example</td><td>Online shopping</td><td>MapReduce</td><td>Flink</td></tr></tbody></table>

## Lamda vs Kappa

Lambda: A system that contains two processing paths (batch and streaming) simultaneously.

Kappa: A system that combines the batch and streaming in one processing path, the key idea is to handle both real-time data processing and continuous data reprocessing using a single stream processing engine. The difference is using a different input, input stream vs static raw data.

|             | Lambda               | Kappa                                                    |
| ----------- | -------------------- | -------------------------------------------------------- |
| Scalability | Scale independently  | Scale challenge when reprocessing large amounts of data. |
| Overhead    | Operational overhead | No operational overhead                                  |
|             |                      |                                                          |

### Data recalculation

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">
