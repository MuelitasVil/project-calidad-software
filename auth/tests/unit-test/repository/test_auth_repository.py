import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime

# Imports de la aplicación
from repository.auth_repository import AuthRepository
from domain.models.system_user import SystemUser
from domain.models.jwt_token import Token


class TestAuthRepositoryInit:
    """Pruebas para la inicialización de AuthRepository"""

    def test_init_creates_tables_references(self):
        """
        Test: Inicialización correcta del repositorio
        Given: Un cliente DynamoDB mockeado
        When: Se crea una instancia de AuthRepository
        Then: Se crean referencias a las 3 tablas
        """
        # Arrange
        mock_dynamo_client = MagicMock()
        mock_user_table = MagicMock()
        mock_token_table = MagicMock()
        mock_type_user_table = MagicMock()
        
        mock_dynamo_client.Table.side_effect = [
            mock_user_table,
            mock_token_table,
            mock_type_user_table
        ]

        # Act
        repo = AuthRepository(mock_dynamo_client)

        # Assert
        assert repo.dynamo == mock_dynamo_client
        assert repo.user_table == mock_user_table
        assert repo.token_table == mock_token_table
        assert repo.type_user_table == mock_type_user_table
        
        # Verificar que se llamó Table 3 veces con los nombres correctos
        assert mock_dynamo_client.Table.call_count == 3
        mock_dynamo_client.Table.assert_any_call("auth_ms_usuario")
        mock_dynamo_client.Table.assert_any_call("auth_ms_jwt")
        mock_dynamo_client.Table.assert_any_call("auth_ms_type_user")


class TestCreateUser:
    """Pruebas para el método create_user()"""

    def test_create_user_success(self):
        """
        Test: Crear usuario exitosamente
        Given: Un objeto SystemUser válido
        When: Se llama a create_user()
        Then: Se guarda en DynamoDB y retorna el usuario
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_user_table = MagicMock()
        mock_dynamo.Table.return_value = mock_user_table
        
        repo = AuthRepository(mock_dynamo)
        
        test_user = SystemUser(
            e_mail="test@example.com",
            hashed_password="hashed_pwd_123",
            salt="",
            type_user="basic",
            state=True
        )

        # Act
        result = repo.create_user(test_user)

        # Assert
        assert result == test_user
        mock_user_table.put_item.assert_called_once()
        
        # Verificar que se llamó con el diccionario correcto
        call_args = mock_user_table.put_item.call_args
        assert call_args[1]['Item']['e_mail'] == "test@example.com"
        assert call_args[1]['Item']['type_user'] == "basic"
        assert call_args[1]['Item']['state'] is True

    def test_create_user_with_admin_type(self):
        """
        Test: Crear usuario tipo admin
        Given: SystemUser con type_user='admin'
        When: Se llama a create_user()
        Then: Usuario admin se guarda correctamente
        """
        # Arrange
        mock_dynamo = MagicMock()
        repo = AuthRepository(mock_dynamo)
        
        admin_user = SystemUser(
            e_mail="admin@example.com",
            hashed_password="admin_pwd",
            salt="",
            type_user="admin",
            state=True
        )

        # Act
        result = repo.create_user(admin_user)

        # Assert
        assert result.type_user == "admin"
        assert result.e_mail == "admin@example.com"

    def test_create_user_with_inactive_state(self):
        """
        Test: Crear usuario inactivo
        Given: SystemUser con state=False
        When: Se llama a create_user()
        Then: Usuario inactivo se guarda correctamente
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_user_table = MagicMock()
        mock_dynamo.Table.return_value = mock_user_table
        
        repo = AuthRepository(mock_dynamo)
        
        inactive_user = SystemUser(
            e_mail="inactive@example.com",
            hashed_password="pwd",
            salt="",
            type_user="basic",
            state=False
        )

        # Act
        result = repo.create_user(inactive_user)

        # Assert
        assert result.state is False
        call_args = mock_user_table.put_item.call_args
        assert call_args[1]['Item']['state'] is False


