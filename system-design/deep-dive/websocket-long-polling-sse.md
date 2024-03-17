# Websocket / Long Polling / SSE

## Websocket

full-duplex communication channels over a single TCP connection. It's a persistent connection between client and server that both parties can use to start sending data at any time.

### Workflow:

1. Client initiates a websocket handshake process by sending a request.
2. The request contains an HTTP Upgrade header that allows the request to switch to websocket protocol ws:// or wss://
3. The server sends a response to the client, ack the websocket handshake request.&#x20;
4. A websocket connection will be opened once the client receives a successful handshake response.
5. Now the client and server can start sending data in both directions allowing real-time communication.
6. The connection is closed once server or client decides to close connection.

### Pros:

* Full-duplex async messaging.
* Better origin-based security model.
* Lightweight for both client and server.

### Cons:

* Terminated connections aren't automatically recovered.
* Older browsers don't support websocket. (less relevant)

## Long Polling

A technique used to push information to a client as soon as possible from the server.&#x20;

In long polling, the server does not close the connection once it receives a request from the client. Instead, the server responds only if any new message is available or timeout is reached.

<img src="../../.gitbook/assets/file.excalidraw (1) (1) (1).svg" alt="" class="gitbook-drawing">

### Workflow

1. The client makes an initial request and waits for a response.
2. The server receives the request and delays sending anything until update is available.
3. Once an update is available, the response is sent to the client.
4. The client receives the response and makes a new request immediately or after some defined interval to establish connection again.

### Pros:

* Easy to implement, good for small-scale projects.
* Nearly universally supported.

### Cons:

* Not scalable.
* Creates a new connection each time, which is intensive on server.
* Reliable message ordering can be issue for multiple requests.
  * If client has two browser tabs open consuming the same server resource, no guarantee that duplicate data won't be written more than once.
* Increased latency as server needs to wait for new request.

## SSE (Server-Sent Events)

Unidirectional, once client sends the request it can only receive the responses without the ability to send new requests over the same connection.

### Workflow

1. The client makes a request to server.
2. The connection between client and server is established and remains open.
3. The server sends responses or events to client when new data is available.

### Pros:

* Simple to implement and use for both client and server.
* Supported by most browsers.
* No trouble with firewalls.

### Cons:

* Unidirectional nature can be limiting.
* Limitation for max number of open connections.
* Does not support binary data.
