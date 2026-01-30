from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class PatientCreate(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: str = Field(..., max_length=20)


class PatientRead(BaseModel):
    id: int = Field(..., gt=0)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
