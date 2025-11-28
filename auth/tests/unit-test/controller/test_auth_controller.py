import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Imports de la aplicación
from controller.auth_controller import router
from domain.models.system_user import SystemUser
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestRegisterEndpoint:
    """Pruebas para el endpoint POST /auth/register"""

    @patch('controller.auth_controller.AuthService.register')
    def test_register_success(self, mock_register):
        """
        Test: Registro exitoso de un nuevo usuario
        Given: Datos válidos de registro
        When: Se llama al endpoint /auth/register
        Then: Retorna mensaje de éxito y el email del usuario
        """
        # Arrange
        mock_user = SystemUser(
            e_mail="test@example.com",
            hashed_password="hashed_password",
            type_user="basic",
            state=True
        )
        mock_register.return_value = mock_user

        payload = {
            "e_mail": "test@example.com",
            "password": "password123",
            "type_user": "basic"
        }

        # Act
        response = client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "message": "User registered",
            "e_mail": "test@example.com"
        }
        mock_register.assert_called_once_with("test@example.com", "password123", "basic")

    @patch('controller.auth_controller.AuthService.register')
    def test_register_user_already_exists(self, mock_register):
        """
        Test: Intento de registrar un usuario que ya existe
        Given: Email de un usuario existente
        When: Se llama al endpoint /auth/register
        Then: Retorna error 400 con mensaje "User already exists"
        """
        # Arrange
        mock_register.return_value = None  # Simula que el usuario ya existe

        payload = {
            "e_mail": "existing@example.com",
            "password": "password123",
            "type_user": "basic"
        }

        # Act
        response = client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "User already exists"}
        mock_register.assert_called_once_with("existing@example.com", "password123", "basic")

    def test_register_invalid_email(self):
        """
        Test: Intento de registrar con email inválido
        Given: Email con formato inválido
        When: Se llama al endpoint /auth/register
        Then: Retorna error 422 de validación
        """
        # Arrange
        payload = {
            "e_mail": "invalid-email",
            "password": "password123",
            "type_user": "basic"
        }

        # Act
        response = client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_register_short_password(self):
        """
        Test: Intento de registrar con contraseña muy corta
        Given: Contraseña menor a 8 caracteres
        When: Se llama al endpoint /auth/register
        Then: Retorna error 422 de validación
        """
        # Arrange
        payload = {
            "e_mail": "test@example.com",
            "password": "123",
            "type_user": "basic"
        }

        # Act
        response = client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 422  # Validation error

    @patch('controller.auth_controller.AuthService.register')
    def test_register_with_admin_type(self, mock_register):
        """
        Test: Registro de usuario con tipo 'admin'
        Given: Datos de registro con type_user='admin'
        When: Se llama al endpoint /auth/register
        Then: Usuario se registra correctamente como admin
        """
        # Arrange
        mock_user = SystemUser(
            e_mail="admin@example.com",
            hashed_password="hashed_password",
            type_user="admin",
            state=True
        )
        mock_register.return_value = mock_user

        payload = {
            "e_mail": "admin@example.com",
            "password": "adminpass123",
            "type_user": "admin"
        }

        # Act
        response = client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["e_mail"] == "admin@example.com"
        mock_register.assert_called_once_with("admin@example.com", "adminpass123", "admin")


