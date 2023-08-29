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

### User Location Data

<table><thead><tr><th width="157">user_id</th><th width="154">timestamp</th><th width="198">driving_mode</th><th>location</th></tr></thead><tbody><tr><td>101</td><td>1635740977</td><td>driving</td><td>(20.0, 30.5)</td></tr></tbody></table>

### Geocoding DB

Redis, Key-Value

key: place\_name, address. value: lat/lng pair.

### Precomputed Map Tiles

Store in S3 backed by CDN.

## Deep Dive

