import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
import jwt

# Importar configuración de la aplicación
from service.crud.auth_service import SECRET_KEY, ALGORITHM


class TestRegisterIntegration:
    """
    Pruebas de integración para el endpoint POST /auth/register
    Valida el flujo completo: HTTP → Controller → Service → Repository → DynamoDB
    """

    def test_register_new_user_creates_record_in_database(
        self, 
        test_client, 
        dynamodb_tables, 
        test_email, 
        sample_user_data,
        cleanup_test_user
    ):
        """
        Test: Registrar un nuevo usuario guarda el registro en DynamoDB
        
        Given: Un email único y datos válidos de usuario
        When: Se hace POST /auth/register con los datos
        Then: 
            - El endpoint retorna status 200
            - El mensaje de respuesta confirma el registro
            - El usuario existe en la tabla auth_ms_usuario de DynamoDB
            - La contraseña está hasheada en la BD
            - El campo state está en True
            - El tipo de usuario se asocia correctamente
        """
        # Arrange: Preparar datos de prueba
        sample_user_data["e_mail"] = test_email
        user_table = dynamodb_tables["user_table"]
        type_user_table = dynamodb_tables["type_user_table"]
        
        print(f"\n🧪 Testing integration with email: {test_email}")

        # Act: Realizar request HTTP real al endpoint
        response = test_client.post(
            "/auth/register",
            json=sample_user_data
        )

        # Assert 1: Verificar respuesta HTTP
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()
        assert response_data["message"] == "User registered"
        assert response_data["e_mail"] == test_email

        # Assert 2: Verificar que el usuario existe en DynamoDB
        db_response = user_table.get_item(Key={"e_mail": test_email})
        assert "Item" in db_response, "Usuario no encontrado en DynamoDB"
        
        user_in_db = db_response["Item"]
        print(f"✅ Usuario encontrado en DynamoDB: {user_in_db}")

        # Assert 3: Verificar campos del usuario en la BD
        assert user_in_db["e_mail"] == test_email
        assert user_in_db["type_user"] == sample_user_data["type_user"]
        assert user_in_db["state"] is True, "El estado del usuario debe ser True"
        
        # Assert 4: Verificar que la contraseña está hasheada (no plain text)
        assert user_in_db["hashed_password"] != sample_user_data["password"], \
            "La contraseña NO debe estar en texto plano"
        assert user_in_db["hashed_password"].startswith("$2b$"), \
            "La contraseña debe estar hasheada con bcrypt"
        
        # Assert 5: Verificar que se puede verificar la contraseña
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_verified = pwd_context.verify(
            sample_user_data["password"], 
            user_in_db["hashed_password"]
        )
        assert password_verified, "La contraseña hasheada debe ser verificable"

        # Assert 6: Verificar que el tipo de usuario se creó/actualizó en auth_ms_type_user
        type_response = type_user_table.get_item(
            Key={"type_user": sample_user_data["type_user"]}
        )
        assert "Item" in type_response, "Tipo de usuario no encontrado en DynamoDB"
        
        type_user_in_db = type_response["Item"]
        assert test_email in type_user_in_db["emails"], \
            f"El email {test_email} debe estar en la lista de emails del tipo {sample_user_data['type_user']}"
        
        print(f"✅ Tipo de usuario verificado: {type_user_in_db}")


    def test_register_duplicate_user_returns_error(
        self, 
        test_client, 
        dynamodb_tables, 
        test_email, 
        sample_user_data,
        cleanup_test_user
    ):
        """
        Test: Intentar registrar un usuario duplicado retorna error
        
        Given: Un usuario ya registrado en DynamoDB
        When: Se intenta registrar el mismo email nuevamente
        Then: 
            - El endpoint retorna status 400
            - El mensaje de error indica que el usuario ya existe
            - No se crea un segundo registro en la BD
        """
        # Arrange: Registrar el usuario por primera vez
        sample_user_data["e_mail"] = test_email
        user_table = dynamodb_tables["user_table"]
        
        print(f"\n🧪 Testing duplicate user with email: {test_email}")
        
        # Primer registro (exitoso)
        first_response = test_client.post(
            "/auth/register",
            json=sample_user_data
        )
        assert first_response.status_code == 200

        # Act: Intentar registrar el mismo usuario nuevamente
        second_response = test_client.post(
            "/auth/register",
            json=sample_user_data
        )

        # Assert 1: Verificar que retorna error 400
        assert second_response.status_code == 400
        error_data = second_response.json()
        assert "already exists" in error_data["detail"].lower()

        # Assert 2: Verificar que solo hay un registro en DynamoDB
        db_response = user_table.get_item(Key={"e_mail": test_email})
        assert "Item" in db_response, "El usuario debe seguir existiendo en DynamoDB"
        
        print(f"✅ Usuario duplicado rechazado correctamente")


    def test_register_with_admin_type_creates_admin_user(
        self, 
        test_client, 
        dynamodb_tables, 
        test_email,
        cleanup_test_user
    ):
        """
        Test: Registrar un usuario tipo 'admin' lo guarda correctamente
        
        Given: Datos de usuario con type_user='admin'
        When: Se hace POST /auth/register
        Then: 
            - El usuario se crea con type_user='admin' en DynamoDB
            - El email se asocia al tipo 'admin' en auth_ms_type_user
        """
        # Arrange
        admin_data = {
            "e_mail": test_email,
            "password": "AdminPassword123!",
            "type_user": "admin"
        }
        user_table = dynamodb_tables["user_table"]
        type_user_table = dynamodb_tables["type_user_table"]
        
        print(f"\n🧪 Testing admin user registration with email: {test_email}")

        # Act: Registrar usuario admin
        response = test_client.post(
            "/auth/register",
            json=admin_data
        )

        # Assert 1: Verificar respuesta HTTP exitosa
        assert response.status_code == 200

        # Assert 2: Verificar usuario en DynamoDB tiene type_user='admin'
        db_response = user_table.get_item(Key={"e_mail": test_email})
        assert "Item" in db_response
        user_in_db = db_response["Item"]
        assert user_in_db["type_user"] == "admin"

        # Assert 3: Verificar que el email está en la lista de admins
        type_response = type_user_table.get_item(Key={"type_user": "admin"})
        assert "Item" in type_response
        type_user_in_db = type_response["Item"]
        assert test_email in type_user_in_db["emails"]
        
        print(f"✅ Usuario admin creado y verificado correctamente")


    def test_register_invalid_email_returns_validation_error(
        self, 
        test_client,
        sample_user_data
    ):
        """
        Test: Registrar con email inválido retorna error de validación
        
        Given: Un email con formato inválido
        When: Se hace POST /auth/register
        Then: El endpoint retorna status 422 (Validation Error)
        """
        # Arrange: Email inválido
        invalid_data = sample_user_data.copy()
        invalid_data["e_mail"] = "not-an-email"
        
        print(f"\n🧪 Testing invalid email format: {invalid_data['e_mail']}")

        # Act: Intentar registrar con email inválido
        response = test_client.post(
            "/auth/register",
            json=invalid_data
        )

        # Assert: Verificar error de validación
        assert response.status_code == 422, \
            f"Expected 422 for invalid email, got {response.status_code}"
        
        print(f"✅ Validación de email funcionó correctamente")


    def test_register_and_verify_password_hashing(
        self, 
        test_client, 
        dynamodb_tables, 
        test_email, 
        sample_user_data,
        cleanup_test_user
    ):
        """
        Test: La contraseña se hashea correctamente con bcrypt
        
        Given: Una contraseña en texto plano
        When: Se registra el usuario
        Then: 
            - La contraseña en DynamoDB está hasheada
            - Se puede verificar con el hash
            - No se puede recuperar la contraseña original
        """
        # Arrange
        sample_user_data["e_mail"] = test_email
        original_password = sample_user_data["password"]
        user_table = dynamodb_tables["user_table"]
        
        print(f"\n🧪 Testing password hashing for: {test_email}")

        # Act: Registrar usuario
        response = test_client.post(
            "/auth/register",
            json=sample_user_data
        )
        assert response.status_code == 200

        # Assert 1: Obtener contraseña hasheada de DynamoDB
        db_response = user_table.get_item(Key={"e_mail": test_email})
        hashed_password = db_response["Item"]["hashed_password"]

        # Assert 2: Verificar formato bcrypt
        assert hashed_password.startswith("$2b$"), "Debe usar bcrypt"
        assert len(hashed_password) == 60, "Hash bcrypt debe tener 60 caracteres"

        # Assert 3: Verificar que no es la contraseña original
        assert hashed_password != original_password

        # Assert 4: Verificar que el hash es válido
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        assert pwd_context.verify(original_password, hashed_password)

        # Assert 5: Verificar que una contraseña incorrecta falla
        assert not pwd_context.verify("wrong_password", hashed_password)
        
        print(f"✅ Password hashing verificado correctamente")


