from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class UserContactData(SQLModel, table=True):
    __tablename__ = "user_contact_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    email_unal: str = Field(foreign_key="user_unal.email_unal", max_length=100)
    personal_email: Optional[str] = Field(default=None, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    vehicle_plate: Optional[str] = Field(default=None, max_length=20)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
