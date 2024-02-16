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

is\_available

version

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

```
v1/booking POST
json {
  uid
  listing_id
  payout
}

Response payload:
201 OK {
  "message": "Reservation created. We've informed the dogsitter. They will have 24hr to responde."
}

How this API work?
1. Check if the Listing is still available?
SELECT is_available FROM listing
WHERE listing_id is xxxxxx;
2. Start a transaction
a. create a new reservation record
b. mark the listing as unavailable.
```

## How to avoid double booking?

1. The same user clicks on book button multiple times.
2. Multiple users try to book same room at the same time.

### Same user

1. Client side implementation. On the website we can disable the button once the booking request is sent. This approach is not very reliable since user can maybe disable javascript bypassing client check.
2. Idempotent API. Add an idempotency key in the reservation API request. We can assign a idempotency key reservation\_id to avoid double reservation.

### Different user

User1 and User2 both check the listing, they both see the same listing available, they may or maynot click the booking button at the same time but both of their requests will go through. We will end up with two reservation records with the same listing.

> The isolation property in ACID means database transactions must complet their tasks independently from other transactions. So data changes made by transaction 1 are not visible to transaction 2 until transaction 1 is completed.

#### Option 1: Pessimistic Locking

Pessimistic concurrency control, prevents simultaneous updates by placing a lock on a record as soon as one user starts to update it. Other users who attempt to update the record have to wait until the first user has released the lock.

For MySQL:

```
SELECT ... FOR UPDATE
```

works by locking the rows returned by a selection query.&#x20;

Pros:

* Prevents applications from updating data that is being changed.
* Easy to implement and it avoids conflicts by serializing updates.
* Useful for write heavy application when data-contention is heavy.

Cons:

* Deadlocks may occur when multiple resources are locked. Writing deadlock-free application code could be challenging.
* If a transaction is locked for too long, other transactions cannot access the resource. This has a significant impact on database performance, especially when transactions are long lived.

#### Option 2: Optimistic Locking

Optimistic concurrency control, allows multiple concurrent users to attempt to update the same resource.

1. A new column called version is added to the database table.
2. Before a user modifies the database row, the application read the version number of the row.
3. When the user updates the row, the application increases the version number by 1 and write back to db.
4. A database validation check is put in place: the next version number should exceed the current version number by 1. Otherwise, validation fails and user tries again from step 2.

Pros:

* Prevents applications from updating stale data.
* We don't need to lock db resources. version number control is on application level.
* Optimistic lock is good when data-contention and concurrency is low.&#x20;

Cons:

* Poor performance when data contention is heavy.
* Why? \
  When there are a lot of clients try to reserve the same hotel room, only one of them will succeed and the rest of client requests will have to retry.

#### Option 3: Database constraints

Instead of using is\_available, we can use availablity initialized to 1, and we add the following DB constraint:

```
CONSTRAINT `check_availability` CHECK (availability >= 0)
```

Pros:

* Easy to implement, works well when data contention is low.

Cons:

* The db constraint cannot be version controlled easily like application code.
* Not all db support constraints, if we do data migration in the future, it might cause problems.
