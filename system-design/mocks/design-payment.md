# Validate Instacart Shopper Checkout

{% embed url="https://www.1point3acres.com/bbs/thread-764928-1-1.html" %}

{% embed url="https://www.1point3acres.com/bbs/thread-804726-1-1.html" %}

## Topics:

1. How to ensure system performs as expected? Monitoring?
2. If DB goes down, how do we respond within 1s?
3. Don't need replicas for DB? Because DB replicas will introduce inconsistencies, don't need the complexity?
4. How to approve incoming request if checkout balance is different than the order balance?
   1. The item price on Instacart is not update-to-date with item price in store.
   2. Shopper checkout the same order in multiple batches.
   3. For fruits like apple, the actual weight might fluctuate a bit, so the final amount is not exactly the same.
   4. Shopper has to replace similar item or marked some mising items.
5. SQL vs NoSQL?
   1. Transaction using SQL?
   2. Write throughput using Cassandra?
6. How to handle the case where shopper is picking up order in grocery stores which are not partnered with instacart?
7. What if grocery store doesn't have enough item, for example customer asked for 5 apples, shopper only found three.
8. Duplicate payment? idempotency?
9.  Four parties:

    1. customer
    2. shopper
    3. stripe
    4. visa payment (issuer)

    Instacart gives shopper credit.

Answer:

这轮面试官全程就按照手里的标准答案来，没有任何讨论空间，最后还特别虚伪地说I'm happy with the design，结果就秒拒了 T T 以下是我聊到或者面试官问到的点，大家可以参考着准备 physical infrastructure: server, storage, network data stores: SQL vs NoSQL data model: merchant, shopper, order, transaction (includes order id in transaction table) security: API token, pre-shared secret performance considerations: load balancer, data partition, write through cache of order table Monitoring: how to ensure the system performs expected? Testing & Deployment: Load testing etc Research & Analytics: how can data scientists leverage data for research? 尤其有两个特‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌匪夷所思的点： 如果database down了，如何确保在sla一秒内respond？这时直接approve，因为他们trust shoppers，认为fraud rate低 database不需要replica，面试官认为这个只会增加latency或者inconsistency，不值得有这个complexity



我觉得这个不是payment service 只需要考虑怎么approve incoming request 被问到一个单子分好几次买怎么办



设计题是payment verification，接收一个第三方服务的API，但是payload只有shopper\_id, amount (金额), merchant\_adddress，细节在于如何verify是一个valid payment，如果金额有微小差错怎么办，如果shopper买完发现忘记了什么东西再跑回去买怎么办。因为我个人比较偏重design，所以这轮感觉面的最好。适当提一下，所有payment相关的系统都要注意idempotency，以及verification的过程需要一个模糊估计，这个具体怎么实现见仁见智，可以考虑temporal locality，‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌地址的locality，如何进行fraud detection都可以谈，聊得比较愉快。



被问到了如何scale read/write request，SQL vs NoSQL的选择，有哪些关键metrics需要monitor，特别是availability如何monitor。确实没啥经验，尽量扯了。



第四轮，设计一个payment verification的服务器，接受的request是他们的第三方支付服务，形如{shipper\_id:1123, amount: 13.34, merchant: {addr: 123 ave, city: san jose\}} ，问如何在1sec之内，完成这笔交易的验证，并返回。     主要考察以下几点      1）performance      2) security      3) data model      4) data storage      5) stability/ fallover      问到一个小问题，shopper在刷信用卡时的金额和用户下订单的不是完全一致，比方说有10刀左右的误差，为什么。原因有二：1）instacart系统里面的价格和商店的标价没有实时一致，有滞后的情况。2）有些东西比如一斤苹果，买的时候重量有误差。然后追问，如何判断这个误差是正常的误差，还是shopp‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌er有欺诈。 我给的方案是，用历史数据作为判断依据。可以加一个async的服务，一旦交易完成，就记录下每个商品的误差，并且存到db里面。     还有问到db是被不同的service共享的，如何提高性能。加cache，怎么加cache，cache里面存放的啥，dump的策略是什么。我这个地方没有回答好。我最后还专门问了一下面试官。他说用write through的策略会简单有效，而且只用存放每个shopper最新的一个order的信息就好了。



总的流程应该就是顾客下单后，会有司机（shopper）接到通知，然后拿着公司的信用卡去店里面（比如说costco）购买物品，信用卡公司会找到胡萝卜来verify。但是后段怎么根据已有order来verify？Verify什么哪些方面？Verify之后还需要发生什‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌么事？（比如说如果你是顾客，下的单子应该有个status update之类的吧）还有就是什么样的DB table + schema可以用来支持你的design。准备的时候如果把整个流程都想通，这个问题就容易了。



