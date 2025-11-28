import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
import jwt
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

# Imports de la aplicación
from service.crud.auth_service import AuthService, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from domain.models.system_user import SystemUser
from domain.models.jwt_token import Token


# Configuración de passlib para las pruebas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestRegisterMethod:
    """Pruebas para el método AuthService.register()"""

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    def test_register_success_new_user(self, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Registro exitoso de un nuevo usuario
        Given: Email que no existe en la BD, contraseña válida y tipo de usuario
        When: Se llama a AuthService.register()
        Then: Se crea el usuario, se asocia al tipo y retorna el objeto SystemUser
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        mock_repo_instance.get_user_by_email.return_value = None  # Usuario no existe
        
        test_email = "newuser@example.com"
        test_password = "password123"
        test_type_user = "basic"

        # Act
        result = AuthService.register(test_email, test_password, test_type_user)

        # Assert
        assert result is not None
        assert isinstance(result, SystemUser)
        assert result.e_mail == test_email
        assert result.type_user == test_type_user
        assert result.state is True
        
        # Verificar que se llamó a get_user_by_email para verificar existencia
        mock_repo_instance.get_user_by_email.assert_called_once_with(test_email)
        
        # Verificar que se llamó a create_user con un SystemUser
        assert mock_repo_instance.create_user.called
        created_user_arg = mock_repo_instance.create_user.call_args[0][0]
        assert isinstance(created_user_arg, SystemUser)
        assert created_user_arg.e_mail == test_email
        
        # Verificar que se asoció el email al tipo de usuario
        mock_repo_instance.add_email_to_type_user.assert_called_once_with(test_type_user, test_email)

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    def test_register_user_already_exists(self, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Intento de registrar un usuario que ya existe
        Given: Email que ya existe en la BD
        When: Se llama a AuthService.register()
        Then: Retorna None sin crear el usuario
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        existing_user = SystemUser(
            e_mail="existing@example.com",
            hashed_password="hashed_pwd",
            salt="",
            type_user="basic",
            state=True
        )
        mock_repo_instance.get_user_by_email.return_value = existing_user
        
        test_email = "existing@example.com"
        test_password = "password123"

        # Act
        result = AuthService.register(test_email, test_password)

        # Assert
        assert result is None
        mock_repo_instance.get_user_by_email.assert_called_once_with(test_email)
        # No debe llamar a create_user ni add_email_to_type_user
        mock_repo_instance.create_user.assert_not_called()
        mock_repo_instance.add_email_to_type_user.assert_not_called()

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    def test_register_with_admin_type(self, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Registro de usuario con tipo 'admin'
        Given: Email nuevo y type_user='admin'
        When: Se llama a AuthService.register()
        Then: Usuario se registra correctamente como admin
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        mock_repo_instance.get_user_by_email.return_value = None
        
        test_email = "admin@example.com"
        test_password = "adminpass123"
        test_type_user = "admin"

        # Act
        result = AuthService.register(test_email, test_password, test_type_user)

        # Assert
        assert result is not None
        assert result.type_user == "admin"
        mock_repo_instance.add_email_to_type_user.assert_called_once_with("admin", test_email)

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_register_password_hashing(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Verificar que la contraseña se hashea correctamente
        Given: Una contraseña en texto plano
        When: Se llama a AuthService.register()
        Then: Se hashea la contraseña antes de guardar
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        mock_repo_instance.get_user_by_email.return_value = None
        
        mock_pwd_context.hash.return_value = "hashed_password_12345"
        
        test_email = "test@example.com"
        test_password = "plaintext_password"

        # Act
        result = AuthService.register(test_email, test_password)

        # Assert
        mock_pwd_context.hash.assert_called_once_with(test_password)
        assert result.hashed_password == "hashed_password_12345"

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    def test_register_default_type_user(self, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Registro sin especificar type_user (debe usar 'basic' por defecto)
        Given: Email y password sin type_user
        When: Se llama a AuthService.register()
        Then: Usuario se registra con type_user='basic'
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        mock_repo_instance.get_user_by_email.return_value = None
        
        test_email = "defaultuser@example.com"
        test_password = "password123"

        # Act
        result = AuthService.register(test_email, test_password)  # Sin type_user

        # Assert
        assert result.type_user == "basic"
        mock_repo_instance.add_email_to_type_user.assert_called_once_with("basic", test_email)

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    def test_register_user_state_is_true(self, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Usuario registrado tiene state=True por defecto
        Given: Datos de registro válidos
        When: Se llama a AuthService.register()
        Then: El usuario creado tiene state=True
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        mock_repo_instance.get_user_by_email.return_value = None

        # Act
        result = AuthService.register("user@example.com", "password123")

        # Assert
        assert result.state is True


class TestLoginMethod:
    """Pruebas para el método AuthService.login()"""

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_login_success_valid_credentials(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Login exitoso con credenciales válidas
        Given: Email y contraseña correctos de usuario activo
        When: Se llama a AuthService.login()
        Then: Retorna un token JWT válido
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        hashed_password = pwd_context.hash("correct_password")
        test_user = SystemUser(
            e_mail="user@example.com",
            hashed_password=hashed_password,
            salt="",
            type_user="basic",
            state=True
        )
        mock_repo_instance.get_user_by_email.return_value = test_user
        mock_pwd_context.verify.return_value = True

        # Act
        result = AuthService.login("user@example.com", "correct_password")

        # Assert
        assert result is not None
        assert isinstance(result, str)
        
        # Verificar que es un JWT válido
        decoded = jwt.decode(result, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "user@example.com"
        assert decoded["type_user"] == "basic"
        
        # Verificar que se guardó el token
        mock_repo_instance.create_token.assert_called_once()
        token_arg = mock_repo_instance.create_token.call_args[0][0]
        assert isinstance(token_arg, Token)
        assert token_arg.token == result
        assert token_arg.e_mail == "user@example.com"

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    def test_login_user_not_found(self, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Login con usuario que no existe
        Given: Email que no está registrado
        When: Se llama a AuthService.login()
        Then: Retorna None
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        mock_repo_instance.get_user_by_email.return_value = None

        # Act
        result = AuthService.login("nonexistent@example.com", "password123")

        # Assert
        assert result is None
        mock_repo_instance.create_token.assert_not_called()

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_login_user_inactive(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Login con usuario inactivo (state=False)
        Given: Usuario existe pero state=False
        When: Se llama a AuthService.login()
        Then: Retorna None
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        inactive_user = SystemUser(
            e_mail="inactive@example.com",
            hashed_password="hashed_pwd",
            salt="",
            type_user="basic",
            state=False  # Usuario inactivo
        )
        mock_repo_instance.get_user_by_email.return_value = inactive_user

        # Act
        result = AuthService.login("inactive@example.com", "password123")

        # Assert
        assert result is None
        mock_pwd_context.verify.assert_not_called()
        mock_repo_instance.create_token.assert_not_called()

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_login_wrong_password(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Login con contraseña incorrecta
        Given: Usuario existe y está activo pero contraseña es incorrecta
        When: Se llama a AuthService.login()
        Then: Retorna None
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        test_user = SystemUser(
            e_mail="user@example.com",
            hashed_password="hashed_correct_password",
            salt="",
            type_user="basic",
            state=True
        )
        mock_repo_instance.get_user_by_email.return_value = test_user
        mock_pwd_context.verify.return_value = False  # Contraseña incorrecta

        # Act
        result = AuthService.login("user@example.com", "wrong_password")

        # Assert
        assert result is None
        mock_pwd_context.verify.assert_called_once_with("wrong_password", "hashed_correct_password")
        mock_repo_instance.create_token.assert_not_called()

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_login_jwt_token_expiration(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Verificar que el token JWT tiene la expiración correcta
        Given: Credenciales válidas
        When: Se llama a AuthService.login()
        Then: Token tiene expiración de ACCESS_TOKEN_EXPIRE_MINUTES
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        test_user = SystemUser(
            e_mail="user@example.com",
            hashed_password="hashed_pwd",
            salt="",
            type_user="admin",
            state=True
        )
        mock_repo_instance.get_user_by_email.return_value = test_user
        mock_pwd_context.verify.return_value = True

        # Act
        result = AuthService.login("user@example.com", "password123")

        # Assert
        decoded = jwt.decode(result, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = decoded["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        
        # Verificar que la expiración está cerca de ACCESS_TOKEN_EXPIRE_MINUTES
        time_diff = (exp_datetime - now).total_seconds() / 60
        assert 29 <= time_diff <= 31  # Permitir 1 minuto de margen

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_login_jwt_contains_user_info(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Verificar que el JWT contiene la información del usuario
        Given: Credenciales válidas de usuario admin
        When: Se llama a AuthService.login()
        Then: Token contiene sub (email) y type_user
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        test_user = SystemUser(
            e_mail="admin@example.com",
            hashed_password="hashed_pwd",
            salt="",
            type_user="admin",
            state=True
        )
        mock_repo_instance.get_user_by_email.return_value = test_user
        mock_pwd_context.verify.return_value = True

        # Act
        result = AuthService.login("admin@example.com", "password123")

        # Assert
        decoded = jwt.decode(result, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "admin@example.com"
        assert decoded["type_user"] == "admin"
        assert "exp" in decoded

    @patch('service.crud.auth_service.get_dynamo_client')
    @patch('service.crud.auth_service.AuthRepository')
    @patch('service.crud.auth_service.pwd_context')
    def test_login_saves_token_to_database(self, mock_pwd_context, mock_auth_repo_class, mock_get_dynamo):
        """
        Test: Verificar que el token se guarda en la base de datos
        Given: Login exitoso
        When: Se genera el token JWT
        Then: Se llama a repo.create_token() con el token y email
        """
        # Arrange
        mock_repo_instance = MagicMock()
        mock_auth_repo_class.return_value = mock_repo_instance
        
        test_user = SystemUser(
            e_mail="user@example.com",
            hashed_password="hashed_pwd",
            salt="",
            type_user="basic",
            state=True
        )
        mock_repo_instance.get_user_by_email.return_value = test_user
        mock_pwd_context.verify.return_value = True

        # Act
        result = AuthService.login("user@example.com", "password123")

        # Assert
        mock_repo_instance.create_token.assert_called_once()
        token_arg = mock_repo_instance.create_token.call_args[0][0]
        assert isinstance(token_arg, Token)
        assert token_arg.token == result
        assert token_arg.e_mail == "user@example.com"
        assert isinstance(token_arg.created_at, datetime)


class TestVerifyTokenMethod:
    """Pruebas para el método AuthService.verify_token()"""

    def test_verify_token_valid(self):
        """
        Test: Verificación de token válido
        Given: Token JWT válido y no expirado
        When: Se llama a AuthService.verify_token()
        Then: Retorna True
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            "type_user": "basic"
        }
        valid_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Act
        result = AuthService.verify_token(valid_token)

        # Assert
        assert result is True

    def test_verify_token_expired(self):
        """
        Test: Verificación de token expirado
        Given: Token JWT con exp en el pasado
        When: Se llama a AuthService.verify_token()
        Then: Retorna False
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),  # Expirado hace 1 minuto
            "type_user": "basic"
        }
        expired_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Act
        result = AuthService.verify_token(expired_token)

        # Assert
        assert result is False

    def test_verify_token_invalid_signature(self):
        """
        Test: Verificación de token con firma inválida
        Given: Token JWT con SECRET_KEY incorrecta
        When: Se llama a AuthService.verify_token()
        Then: Retorna False
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            "type_user": "basic"
        }
        invalid_token = jwt.encode(payload, "WRONG_SECRET_KEY", algorithm=ALGORITHM)

        # Act
        result = AuthService.verify_token(invalid_token)

        # Assert
        assert result is False

    def test_verify_token_malformed(self):
        """
        Test: Verificación de token mal formado
        Given: String que no es un JWT válido
        When: Se llama a AuthService.verify_token()
        Then: Retorna False
        """
        # Arrange
        malformed_token = "this.is.not.a.valid.jwt.token"

        # Act
        result = AuthService.verify_token(malformed_token)

        # Assert
        assert result is False

    def test_verify_token_empty_string(self):
        """
        Test: Verificación de token vacío
        Given: String vacío como token
        When: Se llama a AuthService.verify_token()
        Then: Retorna False
        """
        # Arrange
        empty_token = ""

        # Act
        result = AuthService.verify_token(empty_token)

        # Assert
        assert result is False

    def test_verify_token_none(self):
        """
        Test: Verificación de token None
        Given: None como token
        When: Se llama a AuthService.verify_token()
        Then: Retorna False o lanza excepción manejada
        """
        # Arrange
        none_token = None

        # Act & Assert
        try:
            result = AuthService.verify_token(none_token)
            assert result is False
        except (AttributeError, TypeError):
            # Es aceptable que lance excepción con None
            pass

    def test_verify_token_with_different_algorithm(self):
        """
        Test: Verificación de token con algoritmo diferente
        Given: Token JWT creado con algoritmo HS512 en lugar de HS256
        When: Se llama a AuthService.verify_token()
        Then: Retorna False
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            "type_user": "basic"
        }
        wrong_algo_token = jwt.encode(payload, SECRET_KEY, algorithm="HS512")

        # Act
        result = AuthService.verify_token(wrong_algo_token)

        # Assert
        assert result is False

    def test_verify_token_missing_required_claims(self):
        """
        Test: Verificación de token sin claims requeridos (exp)
        Given: Token JWT sin campo 'exp'
        When: Se llama a AuthService.verify_token() con opciones por defecto
        Then: jwt.decode verifica exp automáticamente, si no hay exp pero tampoco se requiere, puede pasar
        Note: jwt.decode por defecto verifica 'exp' solo si existe, no lo requiere
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "type_user": "basic"
            # Falta 'exp' - pero jwt.decode no lo requiere obligatoriamente
        }
        token_without_exp = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Act
        result = AuthService.verify_token(token_without_exp)

        # Assert
        # jwt.decode acepta tokens sin exp si no se especifica verify_exp=True
        # Por lo tanto, el token es técnicamente válido
        assert result is True

    def test_verify_token_recently_expired(self):
        """
        Test: Verificación de token que acaba de expirar
        Given: Token JWT expirado hace 1 segundo
        When: Se llama a AuthService.verify_token()
        Then: Retorna False (no hay margen de gracia)
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
            "type_user": "basic"
        }
        recently_expired_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Act
        result = AuthService.verify_token(recently_expired_token)

        # Assert
        assert result is False

    def test_verify_token_about_to_expire(self):
        """
        Test: Verificación de token que está por expirar
        Given: Token JWT que expira en 1 segundo
        When: Se llama a AuthService.verify_token()
        Then: Retorna True (aún es válido)
        """
        # Arrange
        payload = {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(seconds=1),
            "type_user": "basic"
        }
        about_to_expire_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Act
        result = AuthService.verify_token(about_to_expire_token)

        # Assert
        assert result is True


# Configuración de pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
