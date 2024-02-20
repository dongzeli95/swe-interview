# Design Chat App (WhatsApp)

## Topics:

1. Pros and cons of HTTP vs Websocket
2. How to scale Redis Pub/Sub?
3. How to guarantee message delivery?
4. What DB to use and why?

## Functional Requirement

1. User can send message, receive message.
2. User can join group chat.
3. Message delivery acknowledgement: sent, delivered and read.
4. Push notification

### Optional:

1. Do we support sending images/files?
2. Do we support recall a message?
3. Do we support group chat?
4. How to add friends?

## Non-functional requirement

1. Low latency
2. Highly available
3. Consistency: messages should be delivered in the order they were sent. Users must see the same chat history on all devices.

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (26).svg" alt="" class="gitbook-drawing">

### E2E

1. User A and user B create communication between clients.
2. User A send a message to chat server.
3. Chat server acknowledge back to user A
4. Chat server sends the message to user B and stores message in the DB.
5. User B sends an acknowledgement to chat server.
6. Chat server notifies user A message has been successfully delivered.
7. When user B reads the message, application notifies user A that B has read the message.

## API

### HTTP

Remove a conversation

```
v1/conversation?id=xxx DELETE
response: 201 status
```

View conversation history

```
v1/conversation?uid=xxx GET
response {
  "conversations": [
    "ConversationId1": {
      RecipientName string,
      RecipientProfilePic string,
      LatestMessage string,
    },
    "ConversationId2": {},
    ...
  ],
  "page_size": 10,
  "page_number": 1,
}
```

Get conversation Detail

```
v1/conversation/conversation_id/details?uid=xxx
response {
  "messages": [
    "UserA": "text1",
    "UserB": "text2",
    "UserA": "text1",
  ]
}
```

Get Friends List

```
v1/friends?uid=xxx GET
```

### WebSocket

Create a conversation

```
/connect 
join(room, channel="xxx")
request: uid, recipient_id
response: emit("conversation created", channel="xxx", to=uid)
```

Send message

```
/send
request: uid, room_id, message, type?, media_object?, document?
response: emit("message sent", channel="xxx", to=uid)
```

Acknowledgement Handler on client

```
socketio.on("ack") {

}
```

## Data Schema

Message Table

```
Message {
  uid
  sender
  receiver
  conversation_id
  status: SENT, READ, RECEIVED, RECALLED
  created_at
  is_deleted
}
```

User Table

```
User {
  uid
  handle
  profile_pic
  bio
}
```

Conversation Table

```
Conversation {
  id: uuid
  members: []string
  message_ids: []string
  owner
}

UserConversation {
  uid
  conversation_id
}
```

## Scale

2B users, 100B messages per day.

<mark style="color:purple;">QPS</mark>: 100\*10^9 / 10^5 = 100\*10^4 = 1M QPS.

<mark style="color:purple;">Storage:</mark>

100 bytes for a message

100B\*100B = 10^13B = 10^10KB = 10^7MB = 10TB per day

We keep messages for 30 days = 300 TB per month.

<mark style="color:purple;">Bandwidth:</mark>

10TB / 10^5 = 10\*1000\*1000MB / 10^5 = 1000MB / second

<mark style="color:purple;">Number of servers:</mark>

WhatsApp handles 10M connections on a single server

2B / 10M = 200 servers

<img src="../../.gitbook/assets/file.excalidraw (27).svg" alt="" class="gitbook-drawing">

## How to scale Redis Pub/Sub?

Modern Redis server capability:

100GB memory, gigabit network handle about 100,000 subscribers push.

max 10k connections.

1M QPS / 10^5 = 10 Redis.

2B Users -> 20B channels \* 20 bytes = 400\*10^9 bytes / GB = 400 GB

We need 4 Redis servers with each Redis server has 100GB.

