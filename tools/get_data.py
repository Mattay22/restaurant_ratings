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
    201, # East Ayrshire
    202, # North Ayrshire
    203, # South Ayrshire
    197, # Aberdeen
    198, # Aberdeenshire
    199, # Angus
    221, # Moray
    205, # Clackmanishire
    210, # Edinburgh
    218, # East Lothain
    220, # Midlothian
    219, # West Lothain
    207, # Dumfries
    204, # Borders
    224, # East Renfrewshire
    211, # Falkirk
    215, # Invercylde
    209, # Dundee City
    212, # Fife
    214, # Highland
    228, # Islands
    226, # Shetland
    222, # Orkney
    223, # Perth
    200, # Argyll
    227 # Stirling




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