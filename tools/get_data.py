import requests
import json
url = "https://api.ratings.food.gov.uk/Establishments?localAuthorityId=213"
headers = {
    "Accept": "application/json",
    "x-api-version": "2"
}

response = requests.get(url, headers=headers)

output = response.json()

with open("glasgow_restraunts.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)
