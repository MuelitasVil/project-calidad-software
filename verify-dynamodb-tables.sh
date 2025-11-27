#!/bin/bash
# Script para verificar las tablas DynamoDB en LocalStack
# Ejecutar después de: make up

echo "🔍 Verificando tablas DynamoDB en LocalStack..."
echo ""

# Verificar conectividad
if ! curl -s http://localhost:4566/_localstack/health > /dev/null 2>&1; then
    echo "❌ Error: LocalStack no está corriendo en http://localhost:4566"
    echo "   Ejecuta: make up"
    exit 1
fi

echo "✅ LocalStack está corriendo"
echo ""

# Listar tablas
echo "📋 Tablas DynamoDB disponibles:"
docker exec localstack awslocal dynamodb list-tables --query 'TableNames' --output table

echo ""
echo "📊 Detalles de las tablas:"
echo ""

# auth_ms_usuario
echo "1️⃣  auth_ms_usuario (Usuarios del sistema)"
docker exec localstack awslocal dynamodb describe-table \
  --table-name auth_ms_usuario \
  --query 'Table.[TableName,TableStatus,ItemCount,KeySchema[0]]' \
  --output json | python3 -m json.tool
echo ""

# auth_ms_jwt
echo "2️⃣  auth_ms_jwt (Tokens JWT)"
docker exec localstack awslocal dynamodb describe-table \
  --table-name auth_ms_jwt \
  --query 'Table.[TableName,TableStatus,ItemCount,KeySchema[0]]' \
  --output json | python3 -m json.tool
echo ""

# auth_ms_type_user
echo "3️⃣  auth_ms_type_user (Tipos de usuario)"
docker exec localstack awslocal dynamodb describe-table \
  --table-name auth_ms_type_user \
  --query 'Table.[TableName,TableStatus,ItemCount,KeySchema[0]]' \
  --output json | python3 -m json.tool
echo ""

echo "✅ Verificación completada!"
echo ""
echo "💡 Para insertar datos de prueba:"
echo "   docker exec localstack awslocal dynamodb put-item --table-name auth_ms_usuario --item '{\"e_mail\":{\"S\":\"test@example.com\"},\"hashed_password\":{\"S\":\"hashed123\"},\"type_user\":{\"S\":\"basic\"},\"state\":{\"BOOL\":true}}'"
echo ""
echo "💡 Para consultar datos:"
echo "   docker exec localstack awslocal dynamodb scan --table-name auth_ms_usuario"
