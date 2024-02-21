# Metrics monitoring and alert system

## Topics

1. How to collect the metrics data?
   1. Push or Pull, tradeoff?
2. How to transmit data from sources to monitoring system?
3. How to store incoming data?
4. How to do alert?
5. How to do visualization?
6. What's the read/write data access pattern?
7. What type of DB to use and the trade off?
8. How to scale when time-series DB is unavailable? Scale through Kafka.
   1. How to scale Kafka?
9. Data encoding and compression? Downsampling strategy?

## Functional Requirement

* can ingest large amount of metrics data points.
* can support various types of metrics: latency, QPS, CPU load, memory usage, disk space consumption etc.
* can show dashboard regarding specific metrics.
* can alert when specific metrics passes certain threshold.
* How long to keep data? 1 year
* resolution of metrics data:\
  Keep newly received data for 7 days. After 7 days, you roll them up to 1 minute resolution for 30 days. After 30 days, you roll them up at 1h resolution.
* support alert channels: Email, phone, PagerDuty, web-hooks.

## Non-functional Requirement

* Durable, metrics won't be lost.
* Highly available.
* Low Latency for dashboard and alerts.
* Flexibility: pipeline should be flexible enough to integrate new tech.

## Scale

100M DAU, 1000 server pools and 100 machines per pool.

I have 1000 server pods, 100 machines per pool, 100 metrics per machine => 10M metrics.

## API

1. LogCounter(scopes \[]string, int counter)
2. LogLatency(scopes \[]string, time duration)

## Data Schema

query pattern: constant heavy write load and read load is spiky.

time series DB, for example: InfluxDB and Prometheus.

cpu.load

<table><thead><tr><th width="365">metric_name</th><th>cpu.load</th></tr></thead><tbody><tr><td>labels</td><td>host:i631,env:prod</td></tr><tr><td>timestamp</td><td>1613707265</td></tr><tr><td>value</td><td>0.29</td></tr></tbody></table>

average cpu load.

| metric\_name | cpu.average.load                      |
| ------------ | ------------------------------------- |
| labels       | host:i631,env:prod                    |
| value\_list  | An array of \<value, timestamp> pairs |

Why not use SQL?

1. Relational DB is not optimized for operations like moving average.
2. Does not perform well under constant heavy write load.

Why not use NoSQL?

1. Require deep knowledge of internal workings to devise a scalable schema.

Why time series DB?

1. Can easily handle large amount of write requests. InfluxDB with 8 cores and 32 GB can handle over 250,000 writes per second.
2. Efficient aggregation and analysis of large amount of time-series data by label. Key is to make sure each label is of low cardinality (having small set of values).

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (10).svg" alt="" class="gitbook-drawing">

## E2E

Ingestion:

1. client emits metrics to call API Gateway after aggregation say every 5 seconds.
2. API Gateway aggregates metrics say every 1 mins
3. API forward requests onto ingestion service.
4. Ingestion service will further aggregate based on the needs and store the data onto time series DB.
5. After data is safely stored, we send the data onto Kafka topic.
6. Kafka topics are consumed by other services regarding alert system, email notification etc.

Serving:

1. Dashboard initiate request to gather datapoint for a specific timeframe and display those.
2. Dashboard client initiate and establish a web socket connection for changes regarding emitted metrics.
3. Serving backend pods establish web socket connection and fetch data from time series DB.
4. Whenever the metrics get updated from time series DB, backend pod will broadcast and publish updated data back to dashboard client using web socket connection.

## Deep Dive

### Push or Pull for metrics collector?

#### Pull

<img src="../../.gitbook/assets/file.excalidraw (11).svg" alt="" class="gitbook-drawing">

1. metrics collector fetch configuration metadata from service discovery. Metadata including: pulling interval, IP addresses, timeout and retry parameters etc
2. metrics collector pull metrics data via a pre-defined HTTP endpoint.
3. Optionally, metrics collector register a change event notification with service discovery to pull updates. or metrics collector can poll periodically.

For scale, we use consistent hashing to map every metrics source by its unique name in the hash ring.&#x20;

This ensure one metrics source server is handled by one collector only.

#### Push

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1) (1) (1) (1) (1) (1) (1).svg" alt="" class="gitbook-drawing">

Collection Agent exist within metrics source and aggregate metrics and push those periodically to metrics collector.

Example of pull architecture: Prometheus

Example of push architecture: Amazon CloudWatch, Graphite

|                    | Pull                                                                                                                               | Push                                                                                                         |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Easy debugging     | <mark style="background-color:green;">Pulling metrics can be viewed/tested any time.</mark>                                        |                                                                                                              |
| Health check       | <mark style="background-color:green;">Can quickly figure out if a monitored server is down.</mark>                                 | <mark style="background-color:red;">If collector doesn't receive metrics, it might be due to network.</mark> |
| Short-lived jobs   | <mark style="background-color:red;">Short-lived jobs don't last long enough to be pulled. Although we can use push gateway.</mark> |                                                                                                              |
| Firewall / network | <mark style="background-color:red;">Require more elaborate network infra.</mark>                                                   | <mark style="background-color:green;">Data can be received anywhere.</mark>                                  |
| Protocol           | HTTP / TCP                                                                                                                         | UDP                                                                                                          |
| Security           | Monitored servers are defined in config files in advance. Guaranteed to be authentic.                                              | Any client can send metrics. Can be fixed using whitelist or requiring authentication.                       |

### Scale

What happens if time-series database is unavailable?

Add Kafka between metrics collector and time DB. Then consumers or streming processing services such as Apache Storm, Flink, and Spark, process and push data to the time-series DB.

How to scale Kafka?

1. Configure number of partitions based on throughput requirements.
2. Partition metrics data by metrics name.
3. Partition metrics data with tags/labels.

### Downsampling

Downsampling is the process of converting high-resolution data to low-resolution to reduce overall disk usage.

Retention: 7 days, no sampling.

Retention: 30 days, downsample to 1 minute resolution

Retention: 1 year, downsample to 1 hour resolution.

### Alert system

<img src="../../.gitbook/assets/file.excalidraw (12).svg" alt="" class="gitbook-drawing">

1. Load config file(YAML) to cache servers.
2. Alert manager fetches alert configs from cache.
3. Based on config rules, alert manager calls query service at predefined interval. If the value violates threshold, an alert event is created.
   1. Filter, Merge and dedupe alerts.
   2. Retry: the alert manager checkes alert states and ensures a notification is sent at least once.
4. The alert store is KV DB, such as Cassandra, keep the state of all alerts: \
   inactive, pending, firing, resolved
5. Alerts are inserted into Kafka.
6. Alert consumers pull alert events from Kafka, process them and send notifications over different channels.
