from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import json

# Database
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models, schemas
from seeder import seed

models.Base.metadata.create_all(bind=engine)

# Initialize
app = FastAPI()

# CORS: WhiteList
origins = ["http://localhost:8080",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================================================================================
# Seeder: (Optional)
# =====================================================================================================================

seed(SessionLocal())

# =====================================================================================================================
# Authentication
# =====================================================================================================================

JWT_SECRET = 'supersecretjwt'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    db_user = crud.authenticate_user(db, form_data.username, form_data.password)
    
    if db_user:
        payload = {
            "email": db_user.email,
            "user_type_id": db_user.user_type_id
        }
        token = jwt.encode({"data":payload}, JWT_SECRET)
        return {'access_token' : token, 'token_type' : 'bearer', 'user_type_id':db_user.user_type_id}
    else:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid email or password'
        )

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        email = payload['data']['email']
        user_type_id = payload['data']['user_type_id']
        db_user = crud.get_user_by_email(db, email=email)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Unathorized'
        )
    return db_user


# =====================================================================================================================
# Administration
# =====================================================================================================================

# Status

@app.post("/status/", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    db_status = crud.get_status_by_name(db, name=status.name)
    if db_status:
        raise HTTPException(status_code=400, detail="Status Name already registered")
    return crud.create_status(db=db, status=status)

@app.get("/status/", response_model=List[schemas.Status])
def read_status(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    status = crud.get_status(db, skip=skip, limit=limit)
    return status

# User Type

@app.post("/user_type/", response_model=schemas.UserType)
def create_user_type(user_type: schemas.UserTypeCreate, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    db_user_type = crud.get_user_type_by_title(db, title=user_type.title)
    if db_user_type:
        raise HTTPException(status_code=400, detail="User Type already registered")
    return crud.create_user_type(db=db, user_type=user_type)

@app.get("/user_type/", response_model=List[schemas.UserType])
def read_user_type(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    user_type = crud.get_user_type(db, skip=skip, limit=limit)
    return user_type

# Users 

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# =====================================================================================================================
# Scheduler API
# =====================================================================================================================

# Doctors

@app.get("/doctors/", response_model=List[schemas.User])
def get_doctors(db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    users = crud.get_users_by_user_type(db)
    return users

# Appointment Status

@app.get("/appointment/status/", response_model=List[schemas.AppointmentStatus])
def read_appointment_status(db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    appointment_status = crud.get_appointment_status(db)
    return appointment_status

# Appointments

@app.post("/appointments/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    return crud.create_appointment(db=db, appointment=appointment)

@app.get("/appointments/", response_model=List[schemas.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments


# =====================================================================================================================
# REFERENCES API
# =====================================================================================================================

# Items
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), currentUser: object = Depends(get_current_user)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items