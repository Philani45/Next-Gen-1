from traffic_api import get_traffic_time
from commute_service import calculate_departure
from crud import get_user_schedules
from sqlalchemy.orm import Session

def get_recommendations_for_user(db: Session, user_id: int):
    schedules = get_user_schedules(db, user_id)
    results = []

    for s in schedules:
        traffic_seconds = get_traffic_time(
            origin=s.owner.home_address,
            destination=s.building_location
        )

        departure = calculate_departure(s.start_time, traffic_seconds)

        results.append({
            "class_name": s.class_name,
            "start_time": s.start_time,
            "traffic_seconds": traffic_seconds,
            "recommended_departure": departure
        })

    return results
