from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, status
from src.patient_encounter_system.models.appointment import Encounter
from src.patient_encounter_system.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, appointment_in: AppointmentCreate) -> Encounter:
    new_start = appointment_in.scheduled_start
    if new_start.tzinfo is None:
        new_start = new_start.replace(tzinfo=timezone.utc)

    new_end = new_start + timedelta(minutes=appointment_in.duration_minutes)

    # Reject past appointments
    if new_start < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create appointment in the past",
        )

    existing_appointments = (
        db.query(Encounter)
        .filter(Encounter.doctor_id == appointment_in.doctor_id)
        .all()
    )

    for appt in existing_appointments:
        existing_start = appt.scheduled_start

        # 🔑 Make DB datetime timezone-aware
        if existing_start.tzinfo is None:
            existing_start = existing_start.replace(tzinfo=timezone.utc)

        existing_end = existing_start + timedelta(minutes=appt.duration_minutes)

        if new_start < existing_end and new_end > existing_start:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Doctor already has an appointment during this time",
            )

    appointment = Encounter(**appointment_in.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def list_appointments(db: Session, date, doctor_id=None):

    query = (
        db.query(Encounter)
        .filter(text("DATE(scheduled_start) = :date"))
        .params(date=date)
    )

    if doctor_id:
        query = query.filter(Encounter.doctor_id == doctor_id)

    return query.all()
