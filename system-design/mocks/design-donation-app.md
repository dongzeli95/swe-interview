# Design donation app

[https://docs.google.com/document/d/1GKo6-4u7BZNJhj\_gcMb9Vcxtb9Dx8reqwcA0bpZuXMg/edit](https://docs.google.com/document/d/1GKo6-4u7BZNJhj\_gcMb9Vcxtb9Dx8reqwcA0bpZuXMg/edit)

Say if DoorDash along with other partners across US is sponsoring for 3-day charity event where huge partipation of more than 3 million customers are expected to participant and simply donate money. You were responsible to design an app for this. How would you go about it?

Your app simply accept certain details like customer name, email address, credit/payment method details. You can assume DoorDash already has partnered with payment gateway to store the money collected from event, and transfer them back later.

## Topics

1. 用户余额100。用户在donate 100成功之后又donate100. 第二次donate应该是失败的。因为是async，如果我们向未及时sync的follower去query用户余额信息，仍然会返回用户余额100，可以继续donate。
2. 需不需要把钱先转到系统账户，最后选择直接转到charity账户
3. 需不需要exactly once 和idempotency, 面试官问我你怎么区别用户是刻意多次捐款还是错点。我说有两次点击，第二次只能点击一次，点多次肯定是错误点击
4. 我说如果按照charity\_id做sharding, 会有hot shard problem. 面试官反复问这个，说我们只有5k QPS.
5. SQL vs NOSQL
6. 问我为啥用message queue, 毕竟我们只有5k QPS, 我说有可能有traffic surge
7. 问我用哪种queue, 理由是什么。我说kafka, 我们可能要replay
8.  如果扣款失敗了？我們怎麼通知 User

    如果 PSP 中間一直沒有回應，我們怎麼確定 PSP 已經扣款但傳回來調包，還是根本 PSP 沒扣，我們是不是要用那個 nonce token 定義一個時間之後再去 Query & Update Status? 另外這種 payment service 如果搭 Kafka 一定要考慮到 broker 會突然壞的問題，所以這是為啥每個 Payment system 都會要去定義 retry queue & retryable classfication 去處理重試 （保證 at most once)，還有就是 Kakfa 是 log-based broker, 所以我們還是可以透過 persistent log 去做對帳還有偵測錯誤

## Functional Requirement

1. Customer can donate money.
2. Customer can check back on their donation amount.
3. Customer will be able to check total amount of donation so far.

## Non-functional requirement

1. Highly available
2. Low latency.
3. Reliable, fault tolerant. donation payment need to go through.
4. Consistency, user can see donation amount to be valid after they donate.
5. idempotency, no double payment.

