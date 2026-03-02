import requests

def get_traffic_time(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "key": "YOUR_API_KEY"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data["routes"][0]["legs"][0]["duration_in_traffic"]["value"]