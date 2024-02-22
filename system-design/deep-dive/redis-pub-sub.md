# Redis Pub/Sub

## Memory

A modern server can have 100GB memory.

## CPU

A modern server with gigabit network can handle about 100k subscriber pushes.

## Distributed Redis Pub/Sub cluster

We need service discovery component to our design, with etcd, ZooKeeper.&#x20;

1. The ability to keep a list of servers in service discovery component.

```
Key: /config/pub_sub_ring
Value: ["p_1", "p_2", ...], a list of pubsub servers.
```

2. The ability for clients (websocket servers) to subscribe any updates to the pubsub server.

Given a channel, we need to check with service discovery to find the redis server.

<img src="../../.gitbook/assets/file.excalidraw (1) (1).svg" alt="" class="gitbook-drawing">

ps2 server consists of channel1 and channel2.

### Flow

1. The websocket server consults the hash ring to determine Redis Pub/Sub server to write to. Websocket server could cache a copy of hash ring in memory. The websocket subscribe to any updates on hash ring to get local copy updated.
2. Websocket server publishes the update to user's channel in that Redis Pub/Sub server.

## Scaling Operations

Redis Pub/Sub servers are stateful because they store channel information about subscriber list.

If a new Pub/Sub server is added or old one is removed, subscribers to the moved channel must know about it to resubscribe.

#### Issues:

1. When we resize the cluster, channels need to move onto different Pub/Sub servers. This behavior will generate a ton of resubscription requests.
2. During resubscription, subscriber pushes might be missed.  We should resize cluster when usage is at its lowest during the day.

#### Steps to resize?

1. Determine the new ring size, provision new server or remove old ones.
2. Update keys of hash ring in service discovery.
3. Monitor dashboard and see spikes in CPU usage in websocket servers for resubscription.

#### What if a pub/sub server goes down?

1. We need monitoring to alert on-call operator to update hash ring key to replace dead node with a fresh Redis node.&#x20;
2. Websocket server are notified about the update and each one notifies its connection handler to re-subscribe to the channels on new Pub/Sub server.
