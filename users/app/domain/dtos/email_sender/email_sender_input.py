from pydantic import BaseModel, EmailStr
from typing import Optional


class EmailSenderInput(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
