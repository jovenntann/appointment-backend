### Create Conda Environment
```
conda create --name backendenv python=3.8
conda activate backendenv
```

### Install Requirements
```
pip install -r requirements.txt
```

###  API Docs

```
http://localhost:8000/docs
http://localhost:8000/redoc
```

### Start Service
```
uvicorn main:app --reload
```

### Demo Users

Scheduler:

email: clairerivera@gmail.com  
password: pass12345

Doctor

email: mikechua@gmail.com  
password: pass12345

