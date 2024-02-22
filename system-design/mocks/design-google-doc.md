# Design Google Doc

## Topics:

1. How to allow concurrent editing from multiple users?
2. How to detect and merge editing conflicts?
3. How to store the data?
4. How to guarantee the delivery of the editing changes from other users?

## Functional Requirement

1. User can create a google doc and share it
2. Multiple users can edit the document.
3. User can revisit a document.
4. User can comment on document? (optional)

## Non-functional Requirement

1. Editing changes from other user are rendered in real-time.
2. Low latency
3. Highly available
4. Fault tolerant.

## High Level Architecture

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

## API

CRUD

```
1. Create Document
v1/document POST
json payload {
  uid,
  id,
  folder_id,
  access,
}

Response: 201 OK

2. View Document
v1/document?id=xxx GET
Response {
  id,
  content,
  users,
  users_cursor_pos: {
    'user1': {
      'col': xx,
      'row': xx,
    }
  },
  user_access,
}

3. Share Document
v1/document/#id/share GET
Response {
  "url": ""
}

4. Edit Document
v1/document?id=xxx PUT
Request {
  uid,
  starting_pos_row,
  starting_pos_col,
  text,
}

Response: 200 OK

5. Delete Document
v1/document DELETE

Websocket API
/connect
Request data: uid, document_id

/edit
Request data: uid, document_id, pos_row, pos_col, text

Websocket client handlers:
socket.on("/edit") {
  changes = data.changes;
  
}
```

## Data Schema

```
User Table
{
  uid,
  password,
  email,
  profile_pic,
}

Document Table
{
  id,
  owner,
  user_access: string[],
  created_at,
  is_deleted,
}

Edit Table
{
  id,
  uid,
  pos_row,
  pos_col,
  text,
  created_at,
  screenshot,
}
```

## Scale

DAU: 1B users. 10 write, 10 read

QPS: 1B\*10 / 10^5 = 100k

Storage: 2\*365\*1B\*100kb = 800\*10^11kb = 8\*10^13kb = 20PB / year.

## Final Diagram

<img src="../../.gitbook/assets/file.excalidraw (28).svg" alt="" class="gitbook-drawing">

## What DB to use?

For editing table, we need db that optimize for write requests: Cassandra

Edit table: doc\_id + timestamp bucket as primary key, message\_id as the partition key.

## How to merge conflicts?

### How we get the conflict?

1. Operational Transformation (OT)

A technique that's widely used for conflict resolution in collaborative editing. It's a lock-free and non-blocking approach for conflict resolution. If operations between collaborators conflict, OT resolves conflicts and pushes the correct converged state to end users. As a result, OT provides consistency for users.

Features

1. Causality preservation (order): If operation a happened before operation b, then operation a is executed before operation b.
2. Convergence: All document replicas at different clients will eventually be identical.

Cons:

* Each operation to characters may require changes to the positional index. Operations are <mark style="color:red;">order dependent</mark> on each other.
* It's challenging to develop and implement from scratch.

2. Conflict-free Replicated Data Type (CRDT)

The conflict-free replicated data type (CRDT) was developed in an effort to improve OT.&#x20;

a family of data structures for sets, maps, ordered lists, counters that can be concurrently edited by multiple users, which automatically resolve conflicts in sensible ways. CRDTs have been implemented in Riak 2.0.

1. It assigns a global unique identity to each character.
2. It globally orders each character.



| Data            | Explanation                         | Example |
| --------------- | ----------------------------------- | ------- |
| DocumentID      | UUID                                |         |
| DocumentCounter | The sequence of operations in a doc | 87      |
| Value           | Value of character                  | "A"     |
| PositionalIndex | unique position, can be float       | 4.5     |

The example below depicts that a user from site ID `123e4567-e89b-12d3` is inserting a character with a value of `A` at a `PositionalIndex` of `1.5`. Although a new character is added, the positional indexes of existing characters are preserved using fractional indices. Therefore, the order dependency between operations is avoided. As shown below, an `insert()` between `O` and `T` didn’t affect the position of `T`.

Cons: [https://core.ac.uk/download/pdf/189163265.pdf](https://core.ac.uk/download/pdf/189163265.pdf)

* There are interleaving anomalies.

3. Lock

Locks require us to segment documents into small sections where user could lock a portion and edit it. This will help developers come up with easy solution and avoid complexities like OT and CRDTs.&#x20;

Pros:

* Easy to implement.

Cons:

* Poor user experience: two users may want to add characters to the same sectin of the document, but their operations may not necessaily conflict.

## Do we need processing queue in client or server side?

### Client

Pros:

* Easy to implement&#x20;

Cons:

* No centralized QPS control, imagine if a doc have millions of people editing it altogether, it would cause problem.

### Server side

Pros:

* Centralized QPS throttle and control

Cons:

* Additional component to the system add complexity.
* significant delay if changes are piling up in the queue?