* System design: instacart shopper payment system. 面试官比较关心怎么处理dupli‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌cate payment. 怎么保证SLO 1s RTT 99.9%.  我提出来他不应该set RTT, 因为你没法控制网络延迟.不过面试官好像不同意.



Design。还是经典原题，设计一个payment system，当有shopper刷卡的时候，如何判断是不是要通过这个刷卡请求。虽然面试问的是设计这个小的系统，但我觉得面试官看中的是这个小系统在整个大的系统里的位置，以及如何和大的系统里的其他部分进行沟通。我的建议是按照整个business flow，用breadth first search的方法，从用户下单开始，简单讲讲都会经历哪些component，最后是怎么到达payment system，payment system又需要和哪些其他的component进行交流。面试官会按照自己的喜好来让你深入聊聊某些具体的部分，有可能具体聊的部分不一定是payment system本身，而是一个和payme‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌nt system有联系的其他组件。总之就是先笼统的讲个bigger picture，然后跟着面试官的思路来深入，切记不要一下子就钻的太深。

感觉这道题的难点是AP‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌I design 以及 如何处理transaction error handling/rollback 和ACID compliance

考如何设计一个Shopper checkout系统。问了怎么authorize，设计data schema, 怎么scale，怎么保证idempotence，cache的选择，多个database怎么产生unique id。

应该主要focus on merchant和amount的verification service，而不用考虑其他像是Payment gateway或者PSP。感觉我刚开始说的时候有点偏题了。 被问的还是很细的，比如说什么是index，如何优化transactions的读，如何实现i‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌dempotent，如果同时收到两个request with different amount如何决定。。



面試官沒有貼上來 是用念給我聽 建議與面試官確定需求 我的面試官好像比較注重data base table設計 問了需要哪些table schema 怎麼設計 用sql or nosql, why? 資料很多怎麼增加performace cache, LB 基本問題 斷電 怎麼保證資料都有存好 怎麼確保刷兩次卡 只扣一次錢 怎麼確定shopper 買對的東西

* 如果shopper在不合作的店家買東西 怎麼handle
* 如果shopper分很多次完成訂單怎麼辦, order 10瓶牛奶,太重了 得分兩次刷卡 一次買五瓶
* 商場東西不夠了怎麼辦,order 要五個蘋果, shopper買3個, 買10個分別怎麼處理
* 如果 價格有誤差怎麼處理, costco說蘋果一個一塊 現場卻一個兩塊 可以多想一些case 準備資料

{% embed url="https://brandur.org/idempotency-keys" %}

{% embed url="https://link.1point3acres.com/?url=https%3A%2F%2Fblog.csdn.net%2Fdev_csdn%2Farticle%2Fdetails%2F78949203" %}

{% embed url="https://underhood.blog/uber-payments-platform" %}

<img src="../../.gitbook/assets/file.excalidraw (31).svg" alt="" class="gitbook-drawing">

At instacart, we have customers that place orders on our website, and we hire personal shoppers whose job it is ot go to grocery stores to fullfill those orders.

We give credit cards to our shoppers so they can purchase groceries for orders we've assigned them. Our servers receive an HTTP request from our payment processor every time a shopper swipes credit card that we give them. The payload looks like:

```
{
  shopper_id: 456,
  amount: 100.0,
  merchant: {
    name: "Safeway",
    address: "123 Main St",
  },
}
```

When we receive the HTTP request, we have to synchronously response within 1 second with a 200 OK to approve the transaction or 402 Payment Required to decline the transaction.

Say you are hired tomorrow, and you are leading the three person team in this room. How would you suggest we build the application that processes these requests? Some areas we should be sure to cover are physical infrastructure, data stores, data model, security, and performance considerations. For simiplicity, we should start off with the assumption that 1 shopper has just 1 order at 1 merchant.



## Questions:

1. Does this system need consistency guarantee?

**Atomicity**: This ensures that all parts of a transaction are completed successfully. If any part fails, the entire transaction is rolled back. In your system, this is critical when updating shopper balances. For example, when a payment is processed, you might need to update the shopper's balance and record the transaction simultaneously. If either operation fails, neither should be committed to avoid inconsistencies.

**Consistency**: This ensures that the database transitions from one valid state to another, maintaining all predefined rules. Your system likely has rules such as "balances cannot be negative" or "transactions must have valid shopper and merchant IDs." SQL databases enforce these rules consistently.

**Isolation**: In a system where multiple transactions occur simultaneously, isolation ensures that concurrent transactions do not affect each other's integrity. For instance, two shoppers making purchases at the same time should not impact each other's transactions or balances.

**Durability**: Once a transaction is committed, it is permanently recorded even in the event of a system failure. This is vital for financial transactions to ensure that every payment or balance update is permanently stored.

