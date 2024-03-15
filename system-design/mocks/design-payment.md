# Design Payment

Design。还是经典原题，设计一个payment system，当有shopper刷卡的时候，如何判断是不是要通过这个刷卡请求。虽然面试问的是设计这个小的系统，但我觉得面试官看中的是这个小系统在整个大的系统里的位置，以及如何和大的系统里的其他部分进行沟通。我的建议是按照整个business flow，用breadth first search的方法，从用户下单开始，简单讲讲都会经历哪些component，最后是怎么到达payment system，payment system又需要和哪些其他的component进行交流。面试官会按照自己的喜好来让你深入聊聊某些具体的部分，有可能具体聊的部分不一定是payment system本身，而是一个和payme‍‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‌‌nt system有联系的其他组件。总之就是先笼统的讲个bigger picture，然后跟着面试官的思路来深入，切记不要一下子就钻的太深。

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



## Why Deny?

1. Balance not correct?
   1. whether shopper replaced an item?
   2. whether shopper marked any item not found?
2. Geo location is too far, not possible?
3. Shopper does not exist?
4. Shopper does exist but duplicate requests?

