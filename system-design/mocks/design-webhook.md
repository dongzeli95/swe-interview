# Design Webhook

## Functional Requirement:

1. Retry make sure it delivers
2. Security, sign the request and timestamp
3. Fanout -> add multiple webhook url
4. Filtering by event type.
5. UI Visibility - delivery status: event type, failed\_reason, response.

<img src="../../.gitbook/assets/file.excalidraw (29).svg" alt="" class="gitbook-drawing">

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

