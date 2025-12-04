from pydantic import BaseModel, EmailStr, Field

class LoginInput(BaseModel):
    e_mail: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="password")