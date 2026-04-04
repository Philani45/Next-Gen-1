from datetime import timedelta

def calculate_departure(class_start_time, travel_seconds: int):
    """
    Subtracts travel time from class start time to compute
    the recommended departure datetime.
    """

    travel_delta = timedelta(seconds=travel_seconds)
    recommended_departure = class_start_time - travel_delta

    return recommended_departure
