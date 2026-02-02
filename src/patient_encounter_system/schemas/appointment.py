from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)

    scheduled_start: datetime = Field(
        ...,
        description="Timezone-aware appointment start datetime",
    )

    duration_minutes: int = Field(
        ...,
        gt=0,
        le=480,  # max 8 hours
    )

    @field_validator("scheduled_start")
    @classmethod
    def validate_timezone(cls, value: datetime):
        if value.tzinfo is None:
            raise ValueError("scheduled_start must include timezone information")
        return value


class AppointmentRead(BaseModel):
    id: int = Field(..., gt=0)
    patient_id: int
    doctor_id: int
    scheduled_start: datetime
    duration_minutes: int
    created_at: datetime

    # Derived field (not stored)
    scheduled_end: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.scheduled_end = obj.scheduled_end
        return data
