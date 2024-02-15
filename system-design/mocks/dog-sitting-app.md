# Dog Sitting App

Questions:

1. If this app is location based, how much is the radius we are considering?
2. For booking, what preferences/filters we are considering?&#x20;

## Functional Requirement

1. Dog owner will be able to see dog sitters nearby, ideally within a radius?
2. Dog owner will be able to finish bookings.
3. Dog sitter will be able to see bookings from dog owners.

## Non-functional Requirement

1. Low latency
2. Highly available
3. Consistency for booking operation, both parties should be informed.

## High Level Design

<img src="../../.gitbook/assets/file.excalidraw (19).svg" alt="" class="gitbook-drawing">

### Reservation Service

Receives reservation request and reserves dog sitters. It also tracks for listing inventory as listings are reserved or reservations are cancelled.

### Listing Service

Dog sitter can view record of upcoming reservation, cancel a reservation etc.

## Data Schema

<mark style="color:purple;">Listing table:</mark>

id

dogsitter\_id

type: boarding, dog\_walking, drop\_in

description:

date

<mark style="color:purple;">Rate table:</mark>

id

listing\_id (PK)

date (PK)

rate

<mark style="color:purple;">Profile table:</mark>

user\_id

profile\_pic

location

review

description

<mark style="color:purple;">Geohash\_index table</mark>

user\_id, geohash

## API

```
v1/search POST
json {
  user_id,
  latitude,
  longitude,
  radius,
  drop_off_date,
  pick_up_date
}

Response payload:
{
  [
    profile1: {
      name
      profile_pic
      minimum_price
      distance,
      description,
      review_star
    }
  ]
}

How this API work?
1. Fetch a list of profile ids from DB based on geo_hash.
SELECT profile_id FROM geohash_index WHERE geohash LIKE `{:geohash}%`

2. Fetch listings given the profile ids and the date range.
SELECT date, user_id FROM listing
WHERE user_id IN ${profile_list} AND date between ${startDate} and ${endDate}

3. Filter profile_ids and fetch profile details and return the list of profile details.
SELECT * FROM profile
WHERE user_id IN ${user_list}
```

## How to avoid double booking?
