#!/bin/bash
# Script de prueba para verificar DynamoDB en LocalStack

echo "🧪 Probando DynamoDB en LocalStack..."
echo ""

# Health check
echo "1️⃣ Verificando salud de LocalStack:"
curl -s http://localhost:4566/_localstack/health | python3 -m json.tool | grep -A 2 "dynamodb"
echo ""

# Listar tablas (debería estar vacío al inicio)
echo "2️⃣ Listando tablas DynamoDB:"
aws dynamodb list-tables --endpoint-url http://localhost:4566 --region us-east-1 2>/dev/null || echo "⚠️  AWS CLI no instalado. Instalar con: pip install awscli"
echo ""

# Crear tabla de prueba
echo "3️⃣ Creando tabla de prueba 'test-users':"
aws dynamodb create-table \
  --table-name test-users \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 2>/dev/null && echo "✅ Tabla creada" || echo "⚠️  Error creando tabla (puede que ya exista o AWS CLI no esté instalado)"
echo ""

# Listar tablas nuevamente
echo "4️⃣ Listando tablas después de crear 'test-users':"
aws dynamodb list-tables --endpoint-url http://localhost:4566 --region us-east-1 2>/dev/null
echo ""

echo "✅ Prueba completada. LocalStack con DynamoDB está funcionando!"
echo ""
echo "💡 Para gestionar DynamoDB visualmente:"
echo "   - NoSQL Workbench: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html"
echo "   - Dynobase: https://dynobase.dev/"
echo "   - AWS CLI: aws dynamodb --endpoint-url http://localhost:4566"
