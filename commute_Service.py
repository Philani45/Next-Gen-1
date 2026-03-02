from datetime import timedelta

def calculate_departure(class_start, traffic_seconds):
    parking_buffer = 600   # 10 minutes
    walking_buffer = 480   # 8 minutes

    total_seconds = traffic_seconds + parking_buffer + walking_buffer

    return class_start - timedelta(seconds=total_seconds)