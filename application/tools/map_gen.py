import folium
from folium.plugins import Search
import json

# Create a base map centered on Scotland
map = folium.Map(location=[56.4907, -4.2026], zoom_start=6)

# Add a marker (e.g. for Edinburgh)
folium.Marker(
    location=[55.9533, -3.1883],
    popup="Edinburgh",
    tooltip="Click for info"
).add_to(map)

icon = folium.CustomIcon(
    icon_image='/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/res_img.png',  # relative path to image
    icon_size=(40, 40)  # adjust size as needed
)

name_search_fg = folium.FeatureGroup(name="name")
# Load data from a local JSON file
with open('/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/glasgow_restraunts.json') as f:
    locations = json.load(f)

for loc in locations["establishments"]:

    latitude = loc['geocode']['latitude']
    longitude = loc['geocode']['longitude']
    name = loc['BusinessName']
    rating = loc["RatingValue"]
    AddressLine = loc["AddressLine2"]
    RatingDate = loc["RatingDate"]
    NewRatingPending = loc["NewRatingPending"]
    BusinessType = loc["BusinessType"]
    PostCode = loc["PostCode"]

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }}
            h1 {{ color: #2c3e50; }}
            .rating {{ font-size: 1.5em; color: #27ae60; }}
            .pending {{ color: #e74c3c; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{name}</h1>
            <p><strong>Address:</strong> {AddressLine}</p>
            <p><strong>Postcode:</strong> {PostCode}</p>
            <p><strong>Rating:</strong> <span class="rating">{rating}</span></p>
            <p><strong>Rating Date:</strong> {RatingDate}</p>
            {"<p class='pending'>New Rating Pending</p>" if NewRatingPending else ""}
        </div>
    </body>
    </html>
    """

    if latitude == None:
        continue
    if  "Retailers" in BusinessType:
        continue
    if rating == "Improvement Required":
        folium.Marker(
            location = [latitude, longitude],
            popup = html,
            icon = icon,
            tooltip = name
        ).add_to(name_search_fg)

name_search_fg.add_to(map)

Search(
    layer=name_search_fg,
    search_label="tooltip",  # Use "popup" if you prefer
    placeholder="Search for a business...",
    collapsed=False
).add_to(map)

map.save("/Users/matthewmaloy/projects/python/restaurant_ratings/application/static/map_with_locations.html")

