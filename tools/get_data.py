import requests
import json

url_base = "https://api.ratings.food.gov.uk/Establishments"

headers = {
    "Accept": "application/json",
    "x-api-version": "2"
}

authoritys = [ 
    213, # glasgow
    216, # North Lanarkshire
    217, # South Lanarkshire
    208, # East Dunbarton
    206, # West Dunbarton
]



all_results = []

for authority in authoritys:
    params = {
        "localAuthorityId": authority,
        "pageSize": 500,  # Max allowed is 500
        "pageNumber": 1
    }

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