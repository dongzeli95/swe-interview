# Design Webhook

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

## Functional Requirement:

1. Customer could register multiple webhook
2. Verify ownership of webhook url
3. Security validation for webhook
4. Filtering by event type.
5. UI Visibility - delivery status: event type, failed\_reason, response.

## Non-functional Requirements:

1. Reliability - retry
2. Durability - don't lose event.
3. Security
4. Highly available

## Scale

read, write pattern? a lot of write.

How many users?&#x20;

## API

```
CRUD

POST /v1/webhook

GET /v1/webhook

PUT /v1/webhook

DELETE /v1/webhook
```

## Schema

```
User Table
Event Table

Webhook Table
{
  webhook_id
  owner_id
  event_type
  url
  secret_token
  created_at
  is_active: bool 
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

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

### E2E

1. Client register a webhook with a url
2. Webhook service send a validation request back to client's provided url.
3. After webhook url is verified, we store this information in DB.
4. Depending on triggering mechanism, we send sign the url and send webhook request with its payload to destination.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-24 at 9.01.58 AM.png" alt=""><figcaption></figcaption></figure>

## Deep Dive

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

### What happen if retry doesn't work? DLQ!

In SQS, if the configured maximum receive count for a message is reached without being successfully processed, SQS will move the message into a dead letter queue. We can investigate and fix issue and playback the messages later.



How to validate request is delivered to the right user?

1. Sign your request with secret token that able to be verified on user's side.

* User can create a secret token and store the token in a secure place.
* Validate webhook deliveries:
  * Create a hash signature that can be sent to client with each payload, like: X-Hub-Signature-256. Using HMAC hex digest.
  * Client can calculate a hash based on stored secret and then compare the hash with payload hash.

1. Make a ack protocol between you and client:

> _To acknowledge receipt of a webhook, your endpoint should return a 2xx HTTP status code. Any other information returned in the request headers or request body is ignored. All response codes outside this range, including 3xx codes, will indicate to Stripe that you did not receive the webhook. This does mean that a URL redirection or a “Not Modified” response will be treated as a failure._

Why we don't make web-hook call to customer directly?

1. Customer endpoint may fail, may timeout, may take a long time to respond.

why we need extra logging and monitoring?

Web-hook is hard to know where it failed, client won't be able to know. You will have to know.

### Segment different topics?

### Security issue?

1. Server side request forgery (SSRF) -> make sure customer don't abuse your internal network.
2. Set fixed set of proxies in order to get authenticated by other big company's firewall.

### Deliverability

Retry and scale?

Filter out event based on event types ana schema

Rate limit on outgoing webhooks.
