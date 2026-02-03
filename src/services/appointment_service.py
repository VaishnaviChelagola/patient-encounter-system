from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, status
from src.models.appointment import Appointment
from src.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, appointment_in: AppointmentCreate) -> Appointment:
    start_time = appointment_in.scheduled_start
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    new_end = start_time + timedelta(minutes=appointment_in.duration)

    # Reject past appointments
    if start_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create appointment in the past",
        )

    existing_appointments = (
        db.query(Appointment)
        .filter(Appointment.doctor_id == appointment_in.doctor_id)
        .all()
    )

    for appt in existing_appointments:
        existing_start = appt.scheduled_start

        # Make DB datetime timezone-aware
        if existing_start.tzinfo is None:
            existing_start = existing_start.replace(tzinfo=timezone.utc)

        existing_end = existing_start + timedelta(minutes=appt.duration)

        if start_time < existing_end and new_end > existing_start:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Doctor already has an appointment during this time",
            )

    appointment = Appointment(**appointment_in.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def list_appointments(db: Session, date, doctor_id=None):

    query = (
        db.query(Appointment)
        .filter(text("DATE(scheduled_start) = :date"))
        .params(date=date)
    )

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    return query.all()
