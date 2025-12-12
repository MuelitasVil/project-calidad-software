from pydantic import BaseModel, EmailStr, Field

class VerifyOtpInput(BaseModel):
    """DTO para verificar código OTP"""
    e_mail: EmailStr = Field(..., description="Email del usuario")
    otp_code: str = Field(..., min_length=6, max_length=6, description="Código OTP de 6 dígitos")
