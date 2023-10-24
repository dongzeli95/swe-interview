# Metrics monitoring and alert system

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

time series.

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

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

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

### Data granularity (10m, 20m, 1h, 2days, 1month etc)
