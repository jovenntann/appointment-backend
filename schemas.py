from typing import List, Optional
from pydantic import BaseModel
import datetime

# ====================================================================================================
# STATUS SCHEMA: User Statuses | Available, Unavailable
# ====================================================================================================

class StatusBase(BaseModel):

    pass

class StatusCreate(StatusBase):

    name: str

class Status(StatusBase):
    
    id: int
    name: str
    
    class Config:
        orm_mode = True

# ====================================================================================================
# USER TYPE SCHEMA: User Type: Scheduler, Doctor
# ====================================================================================================

class UserTypeBase(BaseModel):

    pass

class UserTypeCreate(UserTypeBase):

    title: str

class UserType(UserTypeBase):
    
    id: int
    title: str
    
    class Config:
        orm_mode = True

# ====================================================================================================
# ITEMM SCHEMA: User Items
# ====================================================================================================

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

# ====================================================================================================
# APPOINTMENT STATUS SCHEMA: Pending, Accepted, Rejected
# ====================================================================================================

class AppointmentStatusBase(BaseModel):

    pass

class AppointmentStatusCreate(AppointmentStatusBase):

    name: str

class AppointmentStatus(AppointmentStatusBase):
    
    id: int
    name: str
    
    class Config:
        orm_mode = True

# ====================================================================================================
# APPOINTMENT SCHEMA: User = Doctor Appointments
# ====================================================================================================

class AppointmentBase(BaseModel):

    pass

class AppointmentCreate(AppointmentBase):

    patient_first_name: str
    patient_last_name: str
    scheduled_from: datetime.datetime
    scheduled_to: datetime.datetime
    user_id: int
    comments: str
    appointment_status_id: int

class Appointment(AppointmentBase):

    id: int
    patient_first_name: str
    patient_last_name: str
    scheduled_from: datetime.datetime
    scheduled_to: datetime.datetime
    user_id: int
    appointment_status_id: int
    comments: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# ====================================================================================================
# USER SCHEMA: Users | All Users 
# ====================================================================================================

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
    email: str
    first_name: str
    last_name: str
    profile_pic: str
    is_active: bool
    items: List[Item] = []
    user_type_id: int
    status_id: int
    appointments: List[Appointment] = []

    class Config:
        orm_mode = True

