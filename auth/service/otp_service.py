"""
Servicio de gestión de códigos OTP
"""
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict
from domain.models.otp import OTP
from repository.otp_repository import OtpRepository
from service.email_service import EmailService
from configuration.database import get_dynamo_client

class OtpService:
    """Servicio para generar, validar y gestionar códigos OTP"""
    
    OTP_LENGTH = 6  # Longitud del código OTP
    OTP_EXPIRY_MINUTES = 5  # Tiempo de expiración en minutos
    MAX_ATTEMPTS = 3  # Máximo de intentos fallidos permitidos
    
    @staticmethod
    def generate_otp_code() -> str:
        """
        Genera un código OTP aleatorio de 6 dígitos
        
        Returns:
            str: Código OTP de 6 dígitos
        """
        return ''.join(random.choices(string.digits, k=OtpService.OTP_LENGTH))
    
    @staticmethod
    def create_and_send_otp(email: str) -> Dict:
        """
        Crea un código OTP y lo envía por email
        
        Args:
            email: Email del usuario
            
        Returns:
            Dict con status y mensaje
        """
        try:
            repo = OtpRepository(get_dynamo_client())
            
            # Generar código OTP
            otp_code = OtpService.generate_otp_code()
            
            # Calcular tiempo de expiración
            now = datetime.utcnow()
            expires_at = now + timedelta(minutes=OtpService.OTP_EXPIRY_MINUTES)
            
            # Crear objeto OTP
            otp = OTP(
                e_mail=email,
                otp_code=otp_code,
                expires_at=expires_at.isoformat(),
                created_at=now.isoformat(),
                attempts=0
            )
            
            # Guardar en DynamoDB
            if not repo.create_otp(otp):
                return {
                    "success": False,
                    "message": "Error al guardar el código OTP"
                }
            
            # Enviar email
            if not EmailService.send_otp_email(email, otp_code, OtpService.OTP_EXPIRY_MINUTES):
                return {
                    "success": False,
                    "message": "Error al enviar el email con el código OTP"
                }
            
            print(f"✅ OTP generado y enviado para {email}: {otp_code}")
            
            return {
                "success": True,
                "message": f"Código OTP enviado a {email}",
                "expires_in_minutes": OtpService.OTP_EXPIRY_MINUTES
            }
            
        except Exception as e:
            print(f"❌ Error en create_and_send_otp: {e}")
            return {
                "success": False,
                "message": f"Error al generar OTP: {str(e)}"
            }
    
    @staticmethod
    def verify_otp(email: str, otp_code: str) -> Dict:
        """
        Verifica un código OTP
        
        Args:
            email: Email del usuario
            otp_code: Código OTP ingresado por el usuario
            
        Returns:
            Dict con resultado de la verificación
        """
        try:
            repo = OtpRepository(get_dynamo_client())
            
            # Obtener OTP almacenado
            stored_otp = repo.get_otp(email)
            
            if not stored_otp:
                return {
                    "success": False,
                    "error_code": "OTP_NOT_FOUND",
                    "message": "No se encontró un código OTP para este email. Solicita uno nuevo."
                }
            
            # Verificar si ha expirado
            if repo.is_otp_expired(stored_otp):
                repo.delete_otp(email)
                return {
                    "success": False,
                    "error_code": "OTP_EXPIRED",
                    "message": "El código OTP ha expirado. Solicita uno nuevo."
                }
            
            # Verificar número de intentos
            if stored_otp.attempts >= OtpService.MAX_ATTEMPTS:
                repo.delete_otp(email)
                return {
                    "success": False,
                    "error_code": "MAX_ATTEMPTS_EXCEEDED",
                    "message": "Has excedido el número máximo de intentos. Solicita un nuevo código."
                }
            
            # Verificar el código
            if stored_otp.otp_code != otp_code:
                # Incrementar intentos fallidos
                repo.increment_attempts(email)
                remaining_attempts = OtpService.MAX_ATTEMPTS - (stored_otp.attempts + 1)
                
                return {
                    "success": False,
                    "error_code": "INVALID_OTP",
                    "message": f"Código OTP incorrecto. Te quedan {remaining_attempts} intentos.",
                    "remaining_attempts": remaining_attempts
                }
            
            # ✅ Código correcto
            # Eliminar el OTP usado
            repo.delete_otp(email)
            
            print(f"✅ OTP verificado exitosamente para {email}")
            
            return {
                "success": True,
                "message": "Código OTP verificado correctamente"
            }
            
        except Exception as e:
            print(f"❌ Error en verify_otp: {e}")
            return {
                "success": False,
                "error_code": "VERIFICATION_ERROR",
                "message": f"Error al verificar el código: {str(e)}"
            }
    
    @staticmethod
    def resend_otp(email: str) -> Dict:
        """
        Reenvía un nuevo código OTP (invalida el anterior)
        
        Args:
            email: Email del usuario
            
        Returns:
            Dict con status y mensaje
        """
        try:
            repo = OtpRepository(get_dynamo_client())
            
            # Eliminar OTP anterior si existe
            repo.delete_otp(email)
            
            # Generar y enviar nuevo OTP
            otp_code = OtpService.generate_otp_code()
            
            now = datetime.utcnow()
            expires_at = now + timedelta(minutes=OtpService.OTP_EXPIRY_MINUTES)
            
            otp = OTP(
                e_mail=email,
                otp_code=otp_code,
                expires_at=expires_at.isoformat(),
                created_at=now.isoformat(),
                attempts=0
            )
            
            if not repo.create_otp(otp):
                return {
                    "success": False,
                    "message": "Error al guardar el nuevo código OTP"
                }
            
            # Enviar email de reenvío
            if not EmailService.send_otp_resend_notification(email, otp_code):
                return {
                    "success": False,
                    "message": "Error al enviar el email"
                }
            
            print(f"✅ Nuevo OTP reenviado para {email}: {otp_code}")
            
            return {
                "success": True,
                "message": f"Nuevo código OTP enviado a {email}",
                "expires_in_minutes": OtpService.OTP_EXPIRY_MINUTES
            }
            
        except Exception as e:
            print(f"❌ Error en resend_otp: {e}")
            return {
                "success": False,
                "message": f"Error al reenviar OTP: {str(e)}"
            }
    
    @staticmethod
    def get_otp_status(email: str) -> Dict:
        """
        Obtiene el estado actual del OTP para un email
        
        Args:
            email: Email del usuario
            
        Returns:
            Dict con información del OTP
        """
        try:
            repo = OtpRepository(get_dynamo_client())
            otp = repo.get_otp(email)
            
            if not otp:
                return {
                    "exists": False,
                    "message": "No hay código OTP activo"
                }
            
            is_expired = repo.is_otp_expired(otp)
            remaining_time = repo.get_remaining_time(otp)
            remaining_attempts = OtpService.MAX_ATTEMPTS - otp.attempts
            
            return {
                "exists": True,
                "is_expired": is_expired,
                "remaining_time_seconds": remaining_time,
                "remaining_attempts": remaining_attempts,
                "created_at": otp.created_at,
                "expires_at": otp.expires_at
            }
            
        except Exception as e:
            print(f"❌ Error en get_otp_status: {e}")
            return {
                "exists": False,
                "error": str(e)
            }
