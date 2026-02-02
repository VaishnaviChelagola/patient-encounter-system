# Medical Encounter Management System (MEMS)

## Project Overview
MEMS is a backend system for managing medical encounters in a clinic. It handles patients, doctors, and appointments with timezone-aware scheduling. API-only backend with conflict prevention and future-only appointments.

## Features
- Create and retrieve patients and doctors  
- Schedule appointments without overlaps  
- Timezone-aware datetime handling  
- API endpoints for patients, doctors, and appointments  

## Tech Used
Python 3.9+, FastAPI, SQLAlchemy, Pydantic, MySQL, Alembic (for migrations), Pytest (testing), GitHub Actions (CI/CD)  

## How to Run
* Clone the repository: 
  `git clone <repo-url>`
* Navigate into the folder:
   `cd patient-encounter-system`
* Install dependencies:
   `pip install -r requirements.txt`
* Run the application: 
  `uvicorn src.main:app --reload`
* Access API docs at 
  `http://127.0.0.1:8000/docs`
