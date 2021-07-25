from typing import List, Optional
from pydantic import BaseModel
import datetime

# Status Schemas

class StatusBase(BaseModel):

    name: str

class StatusCreate(StatusBase):

    name: str

class Status(StatusBase):
    
    id: int
    name: str
    
    class Config:
        orm_mode = True


# User Type Schemas

class UserTypeBase(BaseModel):

    title: str

class UserTypeCreate(UserTypeBase):

    title: str

class UserType(UserTypeBase):
    
    id: int
    title: str
    
    class Config:
        orm_mode = True




# Item Schemas

class ItemBase(BaseModel):

    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):

    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



# User Schemas

class UserBase(BaseModel):

    email: str

class UserCreate(UserBase):

    password: str
    user_type_id: int
    status_id: int

class User(UserBase):

    id: int
    is_active: bool
    items: List[Item] = []
    user_type_id: int
    status_id: int

    class Config:
        orm_mode = True






# Appointment Schemas

class AppointmentBase(BaseModel):

    patient_name: str

class AppointmentCreate(AppointmentBase):

    patient_name: str
    scheduled_from: datetime.datetime
    scheduled_to: datetime.datetime
    user_id: int
    comments: str

class Appointment(AppointmentBase):

    id: int
    patient_name: str
    scheduled_from: datetime.datetime
    scheduled_to: datetime.datetime
    user_id: int
    comments: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# https://pydantic-docs.helpmanual.io/usage/types/
# Date Time Format: 2020-04-02 14:30:21






