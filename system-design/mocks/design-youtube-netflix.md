# Design Youtube/Netflix

## Topics:

1. How to design schema for video segment? for partitioning.
2. CDN and Redis cache usage?
3. How to achieve low latency?
4. How to de-duplicate videos?
5. How to implement search?
6. Mention Vitess database abstraction layer.
7. Adaptive streaming?
8. How to do video recommendation?

## Functional Requirement

1. Users can view video.
2. Users can see a list of recommended video on homepage.
3. Users can search video based on keyword.
4. Users can upload videos.

Optional:

1. Uploaded video can reviewed and censored.
2. Like and dislike videos
3. Add comments to videos.

## Non-functional Requirement:

1. Low latency
2. Highly available
3. Scalable
4. Fault tolerance.
5. Availability > consistency
6. Read > Write

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (1).svg" alt="" class="gitbook-drawing">

1. Client send a GET request to API Gateway for fetching videos.
2. request get routed to Video service
3. video service determines the user id for the client and fetch recommended videos from DB.
4. video service send back the response with a list of videos.
5. client be able to see videos in the client page.

##

## API

```
/v1/recommendation GET

/v1/video GET (stream video)
Request 
json {
  screen_resolution,
  user_bitrate: determine quality of video chunks,
}
Response: 
json {
  "clips": [
    "clip0": {
    
    },
    "clip1": {
    
    }
    ...
  ],
}

/v1/video POST (Upload Video)
Request
json {
  user_id
  video_file: video file for upload
  category_id: "Entertainment", "Engineering" or "Science"
  title,
  description,
  tags
  default_language
  privacy_settings: PUBLIC, PRIVATE etc.
}

Response
201 OK

/v1/video PUT

/v1/video DELETE

/v1/video/feedback POST (thumbup or thumbdown)
```

## Data Schema

```
User Table
id
email
username
pw
dob

Video Table
id
title
description
upload_date
channel_id
likes_count
dislikes_count
views_count
video_URI
privacy_level
default_lang
first_clip_id
clips_mapping: {0: clipid0, 1: clipid1...}

Channel Table
id
channel_name
user_id
subscribers
description
category_id

Recommendation Table

Clip Table
clip_id (primary key)
clip_offset (sort key)
next_clip_id
video_id
author_id
clip_path: this can be a S3 path where we have different encoding and resolution url there.

Clip Encodings (Store it in CDN storage)
clip_id
encoded_content (binary format)

Comments Table
id
video_id
user_id
posted_date
comment_text
likes_count
dislikes_count

Category Table
```

## Scale

2B DAU, how many new videos a day

QPS: 20B requests = 20\*10^9 / 10^5 = 20\*10^4 = 200k QPS

<mark style="color:purple;">Storage</mark>:

Avg video length: 5 mins

Size before compression: 600MB

Size after compression: 30MB

500 hrs video is uploaded every minute

6MB to store a minute of video

total = 6\*500\*60 = 180000 MB per minute = 180GB per minute = 180\*24\*60 = 259 TB per day = 94TB per year.

<mark style="color:purple;">Bandwidth</mark>

500 hr/min \* 60 min \* 120mb/min \* 8 bits / 60s = 480Gbps

<img src="../../.gitbook/assets/file.excalidraw (1).svg" alt="" class="gitbook-drawing">

1. Use dynamo DB for large read requests and partition data easily with schema key design

DynamoDB Limitations: 1000WCU/s, 3000RCU/s.

1. Use Redis cache to store frequent read data, viral video posted by big influencers.

## How to deduplicate video?

Assume 50 out of 500 hours of videos uploaded to Youtube are duplicates. Considering the one minute of video requires 6MB of storage space, the duplicated content will take up following storage space:

```
(50*60) mins * 6MB/min = 18GB
```

If we avoid video duplication, we can save up to 9.5 perabytes of storage space.

There is also copyright issue, No content creator would want their content plagiarized.&#x20;

Options:

1. Locality-sensitve hashing.
2. Block matching algorithms, phase correlation
3. AI

Ateliere's proprietary FrameDNA™ AI/ML technology revolutionizes video management by fingerprinting each frame upon ingest. This allows for an accurate comparison of video files. This advanced technology not only helps in identifying duplicate content but also assists in detecting any alterations or tampering within the video files. Additionally, the system's efficient storage management capabilities ensure that only the most relevant and original content is preserved, optimizing storage resources and reducing unnecessary duplication.

## Adaptive Streaming

While the content is being served, the bandwidth of the user is also being monitored. Since the video is divided into chunks of different qualities, each video clip can be provided based on changing network conditions.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-20 at 4.58.41 PM.png" alt=""><figcaption></figcaption></figure>

The adaptive bitrate algorithm can bsed on four parameters:

1. End-to-end available bandwidth (from a CDN/servers to a specific client)
2. The device capabilities of the user.
3. Encoding techniques used.
4. The buffer space at the client.

## Recommendation

Youtube recommends video to user based on their profile, taking into account factors such as their interests, view and search history, subscribed channels, related topics to already viewed content and activities on content such as comments and likes.

Youtube filters videos in two phases:

1. <mark style="color:purple;">Candidate generation</mark>: millions of Youtube videos are filtered down to hundreds based on the user's history and current context.
2. <mark style="color:purple;">Ranking</mark>: The ranking phase rates videos based on their feature and according to the user's interests and history. Hundreds of videos are filtered and ranked down to a few dozen videos during the phase.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-20 at 5.36.34 PM.png" alt=""><figcaption></figcaption></figure>

3. <mark style="color:purple;">Collaborative Filtering</mark>

A technique used in recommendation systems, works by predicting a user's interests based on preferences of many users.

User-based collaborative filtering: The approach recommends items by finding similar users. For example, if user X likes items A, B and C and user Y likes item A, B and D. The system infer that X might also like item D because Y likes it.

<figure><img src="../../.gitbook/assets/Screenshot 2024-02-20 at 5.40.56 PM.png" alt=""><figcaption></figcaption></figure>

[https://blog.hootsuite.com/how-the-youtube-algorithm-works/](https://blog.hootsuite.com/how-the-youtube-algorithm-works/)

2005-2011: Optimizing for clicks & views

2012: Optimizing for watch time

2015-2016: Optimizing for satisfaction: Shares, likes and Dislikes, not interested button.

[https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf](https://static.googleusercontent.com/media/research.google.com/en/pubs/archive/45530.pdf)
