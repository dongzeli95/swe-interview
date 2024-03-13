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



## Redis

```
userid: listOfFollowers
timeline cache: userId: listOfTweets
-------------------------------------
Celebrity tweets: userId: listOfTweets
userId: listOfCelebritiesIdTheUserIsFollowing
userId: isCelebrity
```
