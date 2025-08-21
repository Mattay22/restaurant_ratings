import requests
import folium
import json

#def create_postcode_map(postcode):
postcode = "G33"
url = f"https://api.postcodes.io/outcodes/{postcode}"
results = requests.get(url)

location = results.json()
if location:
    lat, lon = location["result"]["latitude"], location["result"]["longitude"]
print(lat)

map = folium.Map(location=[lat, lon], zoom_start=13)
folium.Marker([lat, lon], popup=postcode).add_to(map)
with open('/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/glasgow_restaurants.json') as f:
    locations = json.load(f)
marker_group = folium.FeatureGroup(name="Improvement Required Locations")

icon = folium.CustomIcon(
    icon_image='/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/res_img.png',
    icon_size=(40, 40)
)

# Add filtered markers
for loc in locations:
    if postcode in loc["PostCode"]:
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
        marker_group.add_to(map)
        map.save("static/postcode_map.html")
#return render_template("postcode_map.html")