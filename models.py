import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Status(Base): 

    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class UserType(Base):

    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name =  Column(String)
    profile_pic = Column(String)
    is_active = Column(Boolean, default=True)
    # User has one User Type
    user_type_id = Column(Integer, ForeignKey("user_type.id"))
    # User has one Status
    status_id = Column(Integer, ForeignKey("status.id"))
    # User has many items
    items = relationship("Item", back_populates="owner")
    # User has many appointments
    appointments = relationship("Appointment", back_populates="user")
    
class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_first_name = Column(String)
    patient_last_name = Column(String)
    scheduled_from = Column(DateTime)
    scheduled_to = Column(DateTime)
    comments = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Link to User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="appointments")

    # Link to Appointment Status
    appointment_status_id = Column(Integer, ForeignKey("appointment_status.id"))
    appointment_status = relationship("AppointmentStatus", back_populates="appointments")

class AppointmentStatus(Base):

    __tablename__ = "appointment_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    appointments = relationship("Appointment", back_populates="appointment_status")

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    # Items belong to one User
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")