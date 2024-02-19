# Design ChatGPT

## Functional Requirement:

1. Create conversation
2. Send message
3. Delete conversation
4. Language preference?
5. Do we support images/attachment?
6. Thumb up/down?
7. Login system? Rate Limiting?
8. How about context window? In the conversation?

## Non-functional Requirement:

1. Low Latency
2. Highly available
3. Scalable

## Scale

10M user/day -> 5 conversations, 4 messages -> 200M messages per day.

200M messages -> 100 bytes -> 20G per day -> 73TB (10 years)



## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (25).svg" alt="" class="gitbook-drawing">

## GPT RLHF

### Fine tuning with RL

Proximal Policy Optimization

1. Policy is a language model that takes in a prompt and returns a sequence of text (just probability distributions over text)

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-19 at 9.24.28 AM.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-19 at 9.25.01 AM.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-19 at 9.26.54 AM.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-19 at 9.19.18 AM.png" alt=""><figcaption></figcaption></figure>
