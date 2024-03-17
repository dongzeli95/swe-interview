# Design Inventory

System Design：不是最常见的visa payment system, 而是inventory management, 设计当有客户，卖菜人，和买菜人同时需要更新菜的数量和买卖的情况。全程面试官毫无交流，感觉对墙说话。我每五分钟都停下来确认是不是再聊他想讨论的内容，面试官都是一句敷衍带过good good。最后草草收场去开别的会了。。



问如果做一个能显示各种category （food，clothes..）的页面, 然后点开每个category 的话还能显示sub- category，应该怎么设计database。感觉这里也答得一般



System Design： 是没见过的心题 ， 就算是老面镜题payment都不知道能不能过关。给我来了一个全新的题。 题目： 有用户， 有快递小哥， 有厂商， 围绕着从库里的库存 的数量，更新数据。 api要求返回在1s之内。 问了， 选什么database， 怎么monitor， single point failure有哪些 ‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌之前没怎么看system design， 属于半裸面。 真不敢相信自己真的就扯了1个小时。



shopping experience for customer

* retailer app check 库存 {商店, 商品, 薯量}
* customer app 架入 商品 {商店, 商品, 薯量，盯单}
* 跑腿小哥 checkout {商店, 商品, 薯量，盯单} 没什么特别好的想法，主要问了问库存怎么扣出‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌，怎么确认不超存量

{% embed url="https://www.1point3acres.com/bbs/thread-1025963-1-1.html" %}

## Questions:

1. How frequent does retailer update the inventory?

## Functional Requirement

1. Retailers are able to check inventory, add/update inventory, delete inventory...
2. Customers are able to check inventory, add item to cart and place an order.
3. Shopper can update, checkout order.

## Non-functional Requirement

1. Highly available - user will be able to do grocery shopping at any time.
2. Highly scalable - the system can handle large amount of read/write
3. Low latency
4. Consistency - If multiple users place orders on the same item, we need to accurately reflect on the item availability?

## Scale

How much scale we are looking at? and read:write ratio?

75k stores, 500M products on the shelves.

2M active users place multiple orders of tens of items in their cart every month.

600k Shoppers.

One month -> 10M order -> 10M / 30 = 0.3M order / day = 0.3\*10^6 / 10^5 = 15 QPS

15\*3 = 45 QPS for checkout validation requests.

### Data

75k store, 500M items, 200 locations

> On average a user will make 20 searches per basket before they checkout.

500\*10^6 / (75\*10^3) = 500/75\*10^3 = 10^4 items per store.

1 store -> items

> Retailer partners update inventory once a day for availability of all items on instacart.

> Despite estimation about availability, purchased items are not reserved until our shoppers pick them up in the store.



## API

```
Retailer
CRUD -> Update

Customer
CRUD order
get product item

Shopper
Get order
Update order: Mark item as found
Update Item: Mark not found.
```

## Data Schema

```
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
retailer_id
user_id,
created_at,
amount,
checkout_amount
status

Order Item Table
id (primary key)
order_id
retailer_id
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

Item Availability Table
retailer_id + item_id + date (composite primary key)
retailer_id
item_id
item_quantity,
version, (optimistic lock)
created_at,
updated_at

Item Table
id
retailer_id
item_name
item_price

User Table
id
phone
email
location
first_name
last_name

Question:
how to quickly update quantity for each product item?
is it necessary to keep a separate table for stock quantity?
```



## High Level Diagram

## Deep Dive

### How user make an order?

1. Create cart order
2. Fetch item availability from Cache.
3. Create order and order items.
4. After shopper update order item status:
   1. Fetch item availability and version number.
   2. Update Item Availability table with version number for optimistic lock.
   3. Update order item status.

### How to prevent the inconsistent state when updating inventory?

### Different shoppers

shopper1 and shopper2 both mark the same item as found in the same retail store, we might ended up with inaccurate quantity for item availability table.

> The isolation property in ACID means database transactions must complet their tasks independently from other transactions. So data changes made by transaction 1 are not visible to transaction 2 until transaction 1 is completed.

