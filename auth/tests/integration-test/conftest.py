"""
Configuración de fixtures para pruebas de integración.
Estas pruebas usan recursos reales (DynamoDB, HTTP) sin mocks.
"""
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
import boto3
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Importar la aplicación FastAPI
from main import app


@pytest.fixture(scope="session")
def test_client():
    """
    Cliente HTTP real para probar los endpoints.
    Scope: session - se crea una vez por sesión de pruebas.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def dynamo_client():
    """
    Cliente real de DynamoDB para verificar datos en la base de datos.
    Scope: session - se reutiliza durante toda la sesión de pruebas.
    """
    session = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL")
    )
    yield session


@pytest.fixture(scope="session")
def dynamodb_tables(dynamo_client):
    """
    Referencias a las tablas reales de DynamoDB.
    Retorna un diccionario con las tres tablas.
    """
    tables = {
        "user_table": dynamo_client.Table("auth_ms_usuario"),
        "token_table": dynamo_client.Table("auth_ms_jwt"),
        "type_user_table": dynamo_client.Table("auth_ms_type_user")
    }
    yield tables


@pytest.fixture
def test_email():
    """
    Genera un email único para cada prueba usando UUID.
    Esto evita conflictos entre ejecuciones de pruebas.
    """
    return f"integration_test_{uuid.uuid4().hex[:8]}@test.com"


@pytest.fixture
def cleanup_test_user(dynamodb_tables, test_email):
    """
    Fixture de limpieza: elimina el usuario de prueba después de cada test.
    Se ejecuta después de que la prueba termine (yield).
    """
    yield  # La prueba se ejecuta aquí
    
    # Cleanup: eliminar usuario de prueba
    try:
        user_table = dynamodb_tables["user_table"]
        user_table.delete_item(Key={"e_mail": test_email})
        print(f"\n🧹 Cleanup: Usuario {test_email} eliminado de DynamoDB")
    except Exception as e:
        print(f"\n⚠️ Warning: No se pudo eliminar usuario {test_email}: {e}")


@pytest.fixture
def cleanup_test_tokens(dynamodb_tables):
    """
    Fixture de limpieza: elimina tokens de prueba después de cada test.
    Retorna una lista donde las pruebas pueden agregar tokens a limpiar.
    """
    tokens_to_clean = []
    
    yield tokens_to_clean  # La prueba agrega tokens aquí
    
    # Cleanup: eliminar tokens de prueba
    token_table = dynamodb_tables["token_table"]
    for token_value in tokens_to_clean:
        try:
            token_table.delete_item(Key={"token": token_value})
            print(f"\n🧹 Cleanup: Token eliminado de DynamoDB")
        except Exception as e:
            print(f"\n⚠️ Warning: No se pudo eliminar token: {e}")


@pytest.fixture
def sample_user_data():
    """
    Datos de ejemplo para registrar un usuario.
    Retorna un diccionario con los datos del usuario.
    """
    return {
        "e_mail": None,  # Se sobreescribe en cada prueba con test_email
        "password": "SecurePassword123!",
        "type_user": "basic"
    }
