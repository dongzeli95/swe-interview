# Design Webhook

## [Webhook from hookdeck](https://hookdeck.com/webhooks/guides/webhook-infrastructure-requirements-and-architecture)

## [Retry from Uber](https://www.uber.com/blog/reliable-reprocessing/)

## Topics

1. How to handle failure?
2. How to do retry?
3. How to scale?
4. How to validate webhook url ownership?
5. How to make sure webhook request are secure?
6. Rate limiting and VPC before sending the request?
7. Why to use Kafka vs SQS? Pros and Cons?
8. How to filter different event types, can we use Topic from Kafka?

## Qs:

1. What delivery semantic do we provide?&#x20;
   1. At least once
   2. At most once
   3. Exactly once
2. If we resend webhook, could we assume the endpoint to be idempotent?
3. Are we designing 1st party webhooks or 3rd party webhooks? This is critical since it determines the webhook triggering mechanism. If can be either triggered by us, or triggered by our client.
4. Do we support canceling the webhook?

## Functional Requirement:

1. Customer could register multiple webhook
2. Verify ownership of webhook url
3. Security validation for webhook
4. Filtering by event type.
5. Rate limiting to consumers.
6. UI Visibility - delivery status: event type, failed\_reason, response.

## Non-functional Requirements:

1. Reliability - retry
2. Durability - don't lose event.
3. Security
4. Highly available

## Scale

read, write pattern? a lot of write.

How many users?&#x20;

## API

<pre><code>CRUD

POST /v1/webhook
Request
{
  user_id
  event_type,
  secret_token,
  destination_url,
  payload JSON,
}

Response:
201 status code
json {
  "id": "webhook_id"
}

GET 
/v1/webhook?user_id=xxx
Request {
  page_number,
  page_size,
}

Response {
  webhook_list: [
    {
      webhook_id,
      destination_url,
      status,
      created_at,
    },
    {
      webhook_id,
      destination_url,
      status,
      created_at,
    }
    ...
  ],
}


GET <a data-footnote-ref href="#user-content-fn-1">/v1/webhook?id=xxx</a>
Response: {
  id,
  user_id,
  status,
}

DELETE /v1/webhook (cancel a webhook)
</code></pre>

## Schema

```
User Table
Event Table

Webhook Table
{
  webhook_id (partition key)
  owner_id
  event_type
  destination_url
  secret_token
  created_at (sort key)
  is_active: bool
  status: PENDING, SUCCEED, FAILED
}

User Webhook Table
{
  webhook_id
  owner_id + time bucket(partition key)
  event_type
  destination_url
  secret_token
  created_at (sort key)
  is_active: bool
  status: PENDING, SUCCEED, FAILED
}

WebhookTask Table
{
  task_id
  webhook_id
  payload: JSON
  status: PENDING, SUCCEED, FAILED
}
```

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (29).svg" alt="Initial Approach without MQ" class="gitbook-drawing">

<img src="../../.gitbook/assets/file.excalidraw (2).svg" alt="" class="gitbook-drawing">

<img src="../../.gitbook/assets/file.excalidraw (1) (1).svg" alt="" class="gitbook-drawing">

### E2E

1. Client register a webhook with a url
2. Webhook service send a validation request back to client's provided url.
3. After webhook url is verified, we store this information in DB.
4. Depending on triggering mechanism, we send sign the url and send webhook request with its payload to destination.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-24 at 9.01.58 AM.png" alt=""><figcaption></figcaption></figure>

## Deep Dive

### How to make sure request succeed?

Make a ack protocol between you and client:

> _To acknowledge receipt of a webhook, your endpoint should return a 2xx HTTP status code. Any other information returned in the request headers or request body is ignored. All response codes outside this range, including 3xx codes, will indicate to Stripe that you did not receive the webhook. This does mean that a URL redirection or a “Not Modified” response will be treated as a failure._

### How to handle failure?

Consumer APIs may fail, may timeout, in order to make sure the webhook is sent successfully at least once, we introduces message queue in the middle to decouple the webhook delivery with webhook registration process.&#x20;

#### Benefits:

1. We have retry support, if consumer API timeout or fail, we can reprocess the task again later.
2. Webhook registration service doesn't have to wait for the webhook task to be delivered in order to register next webhook.
3. If there are traffic burst, message queue can help smoothen out the load such that workers are not overwhelmed, and we can scale up number of workers to  catch up on consumption speed.

### How to do retry?

Depending on which message queue we are using, there are different mechanisms.&#x20;

For traditional message queue like SQS, if the task failed to process for whatever reason, the worker don't acknowledge the message within the visibility timeout period, SQS assumes the message processing failed, and other worker will be able to see this task again for retry.&#x20;

