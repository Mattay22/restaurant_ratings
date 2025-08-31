import requests
import json

url_base = "https://api.ratings.food.gov.uk/ratings"

headers = {
    "Accept": "application/json",
    "x-api-version": "2"
}

response = requests.get(url_base, headers=headers)
data = response.json()

print(data)