from pydantic import BaseModel, EmailStr
from typing import Optional


class UserContactDataUpdate(BaseModel):
    personal_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    vehicle_plate: Optional[str] = None
