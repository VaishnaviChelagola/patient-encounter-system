from sqlalchemy.orm import Session
from src.patient_encounter_system.models.patient import Patient
from src.patient_encounter_system.schemas.patient import PatientCreate
from fastapi import HTTPException


def create_patient(db: Session, patient_in: PatientCreate) -> Patient:
    # Check if email already exist
    print("STEP 1: entering service")

    existing = db.query(Patient).filter(Patient.email == patient_in.email).first()

    print("STEP 2: checked existing patient")

    if existing:
        print("STEP 3: patient already exists")
        return existing

    patient = Patient(**patient_in.dict())
    print("STEP 4: patient object created")

    db.add(patient)
    print("STEP 5: added to session")

    db.commit()
    print("STEP 6: committed")

    db.refresh(patient)
    print("STEP 7: refreshed")

    return patient

    """existing = db.query(Patient).filter(Patient.email == patient_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    patient = Patient(
        first_name=patient_in.first_name,
        last_name=patient_in.last_name,
        email=patient_in.email,
        phone=patient_in.phone,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient"""


def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
