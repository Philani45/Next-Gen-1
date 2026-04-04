from pydantic import BaseModel
from datetime import datetime

# -------------------------
# USER SCHEMAS
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    home_address: str


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    home_address: str

    model_config = {
        "from_attributes": True
    }


# -------------------------
# SCHEDULE SCHEMAS
# -------------------------

class ScheduleCreate(BaseModel):
    user_id: int
    class_name: str
    building_location: str
    start_time: datetime


class ScheduleResponse(BaseModel):
    schedule_id: int
    user_id: int
    class_name: str
    building_location: str
    start_time: datetime

    model_config = {
        "from_attributes": True
    }
