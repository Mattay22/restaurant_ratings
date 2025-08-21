import requests
import json
url = "https://api.ratings.food.gov.uk/Establishments?localAuthorityId=213"
headers = {
    "Accept": "application/json",
    "x-api-version": "2"
}

params = {
    "localAuthorityId": 213,
    "pageSize": 500,  # Max allowed is 500
    "pageNumber": 1
}

all_results = []

while True:
    response = requests.get(url_base, headers=headers, params=params)
    data = response.json()
    establishments = data.get("establishments", [])

    if not establishments:
        break

    all_results.extend(establishments)
    params["pageNumber"] += 1


with open("data_source/glasgow_restaurants.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4)