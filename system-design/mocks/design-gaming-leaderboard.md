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

## Scale

5M DAU, 10 matches per day -> 50M matches per day -> 600 QPS -> peak 600x5 = 3000 QPS.

Top 10 player -> 50 users/s -> 50 QPS if user only see leaderboard when first open the game.

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

A sorted set is implemented by: hash table and a skip list.  hash table maps users to scores and the skip list maps scores to users. In sorted set, users are sorted by scores.

**ZADD:** insert user into set if they don't exist. Otherwise, update the score for user. It takes O(logn) to execute.

**ZINCRBY**: increment the score of the user by specified increment, O(logn) to execute.

**ZRANGE/ZREVRANGE:** fetch a range of users sorted by score. It takes O(logn+m), m is the number of entries to fetch.&#x20;

**ZRANK/ZREVRANK**: fetch position of any user in ascending/descending order.

#### Add a point to user:

```
ZINCRBY leaderboard_feb_2021 1 'mary1934'
```

#### Fetches top 10 global leaderboard

```
ZREVRANGE leaderboard_feb_2021 0 9 WITHSCORES
```

#### Fetch user relative position on leaderboard

```
ZREVRANK leaderboard_feb_2021 'mary1934'
```

#### Fetch n positions above/below user's position

```
ZREVRANGE leaderboard_feb_2021 pos-5 pos+5
```

#### Storage requirements

24 character name: 24 bytes + score 4 bytes = 28 bytes.

one leaderboard entry per MAU = 28 bytes \* 25 million = 700M bytes = 700MB

peak QPS is 3000 QPS, both are acceptable for a single Redis server.

<img src="../../.gitbook/assets/file.excalidraw (17).svg" alt="" class="gitbook-drawing">

## Scale Up

### What if score service is down?

Load balancer in front of score service and deploy service onto kubernetes. Use auto scaling.

### What if DB is down?

Figure out read / write throughput?

If read throughput, then we need to add read replicas, add in-memory cache?

### What if we grows DAU 100 times?

500M DAU -> data size: 65GB, QPS = 250,000

We need data sharding:

#### <mark style="color:purple;">Fixed partition</mark>

We break up score by range. \[1, 100], \[101, 200], \[201, 300] ... \[901, 1000]

Need to make sure even distribution of scores across leaderboard.

When we insert/update score for a user, we need to know which shard they are in.&#x20;

#### Option1:

calculating user current score from MySQL DB, not very performant.

#### Option 2

use a secondary cache to maintain mapping between user id and shard id.

**Fetching top 10 player**

fetch top 10 players from the shard with highest scores.

**Fetching rank of a user**

calculate rank within local shard + total number of players in shards with higher scores. We can use _info keyspace_ command in O(1)

#### <mark style="color:purple;">Hash partition</mark>

Redis cluster provides hash slot to shard data automatically across multiple Redis nodes. We can compute hash slot by: CRC16(key) % 16384

The first node contains hash slots \[0, 5500], second: \[5501, 11000], third: \[11001, 16383]

Cons:

1. For returning top k results, we need to use scatter-gather to merge the results. need to be sorted.
2. If we have a lot of partitions, the query has to wait for the slowest partition.
3. doesn't provide straightforward solution for determining the rank of a specific user.
