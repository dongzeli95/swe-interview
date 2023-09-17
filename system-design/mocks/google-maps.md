# Google Maps

## Functional Requirements

* User Location Update
  * Monitor live traffic, detect new and closed roads, analyze user behavior for personalization.
  * Use real-time data to provide accurate ETA and reroute options.
  * Leverage stream of location data to improve system.
* Navigation Service, including ETA
* Map rendering

## Non-functional requirements:

* Accuracy
* Low latency
* Highly available

## Scale

1B DAU

**35** minutes per week for avg user

1B \* 35 / 7 = 5B minutes per day.

#### <mark style="color:blue;">**QPS:**</mark>&#x20;

1. Navigation Requests

twice a day -> 2B requests a day -> 2\*10^9 / 10^5 = **20000** QPS

2. Location Update Requests

300B requests per day if send requests every seconds.

300B per day = 3M QPS

if send requests every 15 seconds = 3M / 15 = 30\*10^5 / 15 = **200000** QPS.

Peak traffic = 2\*10^5 \* 5 = **1M** QPS

#### <mark style="color:blue;">Storage</mark>

At zoom level 21, about 4.3 trillion map tiles.

Each tile is a 256x256 pixel compressed PNG, size = 100KB

4.3 trillion x 100 KB = 440PB

Compressed image + natural lands = **44 to 88PB**

**100 PB in total**

## API

Location Update:

**POST /v1/locations**

Payload: JSON encoded array {latitude, longitude, timestamp}

**GET /v1/navigation?origin=xxx\&destination=xxx**

Response

```
{
    'distance': {'text': '0.2 mi', 'value': 259},
    'duration': {'text': '1 min', 'value': 83},
    'start_location': {'lat': 37.4027165, 'lng': -121.9435809},
    'end_location': {'lat': 37.4021232, 'lng': xxx},
    'polyline': {'points': 'xxx'},
    'geocoded_waypoints': [
        {
            "geocoder_status": "OK",
            "place_id": "xxx"
        },
        {...},
        {...}
    ],
    'travel_mode': 'DRIVING'
}
```

## High Level Diagram

<img src="../../.gitbook/assets/file.excalidraw (5).svg" alt="" class="gitbook-drawing">

## E2E

#### App Initialization

1. Client open up the app, the GPS on the phone will locate user and its coordinate.
2. Client sends map rendering requests to fetch map tiles CDN urls to render nearby map on the specific zoom level.
3. Client set up websocket connections to receive reroute options, ETA updates.

#### Navigation

1. Client search for some place / address on search bar.
2. Backend will route request to geocoding service to convert place or address to latitude and longitude pair.
3. Backend returns the detail information about the place as well as the navigation option response based on user location and destination location.

#### Location Update

1. Client send location update requests every 15 seconds.

## Data Model

### Routing Tiles

> By breaking up road networks into routing tiles that can be loaded on demand, the routing algorithms can significantly reduce memory consumption and improve pathfinding performance by only consuming a small subset of the routing tiles at a time, and only loading additional tiles as needed.

Initial dataset contains roads and associated metadata like names, country, longitude and latitude. The data is not organized as graph structure and is not usable by most routing algorithm.&#x20;

Each tile contains a list of graph nodes and edges representing the intersections and roads.

It's efficient to store it in **S3** and cache it progressively. We can use some package/library to serialize adjacency lists into a binary file. We can **organize tiles by its geohashes** for fast look ups.

#### Road Segments

A road can be represented as a list of connected points: (lat1, lng1), (lat2, lng2)...(latN, lngN). Calculate the geohash for every point, and identify which tiles the road passes through.

For each road segment that crosses multiple tiles, you can split it into smaller segment lie within individual tiles.&#x20;

```
Schema:
segment_id: uuid
start_point: The starting geographical coordinate of the segment.
end_point: The ending coordinate of the segment.
geom: The geometry of the segment, stored as LineString in PostGIS.
geohash: The geohash tile this road belongs to.
road_type: enum, "highway", "local" etc.
speed_limit: xx mph
other_attributes: is_toll_road, surface_type etc.
```

### User Location Data

<table><thead><tr><th width="157">user_id</th><th width="154">timestamp</th><th width="198">driving_mode</th><th>location</th></tr></thead><tbody><tr><td>101</td><td>1635740977</td><td>driving</td><td>(20.0, 30.5)</td></tr></tbody></table>

### Geocoding DB

Redis, Key-Value

key: place\_name, address. value: lat/lng pair.

### Precomputed Map Tiles

Store in S3 backed by CDN.

## Deep Dive

### Location Service

<img src="../../.gitbook/assets/file.excalidraw (6).svg" alt="" class="gitbook-drawing">

### Rendering Map Tiles

**WebGL**: Instead of sending images over network, we can send vector formations (paths and polygons)

Pros: vector tiles provide a much better zooming experience.

### Navigation Service

#### Shortest Path Service

1. Receives the origin and destination in lat/lng pairs. Load start points and end points of routing tiles based on geohashes.
2. Starts with origin routing tile, as it traverse the graph, hydrates neighboring tiles from object storage, including bigger tiles at higher zoom level so that it can make use of highway roads etc.

#### ETA Service

Use machine learning to predict ETAs based on current traffic and historical data.

#### Ranker Service

Navigation service obtains the ETA predications, passes the info to ranker to rank possible routes from fastest to slowest, return top-k results to navigation service.

#### Updater Service

Tap into Kafka location update stream and asynchronously update traffic DB and routing tiles DB.&#x20;

<mark style="color:blue;">Update routing tiles DB</mark>: responsible for transforming the road dataset with newly found roads and road closures into a updated set of routing tiles.

<mark style="color:blue;">Update traffic DB</mark>: Extracts traffic conditions from the streams of location updates sent by active users. Enable ETA service to provide better estimates.

<img src="../../.gitbook/assets/file.excalidraw (1) (1).svg" alt="" class="gitbook-drawing">

### Adaptive ETA and rerouting

The system needs to track all active navigating users and update them on ETA continuously.

* How do we track actively navigating users?
* How do we store data, so we efficiently locate the users affected by traffic changes among millions of navigation routes?

Traffic DB stores actively navigating users with routing tile information:

```
user1: current_r_1, super(r_1), super(super(r_1)), ...
```

We store the upper zoom level routing tile until we found the destination.

To find if a user is affected by the traffic change, we need only check if a routing tile is inside the last routing tile of the row in record.

We prefer to use <mark style="color:blue;">websocket</mark> to communicate the reroute options to clients.

## TODO

* [ ] Why Kafka is good for scaling and broadcasting the location update data?
* [ ] Navigation Service Deep Dive.
* [ ] ETA Service machine learning.
* [ ] What is HTTP keep-alive?
* [ ] Pros and Cons of long polling, websocket and SSE?
