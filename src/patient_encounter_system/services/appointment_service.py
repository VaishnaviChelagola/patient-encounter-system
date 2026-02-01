from sqlalchemy.orm import Session
from sqlalchemy import and_, text
from datetime import timedelta
from fastapi import HTTPException
from src.patient_encounter_system.models.appointment import Encounter
from src.patient_encounter_system.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, appointment_in: AppointmentCreate) -> Encounter:
    start = appointment_in.scheduled_start
    end = start + timedelta(minutes=appointment_in.duration_minutes)

    # Conflict check using raw SQL for MySQL
    conflict = (
        db.query(Encounter)
        .filter(
            Encounter.doctor_id == appointment_in.doctor_id,
            and_(
                Encounter.scheduled_start < end,
                text(
                    "DATE_ADD(vaishnaviCH_appointments.scheduled_start, "
                    "INTERVAL vaishnaviCH_appointments.duration_minutes MINUTE) > :start"
                ),
            ),
        )
        .params(start=start)
        .first()
    )

    if conflict:
        raise HTTPException(
            status_code=409, detail="Doctor has a conflicting appointment"
        )

    appointment = Encounter(
        patient_id=appointment_in.patient_id,
        doctor_id=appointment_in.doctor_id,
        scheduled_start=start,
        duration_minutes=appointment_in.duration_minutes,
    )
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
