---
description: https://www.uber.com/blog/real-time-exactly-once-ad-event-processing/
---

# Top K / Ad Click Aggregation

## Topics:

1. DB Choice: Pinot or Cassandra or BigData infra.
2. Raw data vs aggregated data?
3. Exact-once processing
4. Batch vs streaming
5. Kappa vs Lambda
6. How to manage aggregation window?
7. How to do recalculation and reconciliation?

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
4. Reliability - event cannot be lost.
5. Accuracy: exactly-once or idempotency.
6. Properly handle delayed or duplicate events.

## Scale

1B users, 2 clicks a day = 2B clicks a day.

10^9\*2 / 10^5 = 2\*10^4 = 20000 QPS.

Peak ad click QPS = 20000 \* 5 = 100000 QPS

Assume a single ad click event occupies 0.1KB storage. Daily storage requirement is 0.1KB \* 1B = 100GB

## API

Aggregate the number of clicks of ad\_id in the last M minutes

```
GET /v1/ads/{:ad_id}/aggregated_count

Request: json 
{
  from: start minute
  to: end minute
  filter: an identifier for different filtering strategy, filter = 001 filters out non-US clicks.
}

Response: {
  ad_id
  count
}
```

Return top N most clicked ad\_ids in the last M minutes

```
GET /v1/ads/popular_ads

Request: json
{
  topn: top n most clicked ads
  window: aggregation window size in minutes
  filter
}

Response {
  ad_ids: [] list of most clicked ads.
}
```

## Data Schema

Raw data

<table><thead><tr><th width="95">ad_id</th><th width="159">click_timestamp</th><th width="149">user_id</th><th width="239">ip</th><th>country</th></tr></thead><tbody><tr><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>

Aggregated data

| ad\_id | click\_minute | count |
| ------ | ------------- | ----- |
|        |               |       |

Support ad filtering we can add additional filter\_id to above table.

| filter\_id | region | ip   | user\_id |
| ---------- | ------ | ---- | -------- |
| 0012       | US     | 0012 | \*       |
|            |        |      |          |

Most clicked ads

| window\_size                        | updated\_at        | most\_clicked\_ads  |
| ----------------------------------- | ------------------ | ------------------- |
| The aggregation window size in mins | update time minute | most\_clicked\_ads: |
|                                     |                    |                     |

### Raw data vs Aggregated data

| Raw Data                                                                                                                                                                 | Aggregated Data                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| <ol><li><mark style="background-color:green;">Full Data set</mark></li><li><mark style="background-color:green;">Support data filter and recalculation.</mark></li></ol> | <mark style="background-color:red;">Data loss, this is derived data. 10 entries might aggregated to 1 entry.</mark>                             |
| <ol><li><mark style="background-color:red;">Huge data storage</mark></li><li><mark style="background-color:red;">Slow query</mark></li></ol>                             | <ol><li><mark style="background-color:green;">Smaller data set</mark></li><li><mark style="background-color:green;">Fast query</mark></li></ol> |
|                                                                                                                                                                          |                                                                                                                                                 |

We store both.

It's a good idea to keep raw data. If something goes wrong, we could use the raw data for debugging. If the aggregated data is corrupted due to a bad bug, we can recalculate the aggregated data from raw data.

Aggregated data should be stored as well. The raw data set is huge, the large size makes querying raw data very inefficient.&#x20;

We can also move old data to cold storage to reduce cost.

### DB Choice

Write load is heavy so use NoSQL like Cassandra or time series DB like influxDB

We can also consider to store ORC, parquet in S3/GCS and add hive metastore catalog on top of it. We can use query engine like Presto/BigQuery to query the result.

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

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

### Lambda vs Kappa

Lambda: A system that contains two processing paths (batch and streaming) simultaneously.

Kappa: A system that combines the batch and streaming in one processing path, the key idea is to handle both real-time data processing and continuous data reprocessing using a single stream processing engine. The difference is using a different input, input stream vs static raw data.

|             | Lambda               | Kappa                                                    |
| ----------- | -------------------- | -------------------------------------------------------- |
| Scalability | Scale independently  | Scale challenge when reprocessing large amounts of data. |
| Overhead    | Operational overhead | No operational overhead                                  |
|             |                      |                                                          |

### Data recalculation

<img src="../../.gitbook/assets/file.excalidraw (4).svg" alt="" class="gitbook-drawing">

### Time

Event time: when an ad click happens on client.

Processing time: system time of aggregation server that processes the click event.

|                 | Pros                                                                 | Cons                                                                                                                                                                 |
| --------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Event time      | More accurate because the client knows exactly when an ad is clicked | <p>It depends on timestamp generated on client-side. Clients might have the wrong time or generated by malicious users.<br><br>Have to deal with delayed events.</p> |
| Processing time | More reliable                                                        | Not accurate if event reaches system at much later time.                                                                                                             |
|                 |                                                                      |                                                                                                                                                                      |

#### Use both event time and processing time for more accurate time.

To adjust incorrect device clocks, one approach is to log three timestamps:

1. The time at which the event occurred, according to the device lock.
2. The time at which the event was sent to the server, according to device clock.
3. The time at which the event was received by the server, according to server clock.

offset = 3-2

real time = 1+offset

#### How we deal with delayed events?

1. Ignore straggler events. probably small percentage but can use metrics to track.
2. Publish a correction, an updated value for window with stragglers included.&#x20;
3. "watermark" method for an extended of aggregation window. The value of watermark depends on business requirement. Longer is more accurate but long latency.

#### Aggregation Window

1. Tumbling window

Fixed length. If you have a 1-minute tumbling window, all events between 10:03:00 and 10:03:59 will be grouped in one window, next window would be 10:04:00-10:04:59

2. Sliding window

Events that occur within some interval of each other. For example, a 5-minute sliding window would cover 10:03:39 and 10:08:12 because they are less than 4 minutes apart.

3. Hopping window

Fixed length, but allows windows to overlap in order to provide some smoothing. If you have a 5-minute window with a hop size of 1 minute, it would contain the events between 10:03:00 and 10:07:59, next window would cover 10:04:00-10:08:59

4. Session window

No fixed duration. All events for the same user, the window ends when the user has been inactive for some time (30 minutes). Common in website analytics

Tumbling window and sliding window is relevant in our problem.

**What's the diff between hopping window and sliding window?**

Hopping window uses a fixed window but sliding window only pop expired events out when they are far than the window designed.

### How to scale Kafka?

producer: don't limit the number of producer instances, this can be easily scaled.

consumer: rebalancing mechanism helps to scale consumers by adding or removing nodes.

Rebalancing can be slow, recommend to do during off-peak hours.

1. Hashing Key\
   Using ad\_id as hashing key for Kafka partition. Same ad on same partition.
2. Number of partition\
   Need to pre-allocate enough partitions in advance. If the partition changes, same ads maybe mapped into different partition.
3. Topics sharding\
   Shard the data by geography (topic\_north\_america, topic\_eu, topic\_asia etc) or by business type (topic\_web\_ads, topic\_mobile\_ads, etc)

Pros: more throughput, Cons: more complexity



### How to make sure downstream consumers also have exact-once guarantee?

We can introduce additional Kafka layer to publish on topics.

1. Producer: ack = all or ack = 1
2. Consumer: read\_committed for transaction
3. Use UUID for idempotency key.

## Appendix:

[Uber ad event processing architecture](https://www.uber.com/blog/real-time-exactly-once-ad-event-processing/)
