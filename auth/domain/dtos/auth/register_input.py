from pydantic import BaseModel, EmailStr, Field

class RegisterInput(BaseModel):
    e_mail: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="password")
    type_user: str = Field(..., example="admin")
