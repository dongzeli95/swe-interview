# Design Webhook

## Topics

1. How to handle failure?
2. How to do retry?
3. How to scale?
4. How to validate request is delivered to the right user?

## Functional Requirement:

1. Retry make sure it delivers
2. Security, sign the request and timestamp
3. Fanout -> add multiple webhook url
4. Filtering by event type.
5. UI Visibility - delivery status: event type, failed\_reason, response.

<img src="../../.gitbook/assets/file.excalidraw (29).svg" alt="" class="gitbook-drawing">

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-24 at 9.01.58 AM.png" alt=""><figcaption></figcaption></figure>

Why we don't make webhook call to customer directly?

1. Customer endpoint may fail, may timeout, may take a long time to responde.

why we need extra logging and monitoring?

Webhook is hard to know where it failed, client won't be able to know. You will have to know.

### Segment different topics?

### Security issue?

1. Server side request forgery (SSRF) -> make sure customer don't abuse your internal network.
2. Set fixed set of proxies in order to get authenticated by other big company's firewall.

### Deliverability

Retry and scale?

Filter out event based on event types ana schema

Rate limit on outgoing webhooks.

## Deep Dive

How to validate request is delivered to the right user?

1. Sign your request with secret token that able to be verified on user's side.

* User can create a secret token and store the token in a secure place.
* Validate webhook deliveries:
  * Create a hash signature that can be sent to client with each payload, like: X-Hub-Signature-256. Using HMAC hex digest.
  * Client can calculate a hash based on stored secret and then compare the hash with payload hash.

1. Make a ack protocol between you and client:

> _To acknowledge receipt of a webhook, your endpoint should return a 2xx HTTP status code. Any other information returned in the request headers or request body is ignored. All response codes outside this range, including 3xx codes, will indicate to Stripe that you did not receive the webhook. This does mean that a URL redirection or a “Not Modified” response will be treated as a failure._

