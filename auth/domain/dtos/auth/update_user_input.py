from pydantic import BaseModel, EmailStr
from typing import Optional


class UpdateUserInput(BaseModel):
    password: Optional[str] = None
    type_user: Optional[str] = None
