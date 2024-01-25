from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int

#################################################################
class UserResponse(BaseResponse):
    id: str
    email: str
    first_name:Optional[str]=""
    last_name: Optional[str]=""
    phone_number: Optional[str]=""
    address:Optional[str]=""

class ActivityResponse(BaseResponse):
    id: Optional[str]=""
    start: Optional[str]=""
    end:Optional[str]=""
    activity:  Optional[str]=""
   


class ItemResponse(BaseModel):
    id: Optional[str]=""
    name:  Optional[str]=""
    id:  Optional[str]=""
    chef_id:  Optional[str]=""
    price:  Optional[str]=""
    ingredients: Optional[str]="" # Optional because it can be None
    image_url: Optional[str]=""  # Optional because it can be None
    category: Optional[str]=""  # Optional because it can be None
    sub_category: Optional[str]=""  # Optional because it can be None
    extra_attributes: Optional[dict]={}
    is_active: Optional[bool] = False
    is_approved: Optional[bool] = False

class OrderResponse(BaseModel):
    id: str
    user_id: str
    chef_id: str
    total_price: str  
    final_price: str
    delivery_cost: str
    tax_service: str
    items_ids: List[str]
    is_chef_received: Optional[bool] = None
    is_chef_accepted: Optional[bool] = None
    is_delivery_received: Optional[bool] = None
    is_delivery_accepted: Optional[bool] = None
    is_paid: Optional[bool] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    order_time: Optional[str] = None
    ready_time: Optional[str] = None
    delivery_time: Optional[str] = None