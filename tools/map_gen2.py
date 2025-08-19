import json
import folium

# Create base map
m = folium.Map(location=[55.864237, -4.251806], zoom_start=12)

# Create a FeatureGroup for markers
marker_group = folium.FeatureGroup(name="Improvement Required Locations")

icon = folium.CustomIcon(
    icon_image='/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/res_img.png',
    icon_size=(40, 40)
)

# Load data
with open('/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/glasgow_restraunts.json') as f:
    locations = json.load(f)

# Add filtered markers
for loc in locations["establishments"]:
    latitude = loc['geocode']['latitude']
    longitude = loc['geocode']['longitude']
    name = loc['BusinessName']
    rating = loc["RatingValue"]
    AddressLine = loc["AddressLine2"]
    PostCode = loc["PostCode"]
    FHRSID = loc["FHRSID"]
    BusinessType = loc["BusinessType"]

    if latitude is None or "Retailers" in BusinessType or rating != "Improvement Required":
        continue

    popup_html = f"""
    <b>{name}</b><br>
    Rating: {rating}<br>
    Address: {AddressLine}<br>
    Postcode: {PostCode}<br>
    <a href='/search?q={name}' target='_blank'>View Details</a>
    """
    popup = folium.Popup(popup_html, max_width=250)

    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        tooltip=name.strip(),
        icon=icon
    ).add_to(marker_group)

# Add markers to map
marker_group.add_to(m)

# Optional: remove LayerControl if only one layer
# folium.LayerControl().add_to(m)

# Save map
m.save("/Users/matthewmaloy/projects/python/restaurant_ratings/application/static/map_with_locations.html")
