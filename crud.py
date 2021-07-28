from sqlalchemy.orm import Session
from sqlalchemy.orm import defer
from sqlalchemy.orm import undefer
import models, schemas

# CRUD: Authentication

def authenticate_user(db: Session,email: str, password: str):

    return db.query(models.User).filter(models.User.email == email, models.User.password == password).first()

# CRUD: Status

def get_status_by_name(db: Session, name: str):

    return db.query(models.Status).filter(models.Status.name == name).first()

def create_status(db: Session, status: schemas.StatusCreate):
    
    db_status = models.Status(name=status.name)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)

    return db_status
    
def get_status(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Status).offset(skip).limit(limit).all()


# CRUD User Type

def get_user_type_by_title(db: Session, title: str):

    return db.query(models.UserType).filter(models.UserType.title == title).first()

def create_user_type(db: Session, user_type: schemas.UserTypeCreate):
    
    db_user_type = models.UserType(title=user_type.title)
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)

    return db_user_type

def get_user_type(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.UserType).offset(skip).limit(limit).all()



# CRUD: Users

def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_by_user_type(db: Session):

    return db.query(models.User).filter(models.User.user_type_id == 2).all()

def create_user(db: Session, user: schemas.UserCreate):
    
    db_user = models.User(email=user.email, password=user.password, first_name=user.first_name, last_name=user.last_name, profile_pic=user.profile_pic, user_type_id=user.user_type_id, status_id=user.status_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# CRUD: Appointment Status

def get_appointment_status(db: Session):

    return db.query(models.AppointmentStatus).all()

# CRUD: Appointments

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    
    db_appointment = models.Appointment(
        patient_first_name=appointment.patient_first_name,
        patient_last_name=appointment.patient_last_name,
        scheduled_from=appointment.scheduled_from,
        scheduled_to=appointment.scheduled_to,
        user_id=appointment.user_id,
        appointment_status_id=appointment.appointment_status_id,
        comments=appointment.comments
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment

# Scheduler: Appointments
def get_appointments(db: Session):
    # Custom Format Query Result
    queryResult = db.query(models.Appointment,models.AppointmentStatus).join(models.AppointmentStatus).all()
    formattedDict = []
    for i in queryResult:
        if (i.Appointment.user_id):
            appointment = i.Appointment.__dict__
            appointmentStatus = i.AppointmentStatus.__dict__
            # Get User Info # Remove Password column
            userQueryResult = db.query(models.User).options(defer('password')).filter(models.User.id == i.Appointment.user_id).first()
            user = userQueryResult.__dict__
            formattedDict.append({"appointment":appointment,"appointment_status":appointmentStatus,"user":user})
        else:
            appointment = i.Appointment.__dict__
            appointmentStatus = i.AppointmentStatus.__dict__
            formattedDict.append({"appointment":appointment,"appointment_status":appointmentStatus})

    return formattedDict

def delete_appointment(db: Session,appointment_id: int):
    db.query(models.Appointment).filter(models.Appointment.id == appointment_id).delete()
    db.commit()
    return {"message":"deleted"}

# Doctor: Appointments
def get_my_appointments(db: Session,currentUserId: int):
    # Custom Format Query Result
    queryResult = db.query(models.Appointment,models.AppointmentStatus).join(models.AppointmentStatus).filter(models.Appointment.user_id == currentUserId).all()
    formattedDict = []
    for i in queryResult:
        if (i.Appointment.user_id):
            appointment = i.Appointment.__dict__
            appointmentStatus = i.AppointmentStatus.__dict__
            # Get User Info # Remove Password column
            userQueryResult = db.query(models.User).options(defer('password')).filter(models.User.id == i.Appointment.user_id).first()
            user = userQueryResult.__dict__
            formattedDict.append({"appointment":appointment,"appointment_status":appointmentStatus,"user":user})
        else:
            appointment = i.Appointment.__dict__
            appointmentStatus = i.AppointmentStatus.__dict__
            formattedDict.append({"appointment":appointment,"appointment_status":appointmentStatus})

    return formattedDict

# Doctor: Appointments: Pending
def get_my_appointments_pending(db: Session,currentUserId: int):
    # Custom Format Query Result
    queryResult = db.query(models.Appointment,models.AppointmentStatus).join(models.AppointmentStatus).filter(models.Appointment.user_id == currentUserId,models.Appointment.appointment_status_id == 1).all()
    formattedDict = []
    for i in queryResult:
        if (i.Appointment.user_id):
            appointment = i.Appointment.__dict__
            appointmentStatus = i.AppointmentStatus.__dict__
            # Get User Info # Remove Password column
            userQueryResult = db.query(models.User).options(defer('password')).filter(models.User.id == i.Appointment.user_id).first()
            user = userQueryResult.__dict__
            formattedDict.append({"appointment":appointment,"appointment_status":appointmentStatus,"user":user})
        else:
            appointment = i.Appointment.__dict__
            appointmentStatus = i.AppointmentStatus.__dict__
            formattedDict.append({"appointment":appointment,"appointment_status":appointmentStatus})

    return formattedDict

def get_appointment(db: Session,currentUserId: int,appointment_id: int):
    queryResult = db.query(models.Appointment,models.User,models.AppointmentStatus).join(models.AppointmentStatus,models.User).filter(models.Appointment.id == appointment_id).first()
    return queryResult
    
def update_appointment(db: Session,currentUserId: int,appointment_id: int,appointment):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    db_appointment.user_id = currentUserId
    db_appointment.appointment_status_id = appointment.appointment_status_id
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# CRUD: Items

def get_items(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):

    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item



