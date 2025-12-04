from pydantic import BaseModel, EmailStr
from typing import Optional


class UserContactDataSync(BaseModel):
    """DTO for syncing contact data without requiring email_unal (it will be set from the path)"""
    personal_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    vehicle_plate: Optional[str] = None
