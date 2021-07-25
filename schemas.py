from typing import List, Optional
from pydantic import BaseModel
import datetime

# Status Schemas

class StatusBase(BaseModel):

    pass

class StatusCreate(StatusBase):

    name: str

class Status(StatusBase):
    
    id: int
    name: str
    
    class Config:
        orm_mode = True


# User Type Schemas

class UserTypeBase(BaseModel):

    pass

class UserTypeCreate(UserTypeBase):

    title: str

class UserType(UserTypeBase):
    
    id: int
    title: str
    
    class Config:
        orm_mode = True




# Item Schemas

class ItemBase(BaseModel):

    pass

class ItemCreate(ItemBase):

    title: str
    description: Optional[str] = None

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# User Schemas

class UserBase(BaseModel):

    pass

class UserCreate(UserBase):

    email: str
    password: str
    first_name: str
    last_name: str
    profile_pic: str
    user_type_id: int
    status_id: int

class User(UserBase):

    id: int
    first_name: str
    last_name: str
    profile_pic: str
    is_active: bool
    items: List[Item] = []
    user_type_id: int
    status_id: int

    class Config:
        orm_mode = True






# Appointment Schemas

class AppointmentBase(BaseModel):

    pass

class AppointmentCreate(AppointmentBase):

    patient_first_name: str
    patient_last_name: str
    scheduled_from: datetime.datetime
    scheduled_to: datetime.datetime
    user_id: int
    comments: str

class Appointment(AppointmentBase):

    id: int
    patient_first_name: str
    patient_last_name: str
    scheduled_from: datetime.datetime
    scheduled_to: datetime.datetime
    user_id: int
    comments: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# https://pydantic-docs.helpmanual.io/usage/types/
# Date Time Format: 2020-04-02 14:30:21






