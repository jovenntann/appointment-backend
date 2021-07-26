import models
import json
from sqlalchemy.sql import func

def seed(db):

    jsonFile = open('seed.json',)
    jsonData = json.load(jsonFile) 

    print("Seeding: Status..")
    for data in jsonData['status']:
        db_object = models.Status(name=data)
        db.add(db_object)
    db.commit()
    print("Seeding: Status Completed")

    print("Seeding: User Type..")
    for data in jsonData['user_type']:
        db_object = models.UserType(title=data)
        db.add(db_object)
    db.commit()
    print("Seeding: User Type Completed")

    print("Seeding: Users..")
    for user in jsonData['users']:
        db_object = models.User(
            email=user['email'], 
            password=user['password'], 
            first_name=user['first_name'], 
            last_name=user['last_name'],
            profile_pic=user['profile_pic'],
            user_type_id=user['user_type_id'], 
            status_id=user['status_id']
        )
        db.add(db_object)
    db.commit()
    print("Seeding: Users Completed")

    print("Seeding: Appointment Status..")
    for data in jsonData['appointment_status']:
        db_object = models.AppointmentStatus(name=data)
        db.add(db_object)
    db.commit()
    print("Seeding: Appointment Status Completed")

    print("Seeding: Appointments..")
    for appointment in jsonData['appointments']:
        db_object = models.Appointment(
            patient_first_name=appointment['patient_first_name'],
            patient_last_name=appointment['patient_last_name'],
            scheduled_from=func.now(),
            scheduled_to=func.now(),
            user_id=appointment['user_id'],
            appointment_status_id=appointment['appointment_status_id'],
            comments=appointment['comments']
        )
        db.add(db_object)
    db.commit()
    print("Seeding: Appointments Completed")

    db.refresh(db_object)

    return db_object
