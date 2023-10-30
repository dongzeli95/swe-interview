# Chapter 9: Consistency and Consensus

## Atomic Commit and Two-phase Commit

### Atomic commit on single node

On a single node, transaction commitment depends on the order in which data is written to disk: first the data, then the commit record.

### Distributed atomic commit

2PC uses a coordinator (transaction manager). When the application ready to commit, it has two phases:

1. Prepare Phase\
   Sends prepare requests to each node, asking whether they are able to commit:\
   a. If all participants reply "yes", coordinate continue with commit phase.\
   b. If any of participants replies "no", the coordinator sends an abort phase to all nodes in phase 2.\
   \
   When a participant votes "yes", it promises that it will definitely be able to commit later, regardless of whether coordinator decides later.
2. Commit/Abort Phase\
   Once coordinator decides the decision, abort or commit, the decision is irrevocable. \


Failures:\
If one of the participants or the network fails during 2PC (prepare requests fail or time out), the coordinator aborts the transaction. If any of the commit or abort request fail, the coordinator retries them indefinitely.

If the coordinator fails before sending the prepare requests, a participant can safely abort the transaction.

If the coordinator fails after receiving yes from all participants, the only way 2PC can complete is by waiting for the coordinator to recover in case of failure. This is why the coordinator must write its commit or abort decision to a transaction log on disk before sending commit or abort requests to participants.
