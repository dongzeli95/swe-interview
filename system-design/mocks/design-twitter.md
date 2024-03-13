# Design Twitter

## Topics

1. SQL vs NoSQL
2. How to do index on db schema?
3. How to do pagination on news feed?
4. 随着user, requests, data size increase, how to scale the system?
5. celebrity: different celebrity data pattern diffs a lot, do we need different message queue to fan out?
6. How to deal with thundering herd problem?
7. How to validate and limit malicious user behavior (send 100 tweets in one minute?)
8. How to block sensitive words in tweet?
9. How to design hash tag?

## Functional Requirements

1. Post tweets: registered user can post one or more tweets.
2. View user or home timeline.
3. Delete tweets: can delete one or more tweets on twitter.
4. Follow or unfollow.
5. Like/dislike
6. Reply to tweet.
7. Retweet.
8. Search tweet.
9. Hashtags.
10. Do we support media types like video or images?

## Non-functional Requirement

1. Highly available
2. Low latency
3. read, write ratio: 10000:1
4. Eventual consistency, availability > consistency.

## Scale

### QPS

100M active users -> 500M tweets per day:

Each tweet averages a fanout of 10 deliveries -> 5B total tweets delivered on fanout each day.

10B read requests per day -> 10^4 QPS.

10B search per month.

### Data

```
Tweet id: 8 bytes
user id: 32 bytes
text: 140 bytes
total: 1KB

1KB * 500M tweets per day * 30 days
0.5PB in three years.
```

## API

```
Post tweets
POST /v1/tweet
Request:
{
  user_id
  content
  access_type: private, public etc
  tweet_type? video,image?
  media_url?
}

View home timeline
GET /v1/home
Request: 
{
  user_id,
  page_number, // pagination
  page_size,
  user_location,
}

POST /v1/follow (unfollow)
Request {
  user_id,
  followed_user_id,
}

GET /v1/search
```

## Data Schema

```
Dynamo DB

User Table
{
  user_id, (partition_key)
  profile_url,
  bio,
  userhandle,
  encrypted_pw,
  email,
}

Tweets Table
{
  tweet_id, (partition_key)
  user_id,
  content,
  created_at, (sort_key)
  is_deleted,
}

Follow Table
{
  following_id (partition_key)
  follower_id
  followee_id
  updated_at (sort_key)
}

HashTag table {
  hashtag_id
  name
  reference_counter
}

HashTagRef Table {

}
```

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (32).svg" alt="" class="gitbook-drawing">

1. Client send request, either post a tweet or view home timeline.
2. Web server read and write from DB.
3. Return the response back to client.

Single point of failures:

1. Web servers
2. DB

<img src="../../.gitbook/assets/file.excalidraw (33).svg" alt="" class="gitbook-drawing">

Posting a tweet:

1. user send post tweet request load balancer, it get routes onto one of the web servers.
2. web server write this record onto DB.

Viewing a tweet:

1. user send read request for home timeline.
2. web server read tweets from DB.
3. Same tweets might be read multiple times by different followers.&#x20;

```
userid: listOfFollowers
timeline cache, userId: listOfTweets
```

More read burden on DB. So we can fanout during the write phase for posting tweet:

1. Each user store a list of followers in the cache.
2. We push the tweets into user timeline inbox in the cache.

Posting a tweet:

1. user send post tweet request load balancer, it get routes onto one of the web servers.
2. web server write this record onto DB.
3. Fanout to store tweets in each follower's tweet list cache.

Viewing a tweet:

1. user send read request for home timeline.
2. read from redis first to see if there are any tweets.
3. it not enough, we read tweets from DB.
4. Same tweets might be read multiple times by different followers.&#x20;

Pros:

1. We reduce load on read by doing fanout.

Cons:

1. If the tweet poster is a celebrity, the fanout overhead is huge.
2. We need Redis to scale.



Celebrity case:

Instead of fanout, we store some cache for celebrity in Redis as well:

```
Celebrity tweets, userId: listOfTweets
userId: listOfCelebritiesIdTheUserIsFollowing
userId: isCelebrity
```

<img src="../../.gitbook/assets/file.excalidraw (34).svg" alt="" class="gitbook-drawing">

## Deep Dive

### How to deal with thundering herd problem?

Cascading failure: Some server crashed, and other servers have to take on additional load, but they might not be able to handle it either so all of them crashed one by one.

Rate limiting: Token Bucket/ Leaky Bucket/Sliding Window

For each request we can categorize the user by maintaining an in-memory map or in redis, with user as key and a token. On each request from the same user the token is decreased by one and when it reaches zero we throw temporary error to user.

It might be space intensive if there are too many users...

Context: Some celebrity tweets trends, difficult to determine the load beforehand. Auto scale might not work either.

## Redis

```
userid: listOfFollowers
timeline cache, userId: listOfTweets
-------------------------------------
Celebrity tweets, userId: listOfTweets
userId: listOfCelebritiesIdTheUserIsFollowing
userId: isCelebrity
```

* Keep only several hundred tweets for each home timeline in the **Memory Cache**
* Keep only active users' home timeline info in the **Memory Cache**
  * If a user was not previously active in the past 30 days, we could rebuild the timeline from the **SQL Database**
    * Query the **User Graph Service** to determine who the user is following
    * Get the tweets from the **SQL Database** and add them to the **Memory Cache**

**How to update cache?**

1. **cache aside**

application is responsible for reading and writing from storage.

2. **write-through**

application uses the cache as the main data store, reading and writing data to it without interacting with db.&#x20;

Pros: read are fast.

Cons:&#x20;

* write-through is a slow overall operation due to write operation.
* Most data written might never be read, which can be minimized by TTL config.



2. **write-behind**
3. **refresh ahead**

### How to do censorship for tweets?

1. We can train a model or use some existing models to do that?
2. GPT 3.5 API call?
