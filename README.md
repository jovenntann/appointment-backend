# Create Conda Environment
conda create --name backendenv python=3.8
conda activate backendenv

# Install Fast API
pip install fastapi
pip install uvicorn

# API Docs
http://localhost:8000/docs # Swagger
http://localhost:8000/redoc # ReDoc

# Uvicorn commands
uvicorn main:app --reload

