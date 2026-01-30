from pydantic import BaseModel, Field
from datetime import datetime


class DoctorCreate(BaseModel):
    full_name: str = Field(..., max_length=120)
    specialization: str = Field(..., max_length=120)


class DoctorRead(BaseModel):
    id: int = Field(..., gt=0)
    full_name: str
    specialization: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