class TestLoginEndpoint:
    """Pruebas para el endpoint POST /auth/login"""

    @patch('controller.auth_controller.AuthService.login')
    def test_login_success(self, mock_login):
        """
        Test: Login exitoso con credenciales válidas
        Given: Email y contraseña correctos
        When: Se llama al endpoint /auth/login
        Then: Retorna token de acceso
        """
        # Arrange
        mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"
        mock_login.return_value = mock_token

        payload = {
            "e_mail": "test@example.com",
            "password": "password123"
        }

        # Act
        response = client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["Access Granted"] == "test@example.com"
        assert response_data["Access_token"] == mock_token
        assert response_data["token_type"] == "bearer"
        mock_login.assert_called_once_with("test@example.com", "password123")

    @patch('controller.auth_controller.AuthService.login')
    def test_login_invalid_credentials(self, mock_login):
        """
        Test: Login con credenciales inválidas
        Given: Email o contraseña incorrectos
        When: Se llama al endpoint /auth/login
        Then: Retorna error 401 "Invalid credentials"
        """
        # Arrange
        mock_login.return_value = None  # Simula credenciales inválidas

        payload = {
            "e_mail": "test@example.com",
            "password": "wrongpassword"
        }

        # Act
        response = client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid credentials"}
        mock_login.assert_called_once_with("test@example.com", "wrongpassword")

    @patch('controller.auth_controller.AuthService.login')
    def test_login_nonexistent_user(self, mock_login):
        """
        Test: Login con usuario que no existe
        Given: Email de usuario no registrado
        When: Se llama al endpoint /auth/login
        Then: Retorna error 401 "Invalid credentials"
        """
        # Arrange
        mock_login.return_value = None

        payload = {
            "e_mail": "nonexistent@example.com",
            "password": "password123"
        }

        # Act
        response = client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid credentials"}

    def test_login_invalid_email_format(self):
        """
        Test: Login con email de formato inválido
        Given: Email con formato incorrecto
        When: Se llama al endpoint /auth/login
        Then: Retorna error 422 de validación
        """
        # Arrange
        payload = {
            "e_mail": "not-an-email",
            "password": "password123"
        }

        # Act
        response = client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 422

    def test_login_missing_password(self):
        """
        Test: Login sin contraseña
        Given: Payload sin el campo password
        When: Se llama al endpoint /auth/login
        Then: Retorna error 422 de validación
        """
        # Arrange
        payload = {
            "e_mail": "test@example.com"
        }

        # Act
        response = client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 422


class TestValidateTokenEndpoint:
    """Pruebas para el endpoint GET /auth/validate-token"""

    @patch('controller.auth_controller.AuthService.verify_token')
    def test_validate_token_valid(self, mock_verify):
        """
        Test: Validación de token válido
        Given: Token JWT válido
        When: Se llama al endpoint /auth/validate-token
        Then: Retorna True
        """
        # Arrange
        mock_verify.return_value = True
        valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.valid.token"

        # Act
        response = client.get(f"/auth/validate-token?data={valid_token}")

        # Assert
        assert response.status_code == 200
        assert response.json() is True
        mock_verify.assert_called_once_with(valid_token)

    @patch('controller.auth_controller.AuthService.verify_token')
    def test_validate_token_expired(self, mock_verify):
        """
        Test: Validación de token expirado
        Given: Token JWT expirado
        When: Se llama al endpoint /auth/validate-token
        Then: Retorna False
        """
        # Arrange
        mock_verify.return_value = False
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.expired.token"

        # Act
        response = client.get(f"/auth/validate-token?data={expired_token}")

        # Assert
        assert response.status_code == 200
        assert response.json() is False
        mock_verify.assert_called_once_with(expired_token)

    @patch('controller.auth_controller.AuthService.verify_token')
    def test_validate_token_invalid(self, mock_verify):
        """
        Test: Validación de token inválido
        Given: Token JWT con formato o firma inválidos
        When: Se llama al endpoint /auth/validate-token
        Then: Retorna False
        """
        # Arrange
        mock_verify.return_value = False
        invalid_token = "invalid.token.string"

        # Act
        response = client.get(f"/auth/validate-token?data={invalid_token}")

        # Assert
        assert response.status_code == 200
        assert response.json() is False
        mock_verify.assert_called_once_with(invalid_token)

    def test_validate_token_missing_parameter(self):
        """
        Test: Validación sin proporcionar token
        Given: Request sin el parámetro 'data'
        When: Se llama al endpoint /auth/validate-token
        Then: Retorna error 422 de validación
        """
        # Act
        response = client.get("/auth/validate-token")

        # Assert
        assert response.status_code == 422

    @patch('controller.auth_controller.AuthService.verify_token')
    def test_validate_token_empty_string(self, mock_verify):
        """
        Test: Validación con token vacío
        Given: Token como string vacío
        When: Se llama al endpoint /auth/validate-token
        Then: Se llama a verify_token con string vacío
        """
        # Arrange
        mock_verify.return_value = False
        empty_token = ""

        # Act
        response = client.get(f"/auth/validate-token?data={empty_token}")

        # Assert
        assert response.status_code == 200
        assert response.json() is False
        mock_verify.assert_called_once_with(empty_token)


# Configuración de pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
