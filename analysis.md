# **Analytics Report**

The biggest problem was actually simple and common: what is the most efficient way of retrieving points from the database? There are a few common practices, but what if you want to make it faster? You can grid the map by the same surface area or approximate the number of points (e.g., Kmeans++). This approach works fine until you want to implement a caching mechanism (e.g., Redis), and then everything starts to fall apart. Personally, I haven't found the best way, and now I agree that the core algorithm is not optimal.

After some research, this is the best algorithm I came up with:

I was trying to add some extra logic by counting which grid tiles I have in a certain area.

1. If we are in one tile, take everything from the cache. The map's viewport will cut out all we don't need.
2. If we have more than one tile:
    - If a certain tile is fully covered, take all points from Redis. Then, take the tiles that are not covered and send them to PostGIS. From the first glance, it looks like a solution.

Unfortunately, with the number of points (700-1000 locations for the Netherlands surface area, which leads to 30-50 tiles defined by Kmeans++), PostGIS is much faster than any Python logic. Retrospectively, I would now try something else to make it faster, but back then I was upset and ended up using the Polygon from the contrib.gis library.
