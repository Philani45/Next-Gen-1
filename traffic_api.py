import requests
import os

# IMPORTANT:
# Replace this with your actual Google Maps API key.
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "YOUR_API_KEY_HERE")

def get_traffic_time(origin: str, destination: str) -> int:
    """
    Returns travel time in seconds between origin and destination
    using Google Maps Directions API with traffic.
    """

    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Validate response
    if "routes" not in data or len(data["routes"]) == 0:
        raise Exception("No route found from Google Maps API")

    leg = data["routes"][0]["legs"][0]

    # Prefer traffic-adjusted time if available
    if "duration_in_traffic" in leg:
        return leg["duration_in_traffic"]["value"]

    # Fallback to normal duration
    return leg["duration"]["value"]
