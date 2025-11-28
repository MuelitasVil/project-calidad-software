#!/bin/bash
# Script de inicialización de tablas DynamoDB en LocalStack
# Este script se ejecuta automáticamente cuando LocalStack arranca

set -e

echo "🔧 Esperando a que LocalStack esté listo..."
# Esperar a que LocalStack esté disponible
until curl -s http://localhost:4566/_localstack/health | grep -q '"dynamodb": "available"'; do
  echo "⏳ Esperando LocalStack DynamoDB..."
  sleep 2
done

echo "✅ LocalStack está listo. Creando tablas DynamoDB..."

# Configuración de AWS CLI para LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# ============================================
# Tabla 1: auth_ms_usuario
# ============================================
echo "📝 Creando tabla: auth_ms_usuario (PK: e_mail)"
aws dynamodb create-table \
  --table-name auth_ms_usuario \
  --attribute-definitions \
    AttributeName=e_mail,AttributeType=S \
  --key-schema \
    AttributeName=e_mail,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 \
  || echo "⚠️  Tabla auth_ms_usuario ya existe o error al crear"

# ============================================
# Tabla 2: auth_ms_jwt
# ============================================
echo "📝 Creando tabla: auth_ms_jwt (PK: token)"
aws dynamodb create-table \
  --table-name auth_ms_jwt \
  --attribute-definitions \
    AttributeName=token,AttributeType=S \
  --key-schema \
    AttributeName=token,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 \
  || echo "⚠️  Tabla auth_ms_jwt ya existe o error al crear"

# ============================================
# Tabla 3: auth_ms_type_user
# ============================================
echo "📝 Creando tabla: auth_ms_type_user (PK: type_user)"
aws dynamodb create-table \
  --table-name auth_ms_type_user \
  --attribute-definitions \
    AttributeName=type_user,AttributeType=S \
  --key-schema \
    AttributeName=type_user,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 \
  || echo "⚠️  Tabla auth_ms_type_user ya existe o error al crear"

echo ""
echo "✅ Tablas DynamoDB creadas exitosamente!"
echo ""
echo "📋 Listando tablas:"
aws dynamodb list-tables \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 \
  --query 'TableNames' \
  --output table

echo ""
echo "🎉 Inicialización completada!"
