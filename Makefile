# ===================================
# Docker Compose - Desarrollo Local
# ===================================

.PHONY: up down build restart logs clean help
.PHONY: recreate recreate-auth
.PHONY: mysql-native-auth
.PHONY: verify-dynamodb

# Detectar qué comando de docker compose está disponible:
# - `docker-compose` (legacy)
# - `docker compose` (plugin v2+)
DOCKER_COMPOSE := $(shell if command -v docker-compose >/dev/null 2>&1; then echo docker-compose; elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then echo "docker compose"; fi)

ifeq ($(DOCKER_COMPOSE),)
$(error "docker compose or docker-compose not found. Please install Docker Compose v2 or set an alias: alias docker-compose='docker compose'. See README.md for details.")
endif

## === Desarrollo Local con Docker Compose ===

help:
	@echo "📦 Comandos disponibles:"
	@echo ""
	@echo "  make up              - Iniciar todos los servicios"
	@echo "  make mysql-native-auth - Aplicar mysql_native_password para el usuario admin"
	@echo "  make verify-dynamodb - Verificar tablas DynamoDB en LocalStack"
	@echo "  make down            - Detener todos los servicios"
	@echo "  make build           - Construir las imágenes Docker"
	@echo "  make rebuild         - Reconstruir las imágenes (sin cache)"
	@echo "  make restart         - Reiniciar los servicios"
	@echo "  make logs            - Ver logs de todos los servicios"
	@echo "  make logs-auth       - Ver logs del servicio de auth"
	@echo "  make logs-users      - Ver logs del servicio de usuarios"
	@echo "  make clean           - Limpiar contenedores y volúmenes"
	@echo "  make ps              - Ver estado de los contenedores"
	@echo ""

		@echo "  make recreate        - Reconstruir y forzar recrear todos los servicios"
		@echo "  make recreate-auth   - Forzar reconstrucción del servicio auth"
build:
	@echo "🔨 Construyendo imágenes Docker..."
	$(DOCKER_COMPOSE) build

rebuild:
	@echo "🔨 Reconstruyendo imágenes Docker (sin cache)..."
	$(DOCKER_COMPOSE) build --no-cache

up:
	@echo "🚀 Iniciando servicios..."
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Servicios iniciados!"
	@echo ""
	@echo "📝 URLs disponibles:"
	@echo "   - Auth Service:  http://localhost:8000/docs"
	@echo "   - Users Service: http://localhost:8001/docs"
	@echo "   - MySQL:         localhost:3306"
	@echo "   - LocalStack (DynamoDB): http://localhost:4566/_localstack/health"
	@echo ""

down:
	@echo "🛑 Deteniendo servicios..."
	$(DOCKER_COMPOSE) down

restart:
	@echo "🔄 Reiniciando servicios..."
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f

logs-auth:
	$(DOCKER_COMPOSE) logs -f auth-service

logs-users:
	$(DOCKER_COMPOSE) logs -f users-service

ps:
	$(DOCKER_COMPOSE) ps

recreate:
	@echo "🔁 Reconstruyendo y forzando recreación de todos los servicios..."
	$(DOCKER_COMPOSE) up -d --force-recreate --build

recreate-auth:
	@echo "🔁 Forzando reconstrucción y recreación del servicio auth-service..."
	$(DOCKER_COMPOSE) up -d --force-recreate --build auth-service

mysql-native-auth:
	@echo "🔧 Aplicando mysql_native_password al usuario admin (entorno local)"
	@$(DOCKER_COMPOSE) exec -T mysql mysql -u root -proot123 -e "ALTER USER 'admin'@'%' IDENTIFIED WITH mysql_native_password BY 'teamb321**'; FLUSH PRIVILEGES;" || true

verify-dynamodb:
	@echo "🔍 Verificando tablas DynamoDB en LocalStack..."
	@./verify-dynamodb-tables.sh

.PHONY: dynamodb-ui-host
dynamodb-ui-host:
	@echo "🔎 Iniciando DynamoDB Admin UI en el host (usa --network host, Linux)"
	@docker run --rm --network host -e DYNAMO_ENDPOINT=http://localhost:8002 node:18-slim \
		sh -c "npm i -g dynamodb-admin@latest --no-progress && dynamodb-admin --host 0.0.0.0 --port 8003 --dynamo-endpoint http://localhost:8002"

clean:
	@echo "🧹 Limpiando..."
	$(DOCKER_COMPOSE) down -v
	@echo "✅ Limpieza completada!"

# ===================================
# AWS ECR (Producción)
# ===================================

REGION ?= us-east-1
ACCOUNT_ID ?= 123456789012
TAG ?= latest

.PHONY: build-users push-users build-auth push-auth prod-all

build-users-prod:
	 docker build -t users-service:$(TAG) ./users

push-users: build-users-prod
	 aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
	 docker tag users-service:$(TAG) $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/users-service:$(TAG)
	 docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/users-service:$(TAG)

build-auth-prod:
	 docker build -t auth-service:$(TAG) ./auth

push-auth: build-auth-prod
	 aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
	 docker tag auth-service:$(TAG) $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/auth-service:$(TAG)
	 docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/auth-service:$(TAG)

prod-all: push-users push-auth
