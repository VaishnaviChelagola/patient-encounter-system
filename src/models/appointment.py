from sqlalchemy import ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from src.database import Base


class Appointment(Base):
    __tablename__ = "vaishnaviCH_appointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign Key references
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("vaishnaviCH_patients.id"),
        nullable=False,
        index=True,
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("vaishnaviCH_doctors.id"),
        nullable=False,
        index=True,
    )

    # Appointment start time (UTC)
    scheduled_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Duration in minutes
    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Audit timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationships (for querying convenience)
    patient = relationship("Patient", back_populates="appointments")

    doctor = relationship("Doctor", back_populates="appointments")

    # Derived: Calculate end time dynamically
    @property
    def scheduled_end(self) -> datetime:
        return self.scheduled_start + timedelta(minutes=self.duration)
