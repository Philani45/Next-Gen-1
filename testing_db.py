from database import SessionLocal
from models import User, Schedule
from datetime import datetime

db = SessionLocal()

new_user = User(
    name="Test User",
    email="tester1aiham@example.com",
    password="123456969",
    home_address="420 Main Dope Street"
)

db.add(new_user)
db.commit()
db.refresh(new_user)
print("User created:", new_user.user_id)

new_schedule = Schedule(
    user_id=new_user.user_id,
    class_name="Math 1101",
    building_location="Langdale Hall",
    start_time=datetime(2025, 1, 1, 9, 0)
)

db.add(new_schedule)
db.commit()
db.refresh(new_schedule)
print("Schedule created:", new_schedule.schedule_id)

db.close()
