import uuid
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.domain.models.system_user import SystemUser
from app.domain.models.jwt_token import Token
from app.repository.auth_repository import AuthRepository

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def register(email: str, password: str, session: Session) -> SystemUser:
        repo = AuthRepository(session)
        salt = uuid.uuid4().hex
        hashed = pwd_context.hash(password + salt)
        user = SystemUser(
            email=email,
            hashed_password=hashed,
            salt=salt
        )
        return repo.create_user(user)

    @staticmethod
    def login(email: str, password: str, session: Session) -> str:
        repo = AuthRepository(session)
        user = repo.get_user_by_email(email)
        if not user or not user.state:
            return None

        if not pwd_context.verify(password + user.salt, user.hashed_password):
            return None

        # Crear JWT
        expire = (
            datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        payload = {"sub": user.email, "exp": expire}
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Guardar token en DB
        repo.create_token(
            Token(
                jwt_token=jwt_token,
                email=user.email,
                created_at=datetime.utcnow()
            )
        )
        return jwt_token
