#!/bin/bash

# =========================================
# Validación de Setup Local
# =========================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}═════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Checklist de Validación - Setup Local  ${NC}"
echo -e "${YELLOW}═════════════════════════════════════════${NC}"
echo ""

PASS=0
FAIL=0

# Función para verificar
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅${NC} $1"
        ((PASS++))
    else
        echo -e "${RED}❌${NC} $1"
        ((FAIL++))
    fi
}

# 1. Verificar Docker
echo "📦 Verificando dependencias..."
command -v docker &> /dev/null
check "Docker instalado"

if command -v docker-compose &> /dev/null; then
    check "Docker Compose (legacy) instalado"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    check "Docker Compose plugin (docker compose) instalado"
else
    echo -e "${RED}❌ Docker Compose no encontrado${NC}"
    ((FAIL++))
fi

# 2. Verificar archivos
echo ""
echo "📁 Verificando archivos del proyecto..."
[ -f "docker-compose.yml" ]
check "docker-compose.yml existe"

[ -f ".env.local" ]
check ".env.local existe"

[ -f "Makefile" ]
check "Makefile existe"

[ -f "auth/Dockerfile" ]
check "auth/Dockerfile existe"

[ -f "users/Dockerfile" ]
check "users/Dockerfile existe"

[ -f "setup-local.sh" ]
check "setup-local.sh existe"

# 3. Verificar estructura de directorios
echo ""
echo "📂 Verificando estructura..."
[ -d "auth" ] && [ -f "auth/main.py" ]
check "Directorio auth con main.py"

[ -d "users" ] && [ -f "users/app/main.py" ]
check "Directorio users con app/main.py"

[ -d "users/db" ] && [ -f "users/db/create_tables.sql" ]
check "Scripts SQL de usuarios existen"

# 4. Verificar configuración
echo ""
echo "⚙️  Verificando configuración..."
grep -q "MYSQL_USER" .env.local
check "Variables MySQL en .env.local"

grep -q "AWS_REGION" .env.local
check "Variables AWS en .env.local"

# 5. Verificar contenido de Dockerfiles
echo ""
echo "🐳 Verificando Dockerfiles..."
grep -q "python:3.11" auth/Dockerfile
check "auth/Dockerfile usa Python 3.11"

grep -q "python:3.11" users/Dockerfile
check "users/Dockerfile usa Python 3.11"

# 6. Verificar Makefile
echo ""
echo "🔨 Verificando Makefile..."
grep -q "docker compose build\|docker-compose build" Makefile
check "Makefile tiene comando build"

grep -q "docker compose up\|docker-compose up" Makefile
check "Makefile tiene comando up"

grep -q "docker compose down\|docker-compose down" Makefile
check "Makefile tiene comando down"

# Resumen
echo ""
echo "═════════════════════════════════════════"
echo -e "Resultados: ${GREEN}✅ $PASS pasadas${NC} / ${RED}❌ $FAIL fallidas${NC}"
echo "═════════════════════════════════════════"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡Todos los checks pasaron!${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "  1. make build     # Construir imágenes"
    echo "  2. make up        # Iniciar servicios"
    echo "  3. make logs      # Ver logs en tiempo real"
    exit 0
else
    echo -e "${RED}⚠️  Algunos checks fallaron${NC}"
    echo "Por favor revisa los puntos fallidos"
    exit 1
fi

# 7. (Opcional) Verificar plugin de autenticación MySQL (si está en ejecución)
if docker ps --filter "name=mysql" --format '{{.Names}}' | grep -q mysql; then
    echo "\n🔍 Verificando plugin de autenticación del usuario admin..."
    OUT=$(docker exec mysql mysql -u root -proot123 -ss -e "SELECT plugin FROM mysql.user WHERE user='admin' AND host='%';" || true)
    if [ "${OUT}" = "mysql_native_password" ]; then
        echo -e "${GREEN}✅ admin usa mysql_native_password${NC}"
    else
        echo -e "${YELLOW}⚠️ admin no usa mysql_native_password (${OUT:-unknown}) - puedes aplicar 'make mysql-native-auth'${NC}"
    fi
fi