For Kafka, the worker only commit offset after the task is successfully processed. So if consumer worker dead, some other consumer will be able to start processing from the previous commit offset which will ensure the retry.

We can handle errors with exponential backoff. Each request that results in a non-200 response code or time out will be re-attempted over the course of 10 minutes. Client can see the error in the console UI.

### What's wrong with simple retries?

<figure><img src="../../.gitbook/assets/Screenshot 2024-03-08 at 8.59.51 AM.png" alt=""><figcaption></figcaption></figure>

* Clogged batch processing \
  When we are required to process a large number of messages in real time, repeatedly failed messages can clog batch processing.&#x20;

We can use separate retry queues to insert failed messages and a separate set of retry consumers can pick up and do the retry. We commit offset in the original topic to unblock the process. For retry queues, we can add several layers. When the handler of a particular topic returns an error response for a given message, it will publish that message onto next retry topic. We use DLQ as the end of line Kafka topic.&#x20;

We can replay dead letter messages by publishing them back to first retry topic.

For each subsequent level of retry consumers, we can enforce a processing delay.

#### Pros:

* Unblock batch processing
* We can decouple message into granular steps and only retry some of the step. Say the message succeeded in step 1 and failed at step 2, we only publish step2 portion of the job onto retry topic.
* Observability is better, we have a easy tracing of errored message's path. When and how many times the message has been retried. We can monitor the rate of production into original processing topic versus those of retry topic and DLQ to inform thresholds for automated alerts.

### How to verify webhook url ownership?

Send a request to client webhook url served as a verification request.

The verification request will be a GET request with a challenge parameter, which is a random string.

```
https://www.example.com/webhook?challenge=xxxx
```

client app should echo back the challenge parameter as the body of its response. Once we receives a valid response, the endpoint is considered a valid webhook, we can start sending notifications to those urls.&#x20;

client app have ten seconds to responde to the verification request. We will not perform automatic retry for verficiation requests.

How to make sure webhook request are secure?

### How to make sure webhook request are secure?

#### Basic Authentication

```
Authorization: Basic {base64(username:password)
```

1. The developer of the destination application submits their username and password to webhook provider.
2. Provider first sends a request with no Authorization header. The request is rejected with 401 and destination point sends back an authentication challenge using WWW-Authenticate header.
3. Producer combine username and password and send base64 version.
4. Destination endpoint receives the authenticated request, verify the credentials and if valid, allows the webhook.

#### Signature Verification

1. A secret key is known by both webhook producer and consumer.
2. When sending webhook, producer uses this key and cryptographic algorithms like HMAC to create cryptographic hash of the webhook payload.
3. The signature is sent in a custom header along with the webhook request. The type of algorithm used sometimes is also sent.

```
X-Hub-Signature-256. Using HMAC hex digest.
```

1. When webhook arrives at webhook URL, the receiving application takes the webhook payload and uses the secret key and cryptographic algorithm the calculate the signature.
2. The calculated signature is then compared with that sent by producer in the custom header. If there is a match then the request is valid.

#### Prevent Replay attack

A reply attack occurs when an attacker gets hold of an authenticated request and repeats it, thereby causing duplicated webhooks.

To prevent replay attacks, signature verification allows you to add a timestamp that can be used to expire webhook after a certain period of time, ex: 2 mins. This time can be adjusted based on security requirements.

When webhook hits the webhook URL, it's checked against current time to see if it's still valid for use. If timestamp is too old, webhook is rejected.

### What happen if retry doesn't work?

#### If issue comes from our end?

In SQS, if the configured maximum receive count for a message is reached without being successfully processed, SQS will move the message into a dead letter queue. We can investigate and fix issue and playback the messages later.

#### If issue comes from client end?

If client webhook url returns more than a percentage of errors in the past 10 minutes, or 5% failure rate.  We can disable client's webhook and notify them through email. They can re-enable their webhook in console UI.

### How to scale?

1. Do load test to figure out the bottleneck.

#### Potential bottlenecks:

* API/Webhook delivery servers: deploy on k8s and use auto scale.
* Cassandra DB: figure out partition key and sort key to do partition and increase on write throughput?
* Kafka: Add more specific topics and more partitions within the topic.

### Why we need extra logging and monitoring?

Web-hook is hard to know where it failed, client won't be able to know. You will have to know.

### Security issue?

1. Server side request forgery (SSRF) -> make sure customer don't abuse your internal network.
2. Set fixed set of proxies in order to get authenticated by other big company's firewall.

### Deliverability

Filter out event based on event types ana schema

Rate limit on outgoing webhooks.

[^1]: 
