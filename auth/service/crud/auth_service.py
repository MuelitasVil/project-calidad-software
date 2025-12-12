import uuid
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from domain.models.system_user import SystemUser
from domain.models.jwt_token import Token
from repository.auth_repository import AuthRepository
from configuration.database import get_dynamo_client

# Configuración del token
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def register(e_mail: str, password: str, type_user: str = "basic"):
        """Registra un nuevo usuario y lo asocia a su tipo en auth_ms_type_user"""
        repo = AuthRepository(get_dynamo_client())

        # Verificar si ya existe el usuario
        existing_user = repo.get_user_by_email(e_mail)
        if existing_user:
            print("⚠️ El usuario ya existe")
            return None

        # Verificar si se intenta crear un admin cuando ya existe uno
        if type_user.lower() == "admin":
            if repo.check_admin_exists():
                print("⚠️ Ya existe un usuario administrador registrado")
                return "admin_exists"

        # Crear el usuario en auth_ms_usuario
        hashed = pwd_context.hash(password)
        user = SystemUser(
            e_mail=e_mail,
            hashed_password=hashed,
            salt='',
            type_user=type_user,
            state=True
        )
        repo.create_user(user)

        # Asociar el correo al tipo de usuario en auth_ms_type_user
        repo.add_email_to_type_user(type_user, e_mail)

        return user

    @staticmethod
    def login(e_mail: str, password: str) -> dict | None:
        """Verifica credenciales y genera un token JWT"""
        repo = AuthRepository(get_dynamo_client())
        user = repo.get_user_by_email(e_mail)

        if not user or not user.state:
            return None

        if not pwd_context.verify(password, user.hashed_password):
            return None

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user.e_mail, "exp": expire, "type_user": user.type_user}

        # Crear JWT
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Guardar token en DynamoDB
        repo.create_token(
            Token(
                token=jwt_token,
                e_mail=user.e_mail,
                created_at=datetime.utcnow()
            )
        )
        
        # Retornar token y datos del usuario
        return {
            "token": jwt_token,
            "user": {
                "email": user.e_mail,
                "type_user": user.type_user
            }
        }

    @staticmethod
    def verify_token(token: str) -> bool | None:
        """Valida un token JWT y retorna el email del usuario si es válido"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except jwt.ExpiredSignatureError:
            print("⛔ Token expirado")
            return False
        except jwt.InvalidTokenError:
            print("❌ Token inválido")
            return False

    @staticmethod
    def update_user(e_mail: str, password: str = None, type_user: str = None):
        """Actualiza contraseña y/o tipo de usuario"""
        repo = AuthRepository(get_dynamo_client())
        
        # Verificar que el usuario existe
        user = repo.get_user_by_email(e_mail)
        if not user:
            return None

        # Obtener el tipo actual del usuario
        current_type = user.type_user

        # Validar restricción de admin único si se está cambiando a admin
        if type_user and type_user.lower() == "admin" and current_type.lower() != "admin":
            if repo.check_admin_exists():
                return "admin_exists"

        # Actualizar contraseña si se proporciona
        if password:
            hashed = pwd_context.hash(password)
            if not repo.update_user_password(e_mail, hashed):
                return None

        # Actualizar tipo de usuario si se proporciona
        if type_user and type_user != current_type:
            # Actualizar en tabla usuario
            if not repo.update_user_type(e_mail, type_user, current_type):
                return None
            
            # Actualizar en tabla type_user (remover del tipo anterior y agregar al nuevo)
            repo.remove_email_from_type_user(current_type, e_mail)
            repo.add_email_to_type_user(type_user, e_mail)

        # Obtener usuario actualizado
        return repo.get_user_by_email(e_mail)

    @staticmethod
    def get_user_type(e_mail: str) -> str | None:
        """Obtiene el tipo de usuario por su email"""
        repo = AuthRepository(get_dynamo_client())
        return repo.get_user_type_by_email(e_mail)
    
    @staticmethod
    def validate_credentials(e_mail: str, password: str) -> SystemUser | None:
        """
        Valida credenciales de usuario sin generar token
        
        Args:
            e_mail: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            SystemUser si las credenciales son válidas, None si no
        """
        repo = AuthRepository(get_dynamo_client())
        user = repo.get_user_by_email(e_mail)

        if not user or not user.state:
            return None

        if not pwd_context.verify(password, user.hashed_password):
            return None

        return user
    
    @staticmethod
    def generate_token_for_user(e_mail: str) -> dict | None:
        """
        Genera token JWT para un usuario (después de validar OTP)
        
        Args:
            e_mail: Email del usuario
            
        Returns:
            Dict con token y datos del usuario
        """
        repo = AuthRepository(get_dynamo_client())
        user = repo.get_user_by_email(e_mail)

        if not user or not user.state:
            return None

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user.e_mail, "exp": expire, "type_user": user.type_user}

        # Crear JWT
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Guardar token en DynamoDB
        repo.create_token(
            Token(
                token=jwt_token,
                e_mail=user.e_mail,
                created_at=datetime.utcnow()
            )
        )
        
        return {
            "token": jwt_token,
            "user": {
                "email": user.e_mail,
                "type_user": user.type_user
            }
        }
    
    @staticmethod
    def get_user_by_email(e_mail: str) -> SystemUser | None:
        """
        Obtiene un usuario por su email
        
        Args:
            e_mail: Email del usuario
            
        Returns:
            SystemUser si existe, None si no
        """
        repo = AuthRepository(get_dynamo_client())
        return repo.get_user_by_email(e_mail)
