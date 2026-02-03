from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.database import Base


class Doctor(Base):
    __tablename__ = "vaishnaviCH_doctors"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )

    specialization: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="1",  # MySQL-compatible true
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    appointments = relationship("Appointment", back_populates="doctor")
