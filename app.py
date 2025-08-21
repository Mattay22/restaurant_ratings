from flask import Flask, render_template, request
import json
from collections import defaultdict
import requests
import folium

app = Flask(__name__)

# Load and index data once at startup
#with open('/Users/matthewmaloy/projects/python/restaurant_ratings/application/data_source/glasgow_restaurants.json') as f:
#    data = json.load(f)

with open('data_source/glasgow_restaurants.json') as f:
    data = json.load(f)

# Index by lowercase business name
name_index = {
    e["BusinessName"].lower(): e
    for e in data
    if e.get("BusinessName")
}

@app.route('/')
def home():
    return render_template("base.html")  # Your main layout

@app.route('/map')
def map():
    return render_template("map_embed.html")  # Just the map

@app.route('/search')
def search():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return render_template("search_results.html", results=[], query=query)

    # Case-insensitive partial match
    results = [
        e for name, e in name_index.items()
        if query in name
    ]

    # Add Google Maps link to each result
    for r in results:
        lat = r.get("geocode", {}).get("latitude")
        lon = r.get("geocode", {}).get("longitude")
        if lat and lon:
            r["google_maps_url"] = f"https://www.google.com/maps?q={lat},{lon}"

    return render_template("search_results.html", results=results, query=query)

@app.route('/postcode-summary', methods=['POST', 'GET'])
def postcode_summary():
    partial_postcode = request.form.get('postcode', 'G1').strip().upper()

    ### This will cause issue if there are postcodes with two chars i.e IV12
    if len(partial_postcode) == 2:
        partial_postcode = f"{partial_postcode} "
    if len(partial_postcode) > 3:
        partial_postcode = partial_postcode[:3]

    results = [b for b in data if b['PostCode'].startswith(partial_postcode)]

    total = len(results)
    passed = sum(1 for b in results if b['RatingValue'] == 'Pass')
    failed = sum(1 for b in results if b['RatingValue'] == 'Improvement Required')

    percent_passed = round((passed / total) * 100, 1) if total else 0
    percent_failed = round((failed / total) * 100, 1) if total else 0

    postcode_summary = {
        'postcode': partial_postcode,
        'total': total,
        'percent_passed': percent_passed,
        'percent_failed': percent_failed
    }

    # Geocode the postcode prefix
    url = f"https://api.postcodes.io/outcodes/{partial_postcode}"
    response = requests.get(url).json()

    if not response.get("result"):
        return render_template("postcode_returned.html", error="Invalid postcode prefix")

    lat = response["result"]["latitude"]
    lon = response["result"]["longitude"]

    # Create map and marker group
    map = folium.Map(location=[lat, lon], zoom_start=13)
    marker_group = folium.FeatureGroup(name="Improvement Required Locations")

    icon = folium.CustomIcon(
        icon_image='data_source/res_img.png',  # Move image to static folder for Flask
        icon_size=(40, 40)
    )

    # Add central marker
    folium.Marker([lat, lon], popup=f"{partial_postcode} region").add_to(map)

    # Add business markers
    for loc in data:
        if partial_postcode in loc["PostCode"]:
            latitude = loc['geocode']['latitude']
            longitude = loc['geocode']['longitude']
            name = loc['BusinessName']
            rating = loc["RatingValue"]
            address = loc["AddressLine2"]
            postcode = loc["PostCode"]
            business_type = loc["BusinessType"]

            if not latitude or "Retailers" in business_type or rating != "Improvement Required":
                continue

            popup_html = f"""
            <b>{name}</b><br>
            Rating: {rating}<br>
            Address: {address}<br>
            Postcode: {postcode}<br>
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

    return render_template("postcode_returned.html", postcode_summary=postcode_summary)

@app.route('/postcode-rankings')
def postcode_rankings():

    postcode_groups = defaultdict(list)

    for b in data:
        postcode = b['PostCode'][:3].upper()  # Use first 3 chars as partial postcode
        if postcode == "":
            postcode = "Missing Data"
        postcode_groups[postcode].append(b)

    rankings = []

    for postcode, businesses in postcode_groups.items():
        
        total = len(businesses)
        passed = sum(1 for b in businesses if b['RatingValue'] == 'Pass')
        failed = sum(1 for b in businesses if b['RatingValue'] == 'Improvement Required')
        awaiting_inspection = sum(1 for b in businesses if b['RatingValue'] == 'Awaiting Inspection')
        percent_passed = round((passed / total) * 100, 1) if total else 0
        percent_failed = round((failed / total) * 100, 1) if total else 0
        percent_awaiting_inspection = round((awaiting_inspection / total) * 100, 1) if total else 0


        rankings.append({
            'postcode': postcode,
            'total': total,
            'percent_passed': percent_passed,
            'percent_failed': percent_failed,
            'percent_awaiting_inspection': percent_awaiting_inspection
        })

    # Sort by best hygiene performance
    rankings.sort(key=lambda x: x['postcode'])


    return render_template("rankings.html", rankings=rankings)

@app.route('/violation-reasons')
def violation_reasons():

    return render_template("violation_reasons.html")


if __name__ == '__main__':
    app.run(debug=True)

