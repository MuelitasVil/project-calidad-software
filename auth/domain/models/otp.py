from pydantic import BaseModel
from datetime import datetime

class OTP(BaseModel):
    """Modelo para códigos OTP"""
    e_mail: str  # PK en DynamoDB
    otp_code: str  # Código de 6 dígitos
    expires_at: str  # Timestamp ISO de expiración
    created_at: str  # Timestamp ISO de creación
    attempts: int = 0  # Intentos de verificación
