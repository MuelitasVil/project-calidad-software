#!/usr/bin/env bash
set -euo pipefail

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Docker Compose Local Setup            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Construyendo imágenes...${NC}"
docker-compose build

echo -e "${YELLOW}🚀 Iniciando servicios...${NC}"
docker-compose up -d

# Esperar a que los servicios estén listos
echo -e "${YELLOW}⏳ Esperando que los servicios estén listos...${NC}"
sleep 10

# Verificar estado
echo -e "${YELLOW}📊 Estado de los contenedores:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}✅ ¡Configuración completada!${NC}"
echo ""
echo -e "${YELLOW}📝 URLs disponibles:${NC}"
echo -e "   ${GREEN}Auth Service:${NC}  http://localhost:8000/docs"
echo -e "   ${GREEN}Users Service:${NC} http://localhost:8001/docs"
echo -e "   ${GREEN}MySQL:${NC}          localhost:3306 (admin:teamb321**)"
echo -e "   ${GREEN}DynamoDB Local:${NC} http://localhost:8000"
echo ""
echo -e "${YELLOW}📋 Comandos útiles:${NC}"
echo -e "   ${GREEN}make logs${NC}        - Ver logs de todos los servicios"
echo -e "   ${GREEN}make logs-auth${NC}   - Ver logs del auth service"
echo -e "   ${GREEN}make logs-users${NC}  - Ver logs del users service"
echo -e "   ${GREEN}make down${NC}        - Detener los servicios"
echo -e "   ${GREEN}make clean${NC}       - Limpiar todo (contenedores + volúmenes)"
echo ""
