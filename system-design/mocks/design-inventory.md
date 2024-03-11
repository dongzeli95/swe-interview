# Design Inventory

System Design：不是最常见的visa payment system, 而是inventory management, 设计当有客户，卖菜人，和买菜人同时需要更新菜的数量和买卖的情况。全程面试官毫无交流，感觉对墙说话。我每五分钟都停下来确认是不是再聊他想讨论的内容，面试官都是一句敷衍带过good good。最后草草收场去开别的会了。。



shopping experience for customer

* retailer app check 库存 {商店, 商品, 薯量}
* customer app 架入 商品 {商店, 商品, 薯量，盯单}
* 跑腿小哥 checkout {商店, 商品, 薯量，盯单} 没什么特别好的想法，主要问了问库存怎么扣出‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌，怎么确认不超存量

{% embed url="https://www.1point3acres.com/bbs/thread-1025963-1-1.html" %}

## Functional Requirement

1. Retailers are able to check inventory, add/update inventory, delete inventory...
2. Customers are able to check inventory, make an order on inventory.
3. Shopper can checkout on the order.

## Non-functional Requirement

1. Highly available
2. Highly scalable
3. Low latency
4. Consistency - if customer make an order, the items quatity need to be accurate?

## Scale

How much scale we are looking at? and read:write ratio?

75k stores, 500M products on the shelves.

2M active users place multiple orders of tens of items in their cart every month.

> Retailer partners update inventory once a day for availability of all items on instacart.

> Despite estimation about availability, purchased items are not reserved until our shoppers pick them up in the store.

## Data Schema

```
```
