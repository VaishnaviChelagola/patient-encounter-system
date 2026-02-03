from sqlalchemy.orm import Session
from src.models.doctor import Doctor
from src.schemas.doctor import DoctorCreate
from fastapi import HTTPException


def create_doctor(db: Session, doctor_in: DoctorCreate) -> Doctor:
    doctor = Doctor(
        full_name=doctor_in.full_name,
        specialization=doctor_in.specialization,
        is_active=True,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor(db: Session, doctor_id: int) -> Doctor:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