class TestRegisterIntegrationEdgeCases:
    """
    Casos límite y escenarios complejos de integración
    """

    def test_register_multiple_users_same_type(
        self, 
        test_client, 
        dynamodb_tables
    ):
        """
        Test: Registrar múltiples usuarios del mismo tipo actualiza la lista de emails
        
        Given: Varios usuarios con el mismo type_user
        When: Se registran todos
        Then: Todos los emails están en la lista de ese tipo en auth_ms_type_user
        """
        # Arrange
        import uuid
        type_user_table = dynamodb_tables["type_user_table"]
        user_table = dynamodb_tables["user_table"]
        
        test_type = f"test_type_{uuid.uuid4().hex[:8]}"
        emails = [
            f"user1_{uuid.uuid4().hex[:8]}@test.com",
            f"user2_{uuid.uuid4().hex[:8]}@test.com",
            f"user3_{uuid.uuid4().hex[:8]}@test.com"
        ]
        
        print(f"\n🧪 Testing multiple users with type: {test_type}")

        # Act: Registrar 3 usuarios del mismo tipo
        for email in emails:
            response = test_client.post(
                "/auth/register",
                json={
                    "e_mail": email,
                    "password": "TestPassword123!",
                    "type_user": test_type
                }
            )
            assert response.status_code == 200

        # Assert: Verificar que todos los emails están en el tipo
        type_response = type_user_table.get_item(Key={"type_user": test_type})
        assert "Item" in type_response
        
        emails_in_type = type_response["Item"]["emails"]
        for email in emails:
            assert email in emails_in_type, \
                f"Email {email} debe estar en la lista del tipo {test_type}"
        
        print(f"✅ {len(emails)} usuarios registrados en el mismo tipo")

        # Cleanup: Eliminar usuarios de prueba
        for email in emails:
            try:
                user_table.delete_item(Key={"e_mail": email})
            except:
                pass


    def test_register_empty_password_returns_validation_error(
        self, 
        test_client, 
        test_email
    ):
        """
        Test: Registrar con contraseña vacía retorna error de validación
        
        Given: Datos de usuario con password vacío
        When: Se hace POST /auth/register
        Then: El endpoint retorna error de validación
        """
        # Arrange
        invalid_data = {
            "e_mail": test_email,
            "password": "",
            "type_user": "basic"
        }
        
        print(f"\n🧪 Testing empty password for: {test_email}")

        # Act
        response = test_client.post(
            "/auth/register",
            json=invalid_data
        )

        # Assert: Debe retornar error (422 o 400)
        assert response.status_code in [422, 400], \
            f"Expected validation error, got {response.status_code}"
        
        print(f"✅ Empty password rejected correctly")