class TestGetUserByEmail:
    """Pruebas para el método get_user_by_email()"""

    def test_get_user_by_email_found(self):
        """
        Test: Obtener usuario existente por email
        Given: Email de usuario que existe en DynamoDB
        When: Se llama a get_user_by_email()
        Then: Retorna el objeto SystemUser
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_user_table = MagicMock()
        mock_dynamo.Table.return_value = mock_user_table
        
        mock_user_table.get_item.return_value = {
            "Item": {
                "e_mail": "existing@example.com",
                "hashed_password": "hashed_pwd",
                "salt": "",
                "type_user": "basic",
                "state": True
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_user_by_email("existing@example.com")

        # Assert
        assert result is not None
        assert isinstance(result, SystemUser)
        assert result.e_mail == "existing@example.com"
        assert result.type_user == "basic"
        assert result.state is True
        
        mock_user_table.get_item.assert_called_once_with(
            Key={"e_mail": "existing@example.com"}
        )

    def test_get_user_by_email_not_found(self):
        """
        Test: Buscar usuario que no existe
        Given: Email que no está en DynamoDB
        When: Se llama a get_user_by_email()
        Then: Retorna None
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_user_table = MagicMock()
        mock_dynamo.Table.return_value = mock_user_table
        
        mock_user_table.get_item.return_value = {}  # Sin Item
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_user_by_email("nonexistent@example.com")

        # Assert
        assert result is None
        mock_user_table.get_item.assert_called_once_with(
            Key={"e_mail": "nonexistent@example.com"}
        )

    def test_get_user_by_email_inactive_user(self):
        """
        Test: Obtener usuario inactivo
        Given: Email de usuario con state=False
        When: Se llama a get_user_by_email()
        Then: Retorna el usuario con state=False
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_user_table = MagicMock()
        mock_dynamo.Table.return_value = mock_user_table
        
        mock_user_table.get_item.return_value = {
            "Item": {
                "e_mail": "inactive@example.com",
                "hashed_password": "pwd",
                "salt": "",
                "type_user": "basic",
                "state": False
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_user_by_email("inactive@example.com")

        # Assert
        assert result is not None
        assert result.state is False


class TestCreateToken:
    """Pruebas para el método create_token()"""

    def test_create_token_success(self):
        """
        Test: Crear token JWT exitosamente
        Given: Objeto Token válido
        When: Se llama a create_token()
        Then: Token se guarda en DynamoDB y se retorna
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_token_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), mock_token_table, MagicMock()]
        
        repo = AuthRepository(mock_dynamo)
        
        test_token = Token(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token",
            e_mail="user@example.com",
            created_at=datetime(2025, 11, 27, 10, 30, 0)
        )

        # Act
        result = repo.create_token(test_token)

        # Assert
        assert result == test_token
        mock_token_table.put_item.assert_called_once()
        
        call_args = mock_token_table.put_item.call_args
        assert call_args[1]['Item']['token'] == test_token.token
        assert call_args[1]['Item']['e_mail'] == "user@example.com"
        assert 'created_at' in call_args[1]['Item']

    def test_create_token_with_datetime_serialization(self):
        """
        Test: Verificar serialización de datetime a isoformat
        Given: Token con created_at como datetime
        When: Se llama a create_token()
        Then: created_at se convierte a isoformat antes de guardar
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_token_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), mock_token_table, MagicMock()]
        
        repo = AuthRepository(mock_dynamo)
        
        test_datetime = datetime(2025, 11, 27, 15, 45, 30)
        test_token = Token(
            token="test_token_123",
            e_mail="user@example.com",
            created_at=test_datetime
        )

        # Act
        repo.create_token(test_token)

        # Assert
        call_args = mock_token_table.put_item.call_args
        stored_datetime = call_args[1]['Item']['created_at']
        assert stored_datetime == test_datetime.isoformat()


class TestGetToken:
    """Pruebas para el método get_token()"""

    def test_get_token_found(self):
        """
        Test: Obtener token existente
        Given: Token que existe en DynamoDB
        When: Se llama a get_token()
        Then: Retorna el objeto Token
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_token_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), mock_token_table, MagicMock()]
        
        mock_token_table.get_item.return_value = {
            "Item": {
                "token": "test_token_value",
                "e_mail": "user@example.com",
                "created_at": "2025-11-27T10:30:00"
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_token("test_token_value")

        # Assert
        assert result is not None
        assert isinstance(result, Token)
        assert result.token == "test_token_value"
        assert result.e_mail == "user@example.com"
        
        mock_token_table.get_item.assert_called_once_with(
            Key={"token": "test_token_value"}
        )

    def test_get_token_not_found(self):
        """
        Test: Buscar token que no existe
        Given: Token que no está en DynamoDB
        When: Se llama a get_token()
        Then: Retorna None
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_token_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), mock_token_table, MagicMock()]
        
        mock_token_table.get_item.return_value = {}  # Sin Item
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_token("nonexistent_token")

        # Assert
        assert result is None
        mock_token_table.get_item.assert_called_once_with(
            Key={"token": "nonexistent_token"}
        )


class TestGetTypeUser:
    """Pruebas para el método get_type_user()"""

    def test_get_type_user_found(self):
        """
        Test: Obtener tipo de usuario existente
        Given: type_user que existe en DynamoDB
        When: Se llama a get_type_user()
        Then: Retorna el item con type_user y emails
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        mock_type_user_table.get_item.return_value = {
            "Item": {
                "type_user": "basic",
                "emails": ["user1@example.com", "user2@example.com"]
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_type_user("basic")

        # Assert
        assert result is not None
        assert result["type_user"] == "basic"
        assert len(result["emails"]) == 2
        assert "user1@example.com" in result["emails"]
        
        mock_type_user_table.get_item.assert_called_once_with(
            Key={"type_user": "basic"}
        )

    def test_get_type_user_not_found(self):
        """
        Test: Buscar tipo de usuario que no existe
        Given: type_user que no está en DynamoDB
        When: Se llama a get_type_user()
        Then: Retorna None
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        mock_type_user_table.get_item.return_value = {}  # Sin Item
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_type_user("nonexistent_type")

        # Assert
        assert result is None

    def test_get_type_user_admin(self):
        """
        Test: Obtener tipo de usuario admin
        Given: type_user='admin' que existe
        When: Se llama a get_type_user()
        Then: Retorna el tipo admin con sus emails
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        mock_type_user_table.get_item.return_value = {
            "Item": {
                "type_user": "admin",
                "emails": ["admin@example.com"]
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.get_type_user("admin")

        # Assert
        assert result["type_user"] == "admin"
        assert result["emails"] == ["admin@example.com"]


class TestCreateTypeUser:
    """Pruebas para el método create_type_user()"""

    def test_create_type_user_success(self):
        """
        Test: Crear nuevo tipo de usuario
        Given: type_user y email válidos
        When: Se llama a create_type_user()
        Then: Se crea el tipo con el primer email
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.create_type_user("premium", "premium@example.com")

        # Assert
        assert result is not None
        assert result["type_user"] == "premium"
        assert result["emails"] == ["premium@example.com"]
        
        mock_type_user_table.put_item.assert_called_once()
        call_args = mock_type_user_table.put_item.call_args
        assert call_args[1]['Item']['type_user'] == "premium"
        assert call_args[1]['Item']['emails'] == ["premium@example.com"]

    def test_create_type_user_basic(self):
        """
        Test: Crear tipo de usuario basic
        Given: type_user='basic' y un email
        When: Se llama a create_type_user()
        Then: Se crea el tipo basic correctamente
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.create_type_user("basic", "user@example.com")

        # Assert
        assert result["type_user"] == "basic"
        assert len(result["emails"]) == 1


class TestAddEmailToTypeUser:
    """Pruebas para el método add_email_to_type_user()"""

    def test_add_email_to_existing_type_user(self):
        """
        Test: Agregar email a tipo de usuario existente
        Given: type_user que existe y un nuevo email
        When: Se llama a add_email_to_type_user()
        Then: Email se agrega a la lista de emails
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        # Simular que el tipo ya existe con emails
        mock_type_user_table.get_item.return_value = {
            "Item": {
                "type_user": "basic",
                "emails": ["user1@example.com"]
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.add_email_to_type_user("basic", "user2@example.com")

        # Assert
        assert result is not None
        assert result["type_user"] == "basic"
        assert "user2@example.com" in result["emails"]
        assert len(result["emails"]) == 2
        
        # Verificar que se llamó update_item
        mock_type_user_table.update_item.assert_called_once()
        call_args = mock_type_user_table.update_item.call_args
        assert call_args[1]['Key']['type_user'] == "basic"
        assert "user2@example.com" in call_args[1]['ExpressionAttributeValues'][':emails']

    def test_add_email_to_type_user_when_type_not_exists(self):
        """
        Test: Agregar email cuando el tipo no existe
        Given: type_user que no existe en DynamoDB
        When: Se llama a add_email_to_type_user()
        Then: Se crea el tipo con ese email
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        # Simular que el tipo no existe
        mock_type_user_table.get_item.return_value = {}
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.add_email_to_type_user("new_type", "first@example.com")

        # Assert
        assert result is not None
        assert result["type_user"] == "new_type"
        assert result["emails"] == ["first@example.com"]
        
        # Verificar que se llamó put_item (crear), no update_item
        mock_type_user_table.put_item.assert_called_once()
        mock_type_user_table.update_item.assert_not_called()

    def test_add_duplicate_email_to_type_user(self):
        """
        Test: Intentar agregar email que ya existe
        Given: type_user con email que ya está en la lista
        When: Se llama a add_email_to_type_user() con el mismo email
        Then: No se duplica el email en la lista
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        existing_emails = ["user1@example.com", "user2@example.com"]
        mock_type_user_table.get_item.return_value = {
            "Item": {
                "type_user": "basic",
                "emails": existing_emails.copy()
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.add_email_to_type_user("basic", "user1@example.com")

        # Assert
        # No debe llamar a update_item porque el email ya existe
        mock_type_user_table.update_item.assert_not_called()
        assert result["emails"] == existing_emails

    def test_add_multiple_emails_sequentially(self):
        """
        Test: Agregar múltiples emails secuencialmente
        Given: type_user existente
        When: Se agregan varios emails uno por uno
        Then: Todos los emails se agregan correctamente
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        # Primera llamada: tipo existe con 1 email
        mock_type_user_table.get_item.side_effect = [
            {"Item": {"type_user": "basic", "emails": ["user1@example.com"]}},
            {"Item": {"type_user": "basic", "emails": ["user1@example.com", "user2@example.com"]}}
        ]
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result1 = repo.add_email_to_type_user("basic", "user2@example.com")
        result2 = repo.add_email_to_type_user("basic", "user3@example.com")

        # Assert
        assert mock_type_user_table.update_item.call_count == 2

    def test_add_email_to_admin_type(self):
        """
        Test: Agregar email a tipo admin
        Given: type_user='admin' existente
        When: Se agrega un nuevo admin
        Then: Email se agrega a la lista de admins
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        mock_type_user_table.get_item.return_value = {
            "Item": {
                "type_user": "admin",
                "emails": ["admin1@example.com"]
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.add_email_to_type_user("admin", "admin2@example.com")

        # Assert
        assert "admin2@example.com" in result["emails"]
        assert result["type_user"] == "admin"

    def test_add_email_with_empty_emails_list(self):
        """
        Test: Agregar email cuando la lista de emails está vacía
        Given: type_user con lista emails vacía
        When: Se agrega un email
        Then: Email se agrega correctamente
        """
        # Arrange
        mock_dynamo = MagicMock()
        mock_type_user_table = MagicMock()
        mock_dynamo.Table.side_effect = [MagicMock(), MagicMock(), mock_type_user_table]
        
        mock_type_user_table.get_item.return_value = {
            "Item": {
                "type_user": "basic",
                "emails": []
            }
        }
        
        repo = AuthRepository(mock_dynamo)

        # Act
        result = repo.add_email_to_type_user("basic", "first@example.com")

        # Assert
        assert "first@example.com" in result["emails"]
        assert len(result["emails"]) == 1


# Configuración de pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
