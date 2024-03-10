# Design Payment

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

