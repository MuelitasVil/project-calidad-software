"""
Repositorio para gestionar códigos OTP en DynamoDB
"""
from datetime import datetime, timedelta
from typing import Optional
import boto3
from domain.models.otp import OTP

class OtpRepository:
    """Repositorio para operaciones CRUD de códigos OTP"""
    
    def __init__(self, dynamodb_client):
        self.dynamodb = dynamodb_client
        self.table_name = "auth_ms_otp"
        self.table = self.dynamodb.Table(self.table_name)
    
    def create_otp(self, otp: OTP) -> bool:
        """
        Crea o actualiza un código OTP para un email
        
        Args:
            otp: Objeto OTP con los datos del código
            
        Returns:
            bool: True si se creó exitosamente
        """
        try:
            self.table.put_item(
                Item={
                    "e_mail": otp.e_mail,
                    "otp_code": otp.otp_code,
                    "expires_at": otp.expires_at,
                    "created_at": otp.created_at,
                    "attempts": otp.attempts
                }
            )
            print(f"✅ OTP creado para {otp.e_mail}")
            return True
        except Exception as e:
            print(f"❌ Error creando OTP: {e}")
            return False
    
    def get_otp(self, email: str) -> Optional[OTP]:
        """
        Obtiene el código OTP de un email
        
        Args:
            email: Email del usuario
            
        Returns:
            OTP si existe, None si no
        """
        try:
            response = self.table.get_item(Key={"e_mail": email})
            
            if "Item" in response:
                item = response["Item"]
                return OTP(
                    e_mail=item["e_mail"],
                    otp_code=item["otp_code"],
                    expires_at=item["expires_at"],
                    created_at=item["created_at"],
                    attempts=item.get("attempts", 0)
                )
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo OTP: {e}")
            return None
    
    def delete_otp(self, email: str) -> bool:
        """
        Elimina un código OTP
        
        Args:
            email: Email del usuario
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            self.table.delete_item(Key={"e_mail": email})
            print(f"✅ OTP eliminado para {email}")
            return True
        except Exception as e:
            print(f"❌ Error eliminando OTP: {e}")
            return False
    
    def increment_attempts(self, email: str) -> bool:
        """
        Incrementa el contador de intentos fallidos
        
        Args:
            email: Email del usuario
            
        Returns:
            bool: True si se incrementó exitosamente
        """
        try:
            self.table.update_item(
                Key={"e_mail": email},
                UpdateExpression="SET attempts = if_not_exists(attempts, :start) + :inc",
                ExpressionAttributeValues={
                    ":inc": 1,
                    ":start": 0
                }
            )
            print(f"✅ Intentos incrementados para {email}")
            return True
        except Exception as e:
            print(f"❌ Error incrementando intentos: {e}")
            return False
    
    def is_otp_expired(self, otp: OTP) -> bool:
        """
        Verifica si un código OTP ha expirado
        
        Args:
            otp: Objeto OTP a verificar
            
        Returns:
            bool: True si está expirado, False si aún es válido
        """
        try:
            expires_at = datetime.fromisoformat(otp.expires_at)
            now = datetime.utcnow()
            is_expired = now > expires_at
            
            if is_expired:
                print(f"⏰ OTP expirado para {otp.e_mail}")
            
            return is_expired
            
        except Exception as e:
            print(f"❌ Error verificando expiración: {e}")
            return True  # Por seguridad, considerar expirado si hay error
    
    def get_remaining_time(self, otp: OTP) -> int:
        """
        Calcula el tiempo restante en segundos antes de que expire el OTP
        
        Args:
            otp: Objeto OTP
            
        Returns:
            int: Segundos restantes (0 si ya expiró)
        """
        try:
            expires_at = datetime.fromisoformat(otp.expires_at)
            now = datetime.utcnow()
            remaining = (expires_at - now).total_seconds()
            return max(0, int(remaining))
        except Exception as e:
            print(f"❌ Error calculando tiempo restante: {e}")
            return 0
