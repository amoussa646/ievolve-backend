from pydantic import BaseModel, EmailStr
from typing import List, Optional,Dict,Any
from datetime import datetime
from datetime import date

from app.models import Activity

class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str

class UserUpdateRequest(BaseRequest):
    email: Optional[str] = None 
    first_name: Optional[str] = None 
    last_name: Optional[str] = None 
    phone_number: Optional[str] = None 
    address: Optional[str] = None 
    latitude: Optional[str] = None 
    longitude: Optional[str] = None 


class UserCreateRequest(BaseRequest):
    email: str
    password: str
    # first_name: str
    # last_name: str
    # phone_number: str
    # address: str
    # latitude: str
    # longitude: str
    
class ActivityCreateRequest(BaseRequest):
    start: str
    date:str
class ActivitySchema(BaseModel):
    start: datetime
    end: datetime
    activity: str
    # Add other fields here

class HabitCreateRequest(BaseModel):
    id: Optional[str]
    name: str
    user_id: Optional[int] = None  # Assuming user_id is optional for creating a habit
    frequency : Optional[str] = None

class DayPlanSchema(BaseModel):
    id:  Optional[str] = None
    user_id:  Optional[str] = None
    date:  Optional[str] = None
    dayplan :Optional[List[ActivitySchema]]= []
    class Config:
        arbitrary_types_allowed = True

class ActivitySchema(BaseModel):
    id:  Optional[str] = None
    user_id:  Optional[str] = None
    date:  Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    activity: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True

class ActivityEndRequest(BaseRequest):
    id: str
    end: str
    activity: str
    duration: str

    ########################################today's stuff #####################################33

class TodayPlanCreate(BaseModel):
    date: Optional[str]= None
    full_score: int
    current_score: int
    activities: List[Dict[str, Any]]  # List of activities as dictionaries
    habits: List[Dict[str, Any]]  # List of habits as dictionaries
    user_id: Optional[int] = None
