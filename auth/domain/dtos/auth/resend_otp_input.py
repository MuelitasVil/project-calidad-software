from pydantic import BaseModel, EmailStr, Field

class ResendOtpInput(BaseModel):
    """DTO para reenviar código OTP"""
    e_mail: EmailStr = Field(..., description="Email del usuario")
