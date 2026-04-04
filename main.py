from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import UserCreate, UserResponse, ScheduleCreate, ScheduleResponse
from recommendation_service import get_recommended_departure_time

app = FastAPI()

# -------------------------
# USER ENDPOINTS
# -------------------------

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = crud.create_user(
        db,
        name=user.name,
        email=user.email,
        password=user.password,
        home_address=user.home_address
    )
    return new_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------------
# SCHEDULE ENDPOINTS
# -------------------------

@app.post("/schedules/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, schedule.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_schedule = crud.create_schedule(
        db,
        user_id=schedule.user_id,
        class_name=schedule.class_name,
        building_location=schedule.building_location,
        start_time=schedule.start_time
    )
    return new_schedule


@app.get("/schedules/{user_id}", response_model=list[ScheduleResponse])
def get_schedules(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_schedules(db, user_id)


# -------------------------
# RECOMMENDATION ENDPOINT
# -------------------------

@app.get("/recommendation/{user_id}")
def get_recommendation(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    schedules = crud.get_user_schedules(db, user_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found")

    # For now, use the first schedule
    schedule = schedules[0]

    recommended_time = get_recommended_departure_time(
        user.home_address,
        schedule.building_location,
        schedule.start_time
    )

    return {
        "user_id": user_id,
        "class_name": schedule.class_name,
        "recommended_departure": recommended_time
    }
