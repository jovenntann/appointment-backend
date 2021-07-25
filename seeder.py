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
        db_object = models.User(email=user['email'], password=user['password'], user_type_id=user['user_type_id'], status_id=user['status_id'])
        db.add(db_object)
    db.commit()
    print("Seeding: Users Completed")

    print("Seeding: Appointments..")
    for appointment in jsonData['appointments']:
        db_object = models.Appointment(
            patient_name=appointment['patient_name'],
            scheduled_from=func.now(),
            scheduled_to=func.now(),
            user_id=appointment['user_id'],
            comments=appointment['comments']
        )
        db.add(db_object)
    db.commit()
    print("Seeding: Appointments Completed")

    # db.refresh(db_object)

    return db_object
