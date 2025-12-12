from fastapi import APIRouter, HTTPException
from domain.dtos.auth.register_input import RegisterInput
from domain.dtos.auth.login_input import LoginInput
from domain.dtos.auth.update_user_input import UpdateUserInput
from domain.dtos.auth.verify_otp_input import VerifyOtpInput
from domain.dtos.auth.resend_otp_input import ResendOtpInput
from service.crud.auth_service import AuthService
from service.otp_service import OtpService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterInput):
    user = AuthService.register(data.e_mail, data.password, data.type_user)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    if user == "admin_exists":
        raise HTTPException(status_code=400, detail="Admin user already exists. Only one admin is allowed.")
    return {"message": "User registered", "e_mail": user.e_mail}


@router.post("/login")
def login(data: LoginInput):
    """
    Inicio de sesión con generación de OTP
    
    El flujo es:
    1. Validar credenciales (email y contraseña)
    2. Generar código OTP de 6 dígitos
    3. Enviar código por email
    4. Retornar respuesta indicando que se requiere OTP
    
    El usuario debe luego llamar a /auth/verify-otp con el código recibido
    """
    # Validar credenciales
    user = AuthService.validate_credentials(data.e_mail, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generar y enviar OTP
    otp_result = OtpService.create_and_send_otp(data.e_mail)
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al enviar código OTP: {otp_result['message']}"
        )
    
    return {
        "requires_otp": True,
        "message": "Código OTP enviado a tu correo electrónico",
        "email": data.e_mail,
        "expires_in_minutes": otp_result["expires_in_minutes"]
    }


@router.post("/verify-otp")
def verify_otp(data: VerifyOtpInput):
    """
    Verifica el código OTP y genera el token JWT
    
    Args:
        data: Email y código OTP de 6 dígitos
        
    Returns:
        Token JWT si el código es válido
    """
    # Verificar código OTP
    verification_result = OtpService.verify_otp(data.e_mail, data.otp_code)
    
    if not verification_result["success"]:
        raise HTTPException(
            status_code=401,
            detail=verification_result["message"]
        )
    
    # Código OTP válido - generar token JWT
    result = AuthService.generate_token_for_user(data.e_mail)
    
    if not result:
        raise HTTPException(
            status_code=500,
            detail="Error al generar token de autenticación"
        )
    
    return {
        "Access Granted": result["user"]["email"],
        "Access_token": result["token"],
        "token_type": "bearer",
        "type_user": result["user"]["type_user"],
        "message": "Autenticación exitosa"
    }


@router.post("/resend-otp")
def resend_otp(data: ResendOtpInput):
    """
    Reenvía un nuevo código OTP
    
    Args:
        data: Email del usuario
        
    Returns:
        Confirmación de envío
    """
    # Verificar que el usuario existe
    user = AuthService.get_user_by_email(data.e_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Reenviar OTP
    otp_result = OtpService.resend_otp(data.e_mail)
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Error al reenviar código: {otp_result['message']}"
        )
    
    return {
        "message": "Nuevo código OTP enviado",
        "email": data.e_mail,
        "expires_in_minutes": otp_result["expires_in_minutes"]
    }


@router.get("/otp-status/{e_mail}")
def get_otp_status(e_mail: str):
    """
    Obtiene el estado del OTP para un email
    
    Útil para debugging y para mostrar tiempo restante en el frontend
    """
    status = OtpService.get_otp_status(e_mail)
    return status
    

@router.get("/validate-token")
def validatetoken(data:str):
    return AuthService.verify_token(data)


@router.patch("/user/{e_mail}")
def update_user(e_mail: str, data: UpdateUserInput):
    """Actualiza contraseña y/o tipo de usuario"""
    result = AuthService.update_user(
        e_mail=e_mail,
        password=data.password,
        type_user=data.type_user
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    if result == "admin_exists":
        raise HTTPException(
            status_code=400, 
            detail="Admin user already exists. Only one admin is allowed."
        )
    
    return {
        "message": "User updated successfully",
        "e_mail": result.e_mail,
        "type_user": result.type_user
    }


@router.get("/user/{e_mail}/type")
def get_user_type(e_mail: str):
    """Obtiene el tipo/rol de un usuario"""
    type_user = AuthService.get_user_type(e_mail)
    
    if not type_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"e_mail": e_mail, "type_user": type_user}