You may have to update multiple tables at once:

1. Create transaction record in transaction table.
2. Update order balance.
3. Update order status from Pickup -> Checked out.

## Clarifying Questions

1. Do we assume we have other services and db tables for: Shopper, Retailer, Order and User? Or we design everything from scratch.
2. Do we also check if credit card have sufficient balance? Or if shopper has a balance limit?

## Functional Requirement

1. Validate incoming checkout request

## Non-functional Requirement

1. Highly available
2. Highly scalable
3. Low latency < 1s
4. Durability, transaction record cannot be lost.
5. Consistency (ACID)

## Scale

75k stores, 500M products on the shelves.

2M active users place multiple orders of tens of items in their cart every month.

600k Shoppers.

One month -> 10M order -> 10M / 30 = 0.3M order / day = 0.3\*10^6 / 10^5 = 15 QPS

15\*3 = 45 QPS for checkout validation requests.

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (1) (1).svg" alt="" class="gitbook-drawing">

Single point of failures:

1. Checkout Service -> need load balancer in front of it, ideally we deploy it using Kubernetes and auto-scale based on traffic.
2. DB: We need cache for fast read query and also ease up on read request loads.
3. What if step 5 failed? How do we make sure the transaction record is persisted in DB and we update order balance and status accordingly.

<img src="../../.gitbook/assets/file.excalidraw (35).svg" alt="" class="gitbook-drawing">

## Data Schema

```
Transaction Table
id (primary key)
shopper_id (index)
order_id (index)
amount
retailer_name
retailer_address
validation_result: Failure, Accept, Reject
created_at

Shopper Table
id (primary key)
phone
email
zipcode
first_name
last_name

Order Table
id, (primary key)
shopper_id
user_id,
created_at,
balance,
checkout_balance,

Order Item Table
id (primary key)
order_id
item_id
item_name
item_quantity,
price,
status: PENDING/FOUND/REPLACED/NOT_FOUND
is_deleted,
updated_at

Retailer Table
id (primary key)
store_name
store_address
geo_hash
zipcode

User Table
```

## API

```
Validate payment request

POST v1/authorize
Request
JSON {
  shopper_id: 456,
  amount: 100.0,
  merchant: {
    name: "Safeway",
    address: "123 Main St",
  },
}

Response:
200 OK
402 Payment Required
400 Bad Request
500 Internal Server Errors
404 Not Found
429 Too Many Requests
```

## Deep Dive

### SQL vs NoSQL?

We need strong consistency guarantee, likely ACID properties supported by SQL can help handle that.

We can update multiple tables at once in a transaction to make sure they all succeed or nothing succeed.

### Kafka vs SQS?

Kafka

### Cache architecture?

Write through > Cache aside

Because checkout request are mostly one-time for a specific order. The cache-aside architecture can't optimize first-time read request. We need cache to be ready before this checkout request comes in.

So other services need to use write-through cache to update it before updating DB.

### Why Cache work?

1. Because we don't have high concurrency issues for same shopper credit card, so there won't be a case where the credit card balance is updated concurrently multiple times, leading to inconsistency issues.
2. Data is relatively small, because we only need to store the latest order for each shopper, likely TTL is within a couple hours and we can evict the record.

### Validate Logics?

* Shopper check

1. Check shopper exist and have an active order.

* Balance Check

1. Check the checkout amount doesn't exist shopper credit limit? (Cache this information from Stripe)
2. Check the amount is no more than the latest order total amount?
3. Check how much balance is allowed for single checkout?
4. If balance is different than order balance, we need to check if it's within a threshold, for example either smaller or larger within 20% of total amount is okay? This percentage threshold can be data derived using offline ML pipeline?

* Policy Check

1. Check store is in the right category for grocery.
2. Check location is in the proper radius within customer's location?
3. Check retailer store is in our partnered retailer list?

* Fraud Detection (offline)

### What if DB fails or Redis crashed?&#x20;

1. We can simply return "200" OK since we trust the shoppers and fraudulent rate is actually pretty low.
2. We can have fallback check mechanism to check on basic stuff without querying db or cache? For example, we can just check if balance is within a threshold? If timeout more than 1s, we just run fallback check and return.

### Fraudulent Prevention

Fraud detection:

We can do it based on ip address and historic data. It might involve complicated ML model detection and we can't do it in real-time. We can have an offline pipeline that does this to prevent future fraudulent activities.&#x20;

If we marked the fraudulent activity, we can notify third party payment gateway like stripe to froze the card, or reject the card later?

Fraudulent examples:

1. Shopper checked out in multiple different regions within a short time period.
2. Shopper checked out in a different region than previous checkouts?

### Monolithic vs Microservices?

### Payment and Ledger?

### Security compliances
