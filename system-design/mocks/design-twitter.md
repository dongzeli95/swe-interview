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
