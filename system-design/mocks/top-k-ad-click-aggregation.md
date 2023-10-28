# Top K / Ad Click Aggregation

Q:

1.  How are those ad click events stored and fetched?

    Log file located in different servers and events are append to the end of the file.&#x20;

|   |   |   |
| - | - | - |
|   |   |   |
|   |   |   |
|   |   |   |

1. How much is the scale of the system?&#x20;
2. How often do we update it and how real time do we want the ad click report to be? Say an ad click is made 5 mins ago, how soon we want it to reflect in the aggregation?

## Functional Requirements:

1. Ingest and aggregate ad click events based on different time range.
2. Display ad click aggregation metrics.

## Non-functional Requirements

1. Highly available
2. Highly scalable
3. Low latency, real-time experience

## Scale

1B users, 2 clicks a day = 2B clicks a day.

10^9\*2 / 10^5 = 2\*10^4 = 2000 QPS.

## API

serving: GET /v1/campaign?id=xxx

ingestion: processAdsClick()&#x20;

## Data Schema

time series DB?

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">
