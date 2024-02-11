# Design Gaming Leaderboard

## Clarifying Questions

1. How real-time we want this gaming leaderboard to be updated?
2. How's score calculated?
3. Do we show top 10 players or show position of the current user, and show 5 more player above/below the current player.
4. How many players? 5M DAU, 25M MAU,&#x20;
5. How many games are played on average during a day? 10 matches per day for each player.
6. Is there a time segment associated with the leaderboard? Each month, a new rounament kicks off which starts a new leaderboard.

## Functional Requirements:

1. Able to show position of current user, show 5 more player above/below the current player.
2. Able to show top 10 player.

## Non-functional Requirements:

1. Highly available
2. Highly scalable
3. Real time.

## High Level Architecture

<img src="../../.gitbook/assets/file.excalidraw (16).svg" alt="" class="gitbook-drawing">



### DB Options

1. Relational DB

New user:

```
INSERT INTO leaderboard (user_id, score) VALUES ('mary1934', 1);
```

Existing user:

```
UPDATE leaderboard set score=score+1 where user_id='mary1934';
```

Find user's leaderboard position:

```
SELECT (@rownum := @rownum+1) AS rank, user_id, score
FROM leaderboard
ORDER BY score DESC;
```

Pros:

* Easy to implement.

Cons:

* Query become slow when there are millions of rows: attempting to do a rank operation over millions of rows is taking 10 seconds, which not acceptable for real-time requirements.&#x20;
* Cache won't help since data are constantly changing.
* Won't work on finding user rank because it needs a full table scan to determine rank.

2. NoSQL DB

Pros:

* Optimized for write, like Cassandra, DynamoDB
* Efficiently sort items within the same partition by score.
* Add index: use game\_name#{year-month} as partition key and score as sort key.
* Further partition by user\_id % number of partition. Partition key becomes game\_name#{year-month}#user\_hash

Cons:

* Need to figure out how much partition we need
* Need to merge top 10 player results from multiple partitions.
* Trade off between read complexity and number of partitions, need benchmarking.
* No straight-forward solution to query relative rank of a user.
  * Can query percentile of a user's position instead. top 10%, 20% etc.
  * Assuming score distributions is similar across all shards. Run a cron job to analyzes the distribution of score to percentile and cache the result.

3. Redis Sorted Set

*



What if score service is down?&#x20;

Load balancer in front of score service and deploy service onto kubernetes. Use auto scaling.

What if DB is down?&#x20;

Figure out read / write throughput?

If read throughput, then we need to add read replicas, add in-memory cache?

If write throughput, we might need to consider add message queue like Kafka or SQS to throttle the write throughput.
