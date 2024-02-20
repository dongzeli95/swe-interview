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

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

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

<img src="../../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

1. Use dynamo DB for large read requests and partition data easily with schema key design

DynamoDB Limitations: 1000WCU/s, 3000RCU/s.

1. Use Redis cache to store frequent read data, viral video posted by big influencers.
