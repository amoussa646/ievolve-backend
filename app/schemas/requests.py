from pydantic import BaseModel, EmailStr
from typing import List, Optional
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
class DayPlanCreateRequest(BaseRequest):
    date:str
class HabitCreateRequest(BaseRequest):
    name:str
class DayPlanSchema(BaseModel):
    id:  Optional[str] = None
    user_id:  Optional[str] = None
    date:  Optional[str] = None
    dayplan :Optional[list["Activity"] ]="" 
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

class ItemCreateRequest(BaseModel):
    name: str
    price : str
    description: Optional[str] = None  # Make description optional
    ingredients: Optional[str] = None  # Make ingredients optional
    image_url: Optional[str] = None  # Make image_url optional
    category: Optional[str] = None  # Make category optional
    sub_category: Optional[str] = None  # Make sub_category optional
    extra_attributes: Optional[dict] = None

class OrderCreateRequest(BaseModel):
    chef_id: str
    items_ids: List[str]
    quantities: List[str]
    total_price: str
    final_price: str
    delivery_cost: str
    tax_service : str



    