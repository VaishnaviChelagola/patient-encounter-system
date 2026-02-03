from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.database import get_db, Base, engine

# from src.patient_encounter_system.models.patient import Patient
# from src.patient_encounter_system.models.doctor import Doctor
# from src.patient_encounter_system.models.appointment import Encounter
from src.schemas.patient import PatientCreate, PatientRead
from src.schemas.doctor import DoctorCreate, DoctorRead
from src.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
)
from src.services import (
    patient_service,
    doctor_service,
    appointment_service,
)

app = FastAPI(title="Patient Encounter System API")


@app.on_event("startup")
def startup():
    # Create tables if they don't exist (this will run only on app startup)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


# ------------------- Patient Endpoints -------------------


@app.post("/patients", response_model=PatientRead, status_code=201)
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    print("Received patient:", patient_in)
    return patient_service.create_patient(db, patient_in)


@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_service.get_patient(db, patient_id)


# ------------------- Doctor Endpoints -------------------


@app.post("/doctors", response_model=DoctorRead, status_code=201)
def create_doctor(doctor_in: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.create_doctor(db, doctor_in)


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_service.get_doctor(db, doctor_id)


# ------------------- Appointment Endpoints -------------------


@app.post("/appointments", response_model=AppointmentRead, status_code=201)
def create_appointment(
    appointment_in: AppointmentCreate, db: Session = Depends(get_db)
):
    return appointment_service.create_appointment(db, appointment_in)


@app.get("/appointments", response_model=list[AppointmentRead])
def list_appointments(
    appointment_date: str,
    doctor_id: int | None = None,
    db: Session = Depends(get_db),
):
    return appointment_service.list_appointments(db, appointment_date, doctor_id)


@app.get("/health")
async def health_check():
    return {"status": "UP"}
