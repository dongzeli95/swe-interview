# Cassandra DB

## 2017 Discord Use Case

1. 50/50 read/write ratio.
2. Voice chat channel:&#x20;
   1. < 1000 messages a year.
   2. returning small amount of data involves random seek in disk causing disk cache evictions.
3. Private text chat heavy channel:
   1. 100k to 1M messages a year.
   2. read request is low and unlikely in disk cache.
4. random reads

## About Cassandra

It's a KKV store.&#x20;

The primary key is for partition.

The secondary key is for identify one row within that parition.

## Schema

```
CREATE TABLE messages (
  channel_id bigint,
  message_id bigint,
  author_id bigint,
  content text,
  PRIMARY KEY (channel_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

<mark style="color:purple;">Issues:</mark>

Began to see warinings that partitions were found over 100MB in size.&#x20;

Large partition put a lot of GC pressure on Cassandra during compaction.

<mark style="color:purple;">Solution:</mark>

decide to bucket messages by time. we store about 10 days of messages in one bucket.

```
DISCORD_EPOCH = 1420070400000
BUCKET_SIZE = 1000 * 60 * 60 * 24 * 10


def make_bucket(snowflake):
   if snowflake is None:
       timestamp = int(time.time() * 1000) - DISCORD_EPOCH
   else:
       # When a Snowflake is created it contains the number of
       # seconds since the DISCORD_EPOCH.
       timestamp = snowflake_id >> 22
   return int(timestamp / BUCKET_SIZE)
  
  
def make_buckets(start_id, end_id=None):
   return range(make_bucket(start_id), make_bucket(end_id) + 1)
```

## New Schema

```
CREATE TABLE messages (
   channel_id bigint,
   bucket int,
   message_id bigint,
   author_id bigint,
   content text,
   PRIMARY KEY ((channel_id, bucket), message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

## Concerns

### Eventual Consistency

* Last write wins.
* Read before write anti pattern: read are more expensive than write in Cassandra.
* Every write is an upsert, meaning if exist update, not exist we insert.

#### Concurrency Issues

If user A removes the same message record just before user B edit it, we would end up with a row missing all data except primary key and updated column.

Two solutions:

1. Write the whole message back when editing the message. This had the possibility of resurrecting messages, adding more chance for concurrent conflicts.
2. Figuring out message is corrupt and delete it from DB.

#### Tombstone issues

Avoiding writing null values to Cassandra, causing unnecessary tombstone writing.

A popular channel only have 1 message in it, the owner deleted millions of messages using tombstone. It takes 20 second to load up this channel.

#### Cause:

Cassandra had to effectively scan millions of messages tombstones (generating garbage faster than JVM could collect it.)

#### Solution

1. Lower lifespan of tombstone from 10 days to 2 days
2. Changed application query code to track empty buckets and avoid them in the future. If a user caused this query then at worst Cassandra would scan only the most recent bucket.



