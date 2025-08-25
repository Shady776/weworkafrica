from datetime import date, time, datetime
from decimal import Decimal
from enum import Enum
from token import OP
from typing import Dict, Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl, validator
from pydantic.types import conint
import re




class User(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    created_at: datetime
    
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str


class UserProfile(BaseModel):
    name: str
    email: str
    phone_number: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None


class Space(BaseModel):
    id: int
    user_id: int
    name_of_space: str
    title: str
    description: str
    state: str
    city: str
    address: str
    type: List[str] 
    price_per_day: Decimal
    price_per_week: Decimal
    price_per_month: Decimal
    rules: List[str] 
    created_at: datetime
    updated_at: datetime
    
class SpaceBase(BaseModel):
    name_of_space: str
    title: str
    description: str
    state: str
    city: str
    address: str
    type: List[str] 
    price_per_day: Decimal
    price_per_week: Decimal
    price_per_month: Decimal
    rules: List[str] 
    # map_link: Optional[HttpUrl]


class SpaceCreate(SpaceBase):
    pass


class SpaceUpdate(SpaceBase):
    pass


class SpaceOut(SpaceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {Decimal: float}


# class AvailabilityBase(BaseModel):
#     start_date: date
#     end_date: date


# class AvailabilityCreate(AvailabilityBase):
#     pass


# class AvailabilityOut(AvailabilityBase):
#     id: int
#     space_id: int

#     class Config:
#         orm_mode = True





class BookingBase(BaseModel):
    start_date: date
    end_date: date
    start_time:time
    end_time: time
    # booking_type: BookingType
    
    
    # @validator("start_time", "end_time", pre=True)
    # def normalize_time(cls, value):
    #     # If user sends "8:00", make it "08:00"
    #     if isinstance(value, str):
    #         # Match formats like H:MM or HH:MM
    #         match = re.match(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", value)
    #         if match:
    #             hour, minute, second = match.groups()
    #             hour = hour.zfill(2)  # pad single digit hour
    #             second = second if second else "00"
    #             return f"{hour}:{minute}:{second}"
    #     return value


class BookingCreate(BookingBase):
    space_id: int
    start_time:time
    end_time:time
    start_date: date
    end_date: date
    class Config:
            use_enum_values = True
            json_encoders = {
            datetime: lambda v: v.strftime("%d/%m/%Y %H:%M %p")  
        }
             
          

class BookingOut(BookingBase):
    id: int
    start_date: date
    end_date: date
    start_time:time
    end_time:time
    space: SpaceBase

    class Config:
        orm_mode = True
        
        
# class SpacePublic(BaseModel):
#     id: int  
#     name: str
#     address: str

#     class Config:
#         orm_mode = True
        