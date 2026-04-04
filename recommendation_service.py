from traffic_api import get_traffic_time
from commute_service import calculate_departure

def get_recommended_departure_time(home_address: str, building_location: str, start_time):
    """
    Returns the recommended departure time for a single class.
    """

    # 1. Get travel time in seconds from Google Maps API
    traffic_seconds = get_traffic_time(
        origin=home_address,
        destination=building_location
    )

    # 2. Calculate recommended departure time
    recommended_departure = calculate_departure(start_time, traffic_seconds)

    return {
        "travel_time_seconds": traffic_seconds,
        "recommended_departure": recommended_departure
    }
