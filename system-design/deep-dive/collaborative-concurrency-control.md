# Collaborative Concurrency Control

## Strong Eventual Consistency

1. Eventual delivery: every update made to one non-faulty replica is eventually processed by every non-faulty replica.
2. Convergence: any two replicas that have processed the same set of updates are in the same state.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-22 at 8.48.33 AM (2).png" alt=""><figcaption></figcaption></figure>

## CRDT

* Operation based

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-22 at 8.54.18 AM.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-22 at 11.22.12 AM.png" alt=""><figcaption></figcaption></figure>

1. last write wins
2. Need arbitrary position arithemetic library.
3. Reliable broadcast ensures every operation is eventually delivered to every replica.
4. Applying operation is commutative: order of delivery doesn't matter.

* State based

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-22 at 9.02.59 AM.png" alt=""><figcaption></figcaption></figure>

Merge operator must satisfy:

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-22 at 9.05.38 AM.png" alt=""><figcaption></figcaption></figure>

Best effort broadcast

### State based vs operation based:

| State-based                              | Operation-based                       |
| ---------------------------------------- | ------------------------------------- |
|                                          | Can tolerate message loss/duplication |
| has smaller message payload to broadcast |                                       |
|                                          |                                       |

## OT

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-22 at 11.18.53 AM.png" alt=""><figcaption></figcaption></figure>

Initially the document has "BC"

1. User A inserts A at the beginning, the text becomes "ABC"
2. User B inserts D at the very end, the text becomes "BCD"
3. When then changes from user A get broadcast to userB, it works okay.
4. When the changes from user B: (insert, 2, "D") get broadcast to user A, it becomes "ABDC"&#x20;
5. Operational transformation aim to transform the operation such that the operation will work correctly.
