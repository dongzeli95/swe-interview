---
description: >-
  Geohashes are a way of encoding lat/lon points as strings. It works by
  reducing the two-dimensional longitude and latitude data into a
  one-dimensional string of letters and digits.
---

# Geohash

### Algorithm

```
def encode(latitude, longitude, precision=12):
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    geohash = []
    bits = [ 16, 8, 4, 2, 1 ]
    bit = 0
    ch = 0
    even = True
    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                ch |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash += __base32[ch]
            bit = 0
            ch = 0
    return ''.join(geohash)
```

1. Take the latitude and longitude ranges: latitude between -90 to 90 and longitude between -180 to 180.
2. Determine whether the given latitude is in the first half or the second half of the latitude range, and whether the given longitude is in the first half or the second half of the longitude range. For each, output 0 if it's in the first half or 1 if it's in the second half.
3. Now consider only the half-range that the point is in, and repeat the process. For each iteration, append 0 or 1 to the output based on which half the point is in.
4. Continue this process until you've reached the desired precision.
5. Interleave the bits from the latitude and longitude, starting with the longitude, to get the final Geohash in binary.
6. Convert the binary Geohash to base32 to get the final Geohash string.

### Precision Table

Geohash has 12 precisions, we only interested in 4-6.

<table><thead><tr><th width="176">geohash length</th><th>Grid size</th></tr></thead><tbody><tr><td>1</td><td>5000km x 5000km (size of earth)</td></tr><tr><td>2</td><td>1252km x 624km</td></tr><tr><td>3</td><td>156km x 156km</td></tr><tr><td>4</td><td>39km x 19km</td></tr><tr><td>5</td><td>4.9km x 4.9km</td></tr><tr><td>6</td><td>1.2km x 0.6km</td></tr><tr><td>7</td><td>152.9m x 152m</td></tr><tr><td>8</td><td>38m x 19m</td></tr><tr><td>9</td><td>4.8m x 4.8m</td></tr><tr><td>10</td><td>1.2m x 59.5cm</td></tr><tr><td>11</td><td>14.9cm x 14.9cm</td></tr><tr><td>12</td><td>3.7cm x 1.9cm</td></tr></tbody></table>

To find geohash length that fit the radius, we need the maximum geohash length that cover the entire region for best accuracy.
