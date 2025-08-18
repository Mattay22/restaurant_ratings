from flask import Flask, render_template, request
import json
from collections import defaultdict

app = Flask(__name__)

# Load and index data once at startup
with open('/Users/matthewmaloy/projects/python/food_hygene/application/data_source/glasgow_restraunts.json') as f:
    data = json.load(f)

# Index by lowercase business name
name_index = {
    e["BusinessName"].lower(): e
    for e in data["establishments"]
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
    partial_postcode = request.form.get('postcode', '').strip().upper()
    results = [b for b in data["establishments"] if b['PostCode'].startswith(partial_postcode)]

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

    return render_template("base.html", postcode_summary=postcode_summary)

from collections import defaultdict

@app.route('/postcode-rankings')
def postcode_rankings():

    postcode_groups = defaultdict(list)

    for b in data["establishments"]:
        postcode = b['PostCode'][:3].upper()  # Use first 3 chars as partial postcode
        if postcode == "":
            postcode = "Missing Data"
        postcode_groups[postcode].append(b)

    rankings = []

    for postcode, businesses in postcode_groups.items():
        
        total = len(businesses)
        passed = sum(1 for b in businesses if b['RatingValue'] == 'Pass')
        failed = sum(1 for b in businesses if b['RatingValue'] == 'Improvement Required')

        percent_passed = round((passed / total) * 100, 1) if total else 0
        percent_failed = round((failed / total) * 100, 1) if total else 0

        rankings.append({
            'postcode': postcode,
            'total': total,
            'percent_passed': percent_passed,
            'percent_failed': percent_failed
        })

    # Sort by best hygiene performance
    rankings.sort(key=lambda x: x['percent_passed'], reverse=True)

    return render_template("rankings.html", rankings=rankings)


if __name__ == '__main__':
    app.run(debug=True)