#### Option 1: Pessimistic Locking

Pessimistic concurrency control, prevents simultaneous updates by placing a lock on a record as soon as one user starts to update it. Other users who attempt to update the record have to wait until the first user has released the lock.

For MySQL:

```
SELECT ... FOR UPDATE
```

works by locking the rows returned by a selection query.&#x20;

Pros:

* Prevents applications from updating data that is being changed.
* Easy to implement and it avoids conflicts by serializing updates.
* Useful for write heavy application when data-contention is heavy.

Cons:

* Deadlocks may occur when multiple resources are locked. Writing deadlock-free application code could be challenging.
* If a transaction is locked for too long, other transactions cannot access the resource. This has a significant impact on database performance, especially when transactions are long lived.

#### Option 2: Optimistic Locking

Optimistic concurrency control, allows multiple concurrent users to attempt to update the same resource.

1. A new column called version is added to the database table.
2. Before a user modifies the database row, the application read the version number of the row.
3. When the user updates the row, the application increases the version number by 1 and write back to db.
4. A database validation check is put in place: the next version number should exceed the current version number by 1. Otherwise, validation fails and user tries again from step 2.

Pros:

* Prevents applications from updating stale data.
* We don't need to lock db resources. version number control is on application level.
* Optimistic lock is good when data-contention and concurrency is low.&#x20;

Cons:

* Poor performance when data contention is heavy.
* Why? \
  When there are a lot of shoppers try to mark the same grocery item, only one of them will succeed and the rest of client requests will have to retry.

#### Option 3: Database constraints

Similar to optimistic locking.

Instead of using is\_available, we can use availability initialized to 1, and we add the following DB constraint:

```
CONSTRAINT `check_availability` CHECK ( total inventory - total sold >= 0)
```

Pros:

* Easy to implement, works well when data contention is low.

Cons:

* The db constraint cannot be version controlled easily like application code.
* Not all db support constraints, if we do data migration in the future, it might cause problems.

### How to use cache?

### How to do DB sharding?

There are normally two ways we can scale the DB. Either we add replica or we shard the data.

* Add Read Replicas:

Pros:&#x20;

1. Can help ease up read load.

Cons:

1. Higher chance of change conflicts if user read stale data from version column within the table.

* Partition data into multiple databases

### What if data size is too large for a single database?

1. Move data to cold storage, for example item availability table from past dates.
2. Shard by retailer\_id

```
hash(retailer_id) % number of servers
```

Each retailer is unique and location-based, so we are effectively splitting request traffic from different retailers.



### How to show accurate item availability?

Ingesting scores generated by ML models into DB storage for fast and bulk retrieval. In both method, we store score in DB and update them to address low latency use cases.

1. Full sync

The ML availability scoring service updates a table multiple times a day in Snowflake with the refreshed availability score of items.  The DB ingestion workers read the snowflake table periodically and upsert the availability score for refreshed items to ensure no scores are stale.

2. Lazy Score Refresh

Scores are updated on demand based on an item appearing in the search results. The refresh activity happens in background jobs and used kinesis to aggregate the updates to DB.

<figure><img src="../../.gitbook/assets/Screenshot 2024-03-14 at 9.29.31 PM (1).png" alt=""><figcaption></figcaption></figure>

### Initial model for item availability

<figure><img src="../../.gitbook/assets/Screenshot 2024-03-14 at 9.33.06 PM.png" alt=""><figcaption></figcaption></figure>

### New Model

The new model combines three components for general, trending and real-time availability scores.&#x20;

* General Score: describes typical item availability patterns and is recalculated weekly.
* Trending Score: Quantifies short-term deciations from typical patterns and is recomputed daily or hourly.
* Real-time score: based on latest observations, use a event driven streaming achitecture that employs Kafka and Flink to deliver signals sourced from customer applications and retailer systems.

<figure><img src="../../.gitbook/assets/Screenshot 2024-03-14 at 9.39.33 PM.png" alt=""><figcaption></figcaption></figure>
