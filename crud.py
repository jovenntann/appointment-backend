from sqlalchemy.orm import Session
import models, schemas

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



# CRUD: User Type


# async def authenticate_user(email: str, password: str):
#     db_user = await crud.authenticate_user(db, email=email, password=password)
#     if not user:
#         return False 
#     if not user.verify_password(password):
#         return False
#     return db_user

def authenticate_user(db: Session,email: str, hashed_password: str):

    return db.query(models.User).filter(models.User.email == email, models.User.hashed_password == hashed_password).first()

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

def create_user(db: Session, user: schemas.UserCreate):
    
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, user_type_id=user.user_type_id, status_id=user.status_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



# CRUD: Appointments

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    
    db_appointment = models.Appointment(
        patient_name=appointment.patient_name,
        scheduled_from=appointment.scheduled_from,
        scheduled_to=appointment.scheduled_to,
        user_id=appointment.user_id,
        comments=appointment.comments
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment

def get_appointments(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Appointment).offset(skip).limit(limit).all()



# CRUD: Items

def get_items(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


