from sqlalchemy.orm import Session
from models import User, Schedule

# -------------------------
# USER CRUD
# -------------------------

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, name: str, email: str, password: str, home_address: str):
    user = User(
        name=name,
        email=email,
        password=password,
        home_address=home_address
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# -------------------------
# SCHEDULE CRUD
# -------------------------

def create_schedule(db: Session, user_id: int, class_name: str, building_location: str, start_time):
    schedule = Schedule(
        user_id=user_id,
        class_name=class_name,
        building_location=building_location,
        start_time=start_time
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

def get_user_schedules(db: Session, user_id: int):
    return db.query(Schedule).filter(Schedule.user_id == user_id).all()
