# Back of Envelope

Back of envelope calculations is a technique used within software engineering to determine how a system should be designed. The method is most famous from big tech companies and is often expected in system design interviews. The thought is that you should first calculate some rough numbers so that it can drive decisions in designing possible solutions.

The following article lists various numbers at the time I did the research that I found useful for systems design, but is no longer being updated.

_**Note: All the numbers in this post are heavily rounded as their purpose is to give a rough guide for design decisions in the moment. You should always do more precise calculations before starting on a project/feature.**_

## Useful Calculations <a href="#7bae" id="7bae"></a>

**x Million users \* y KB = xy GB**\
example: 1M users \* a documents of 100KB per day = 100GB per day.

**x Million users \* y MB = xy TB**\
example: 200M users \* a short video of 2MB per day = 400TB per day.

**Byte Number Sizes**

The number of zeros after thousands increments by 3.

Thousands = KB (3 zeros)\
Millions = MB(6 zeros)\
Billions = GB (9 zeros)\
Trillions = TB (12 zeros)\
Quadrilions = PB (15 zeros)

### Byte Conversions <a href="#4da2" id="4da2"></a>

1B = 8bits\
1KB = 1000B\
1MB = 1000KB\
1GB = 1000MB

## Object Sizes <a href="#0cf4" id="0cf4"></a>

### Data <a href="#15d3" id="15d3"></a>

The numbers vary depending on the language and implementation.

* char: 1B (8 bits)
* char (Unicode): 2B (16 bits)
* Short: 2B (16 bits)
* Int: 4B (32 bits)
* Long: 8B (64 bits)
* UUID/GUID: 16B

### Objects <a href="#e6d9" id="e6d9"></a>

* File: 100 KB
* Web Page: 100 KB (not including images)
* Picture: 200 KB
* Short Posted Video: 2MB
* Steaming Video: 50MB per minute
* Long/Lat: 8B

### Lengths <a href="#01e4" id="01e4"></a>

* Maximum URL Size: \~2000 (depends on browser)
* ASCII charset: 128
* Unicode charset: 143, 859

## Per Period Numbers <a href="#9319" id="9319"></a>

The following numbers are heavily rounded and help determine how often something needs to happen over a period of time. For example, if a server has a million requests per day, it will need to handle 12 requests per second.

<figure><img src="https://miro.medium.com/v2/resize:fit:700/1*K158GR1W-DGmzf0LVHUXig.png" alt="" height="380" width="700"><figcaption><p>Heavily rounded per time period numbers.</p></figcaption></figure>

**More complex example:**

100M photos (200KB) are uploaded daily to a server.

* 100 (number of millions) \* 12 (the number per second for 1M) = 1200 uploads a second.
* 1200 (uploads) \* 200KB (size of photo) = 240MB per second.

The web servers will need to handle a network bandwidth of 240MB per second. You will therefore need a machine with high network performance to handle this bandwidth. In AWS this would translate to at least a m4.4xlarge, but it would be better to have multiple smaller servers to handle fault tolerance.

## Usage <a href="#6f75" id="6f75"></a>

### Users <a href="#63cb" id="63cb"></a>

* **Facebook:** 2.27B | **YouTube:** 2B | **Instagram:** 1B
* **Pinterest:** 332M | **Twitter:** 330M | **Onedrive:** 250M
* **TikTok:** 3.7M

### Visits <a href="#1a44" id="1a44"></a>

You can get a rough number of the visits a site gets at the [similarweb website](https://www.similarweb.com/website/johnlewis.com/#overview).

* **Facebook:** 26.12B | **Twitter:** 6.34B | **Pinterest:** 1.32B
* **Spotify:** 293M | **Ikea:** 233M | **Nike:** 110M
* **Argos:** 54M | **John Lewis:** 37M |**Superdry:** 3.5M
* **Virgin Money:** 1.8M | **Aviva:** 1.61M

## Cost of Operations <a href="#2fc3" id="2fc3"></a>

* **Read sequentially from HDD:** 30 MB/s
* **Read sequentially from SSD:** 1 GB/s
* **Read sequentially from memory:** 4 GB/s
* **Read sequentially from 1Gbps Ethernet:** 100MB/s
* **Cross continental network:** 6–7 world-wide round trips per second.

## Systems <a href="#d4a5" id="d4a5"></a>

These are not exact numbers, which very much depend on the implementation and what is hosting the service. The purpose of the numbers is to have a general idea of the performance across different types of services.

### SQL Databases <a href="#f30a" id="f30a"></a>

* **Storage:** 60TB
* **Connections:** 30K
* **Requests:** 25K per second

### Cache <a href="#82f8" id="82f8"></a>

\[[Redis — Requests](https://redis.io/topics/benchmarks)]\[[Redis — connections](https://redis.io/topics/clients)]

* **Storage:** 300 GB
* **Connections:** 10k
* **Requests:** 100k per second

### Web Servers <a href="#09ca" id="09ca"></a>

* **Requests:** 5–10k requests per second

### Queues/Streams <a href="#af91" id="af91"></a>

\[[Pub/Sub — limits](https://cloud.google.com/pubsub/quotas)]\[[Kinesis — limits](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html)]\[[SQS — limits](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)]

* **Requests:** 1000–3000 requests/s
* **Throughput:** 1MB-50MB/s (Write) / 2MB-100MB/s (Read)

### Scrapers <a href="#6568" id="6568"></a>

\[[Colly — go scraper](https://github.com/gocolly/colly)]

* **Requests:** 1000 per second
