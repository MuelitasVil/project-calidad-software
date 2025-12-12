"""
Servicio de envío de emails usando SMTP de Gmail
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    """Servicio para enviar emails mediante SMTP"""
    
    # Configuración SMTP de Gmail
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "unal.team.b@gmail.com"
    SMTP_PASSWORD = "otmwkwlgwqxrkfif"  # Contraseña de aplicación de Gmail
    FROM_EMAIL = "unal.team.b@gmail.com"
    FROM_NAME = "ORGSECURE - Sistema de Autenticación"
    
    @staticmethod
    def send_otp_email(to_email: str, otp_code: str, expires_in_minutes: int = 5) -> bool:
        """
        Envía un código OTP al email del usuario
        
        Args:
            to_email: Email del destinatario
            otp_code: Código OTP de 6 dígitos
            expires_in_minutes: Tiempo de expiración en minutos
            
        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = "🔐 Código de Verificación OTP - ORGSECURE"
            message["From"] = f"{EmailService.FROM_NAME} <{EmailService.FROM_EMAIL}>"
            message["To"] = to_email
            
            # Contenido HTML del email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 40px auto;
                        background-color: #ffffff;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: 600;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .otp-box {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 10px;
                        padding: 30px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .otp-code {{
                        font-size: 48px;
                        font-weight: bold;
                        letter-spacing: 8px;
                        color: #ffffff;
                        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                    }}
                    .info-text {{
                        color: #555;
                        font-size: 16px;
                        line-height: 1.6;
                        margin: 20px 0;
                    }}
                    .warning {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 4px;
                    }}
                    .warning p {{
                        margin: 0;
                        color: #856404;
                        font-size: 14px;
                    }}
                    .footer {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        font-size: 12px;
                        color: #666;
                        border-top: 1px solid #e0e0e0;
                    }}
                    .security-icon {{
                        font-size: 48px;
                        margin-bottom: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="security-icon">🔐</div>
                        <h1>Verificación de Seguridad</h1>
                    </div>
                    
                    <div class="content">
                        <p class="info-text">
                            Hola,<br><br>
                            Hemos recibido una solicitud de inicio de sesión en tu cuenta de <strong>ORGSECURE</strong>.
                            Por motivos de seguridad, por favor verifica tu identidad utilizando el siguiente código:
                        </p>
                        
                        <div class="otp-box">
                            <p style="color: white; margin: 0 0 10px 0; font-size: 14px; font-weight: 500;">
                                TU CÓDIGO DE VERIFICACIÓN
                            </p>
                            <div class="otp-code">{otp_code}</div>
                            <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 13px;">
                                ⏱️ Este código expira en {expires_in_minutes} minutos
                            </p>
                        </div>
                        
                        <p class="info-text">
                            Ingresa este código en la página de inicio de sesión para continuar.
                        </p>
                        
                        <div class="warning">
                            <p>
                                <strong>⚠️ Importante:</strong> Si no solicitaste este código, 
                                ignora este mensaje y considera cambiar tu contraseña de inmediato.
                                Nunca compartas este código con nadie.
                            </p>
                        </div>
                        
                        <p class="info-text" style="margin-top: 30px;">
                            Saludos,<br>
                            <strong>Equipo de ORGSECURE</strong>
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p>Este es un mensaje automático, por favor no respondas a este correo.</p>
                        <p>© 2025 ORGSECURE - Sistema de Gestión Académica</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Adjuntar HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Conectar y enviar
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailService.SMTP_USER, EmailService.SMTP_PASSWORD)
                server.send_message(message)
            
            print(f"✅ Email OTP enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email OTP: {e}")
            return False
    
    @staticmethod
    def send_otp_resend_notification(to_email: str, otp_code: str) -> bool:
        """
        Envía notificación de reenvío de código OTP
        
        Args:
            to_email: Email del destinatario
            otp_code: Nuevo código OTP de 6 dígitos
            
        Returns:
            bool: True si se envió exitosamente
        """
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "🔄 Nuevo Código OTP - ORGSECURE"
            message["From"] = f"{EmailService.FROM_NAME} <{EmailService.FROM_EMAIL}>"
            message["To"] = to_email
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }}
                    .container {{ max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 40px 30px; text-align: center; }}
                    .otp-code {{ font-size: 48px; font-weight: bold; letter-spacing: 8px; color: #667eea; margin: 30px 0; }}
                    .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔄 Nuevo Código de Verificación</h1>
                    </div>
                    <div class="content">
                        <p>Has solicitado un nuevo código de verificación.</p>
                        <div class="otp-code">{otp_code}</div>
                        <p>⏱️ Este código expira en 5 minutos</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 ORGSECURE - Sistema de Gestión Académica</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailService.SMTP_USER, EmailService.SMTP_PASSWORD)
                server.send_message(message)
            
            print(f"✅ Email de reenvío OTP enviado a {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email de reenvío: {e}")
            return False
