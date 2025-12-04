# Frontend Integration - Documentación

## 📋 Resumen de Cambios

Se ha integrado el frontend con los servicios backend locales usando Docker Compose. Los cambios principales incluyen:

1. **Servicio Web con Nginx** para servir el frontend
2. **Actualización de URLs** de AWS a servicios locales
3. **Configuración de CORS** (ya existente en ambos backends)

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Frontend      │
│   (Nginx)       │  Puerto 3000
│   localhost:3000│
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌─────────────┐  ┌─────────────┐
│ Auth Service│  │Users Service│
│   (FastAPI) │  │  (FastAPI)  │
│     :8000   │  │    :8001    │
└──────┬──────┘  └──────┬──────┘
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│  DynamoDB   │  │    MySQL    │
│ (LocalStack)│  │             │
│    :4566    │  │    :3306    │
└─────────────┘  └─────────────┘
```

## 🔧 Servicios Configurados

### Frontend Service
- **Puerto**: 3000
- **Tecnología**: Nginx (Alpine)
- **Ubicación**: `http://localhost:3000`
- **Archivos**: Servidos desde `/usr/share/nginx/html`

### Auth Service  
- **Puerto**: 8000
- **Endpoints**:
  - `POST /auth/register` - Registro de usuarios
  - `POST /auth/login` - Autenticación
  - `GET /auth/validate-token` - Validación de token

### Users Service
- **Puerto**: 8001
- **Endpoints** (períodos académicos):
  - `GET /periods/` - Listar todos los períodos
  - `GET /periods/{cod_period}` - Obtener un período
  - `POST /periods/` - Crear período
  - `PATCH /periods/{cod_period}` - Actualizar período
  - `DELETE /periods/{cod_period}` - Eliminar período

## 📝 Cambios Realizados

### 1. Docker Compose (`docker-compose.yml`)

Se agregó el servicio frontend:

```yaml
frontend:
  build:
    context: ./front
    dockerfile: Dockerfile
  container_name: frontend-service
  ports:
    - "3000:80"
  networks:
    - app-network
  restart: unless-stopped
```

### 2. Archivos Nuevos

- **`front/Dockerfile`**: Imagen Nginx para servir HTML estático
- **`front/nginx.conf`**: Configuración de Nginx
- **`front/FRONTEND_INTEGRATION.md`**: Este archivo

### 3. URLs Actualizadas en los Archivos HTML

#### login.html
- ❌ `https://cjx3hwfu56.execute-api.us-east-1.amazonaws.com/prod/team-b/auth/v1/auth/login`
- ✅ `http://localhost:8000/auth/login`
- ❌ `http://frontunal.s3.us-east-1.amazonaws.com/logo-o.png`
- ✅ `logo-o.png` (ruta relativa)

#### dashboard.html
- ❌ `https://cjx3hwfu56.execute-api.us-east-1.amazonaws.com/prod/team-b/users/v1/periods/`
- ✅ `http://localhost:8001/periods/`
- ❌ `http://frontunal.s3.us-east-1.amazonaws.com/logo-p.png`
- ✅ `logo-p.png` (ruta relativa)
- ❌ `http://frontunal.s3-website-us-east-1.amazonaws.com/compose-email.html`
- ✅ `compose-email.html` (ruta relativa)

#### compose-email.html
- ❌ `https://urvno9a286.execute-api.us-east-1.amazonaws.com/dev/email`
- ✅ ⚠️ **Funcionalidad deshabilitada** (servicio de email no implementado localmente)
- ❌ `http://frontunal.s3-website-us-east-1.amazonaws.com/dashboard.html`
- ✅ `dashboard.html` (ruta relativa)

## 🚀 Cómo Ejecutar

### 1. Iniciar todos los servicios

```bash
# Desde la raíz del proyecto
docker-compose up --build

# O en modo detached
docker-compose up -d --build
```

### 2. Verificar que los servicios están corriendo

```bash
# Ver servicios activos
docker-compose ps

# Deberías ver:
# - frontend-service (puerto 3000)
# - auth-service (puerto 8000)
# - users-service (puerto 8001)
# - localstack (puerto 4566)
# - mysql-local (puerto 3306)
```

### 3. Acceder al Frontend

Abre tu navegador en: **http://localhost:3000**

### 4. Probar el Flujo Completo

1. **Página de inicio**: `http://localhost:3000/index.html`
2. **Login**: `http://localhost:3000/login.html`
   - Usar credenciales registradas previamente
3. **Dashboard**: `http://localhost:3000/dashboard.html`
   - Ver períodos académicos
   - Crear/Editar/Eliminar períodos
4. **Compose Email**: `http://localhost:3000/compose-email.html`
   - ⚠️ Funcionalidad no disponible (servicio no implementado)

## ✅ Verificación de Endpoints

### Auth Service

```bash
# Healthcheck
curl http://localhost:8000/

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"e_mail":"test@example.com","password":"password123"}'

# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"e_mail":"newuser@example.com","password":"password123","type_user":"basic"}'
```

### Users Service

```bash
# Listar períodos (requiere token)
curl http://localhost:8001/periods/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Crear período
curl -X POST http://localhost:8001/periods/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "cod_period": "2025-1",
    "description": "Primer semestre 2025",
    "initial_date": "2025-01-15",
    "final_date": "2025-06-30"
  }'
```

## 🐛 Troubleshooting

### Error: "Failed to fetch" en el navegador

**Causa**: Los servicios backend no están corriendo o CORS está mal configurado.

**Solución**:
```bash
# Verificar que los servicios están activos
docker-compose ps

# Ver logs del servicio específico
docker-compose logs auth-service
docker-compose logs users-service
docker-compose logs frontend
```

### Error: "401 Unauthorized" en dashboard

**Causa**: Token JWT expirado o inválido.

**Solución**:
1. Hacer login nuevamente
2. Verificar que el token se guarda correctamente en localStorage
3. Revisar que el servicio auth esté validando tokens correctamente

### Error: Imágenes no se cargan

**Causa**: Los archivos de imagen no se copiaron correctamente al contenedor.

**Solución**:
```bash
# Reconstruir el contenedor frontend
docker-compose up --build frontend
```

### Error: CORS en el navegador

**Causa**: Los backends no aceptan requests del frontend.

**Verificación**:
```bash
# Verificar logs del backend
docker-compose logs auth-service | grep CORS
docker-compose logs users-service | grep CORS
```

**Solución**: Los backends ya tienen CORS configurado con `allow_origins=["*"]`

## 📊 Estado de Funcionalidades

| Funcionalidad | Estado | Notas |
|---------------|--------|-------|
| Login | ✅ Funcional | Conecta a `auth-service:8000` |
| Registro | ✅ Funcional | Disponible en auth-service |
| Listar Períodos | ✅ Funcional | Conecta a `users-service:8001` |
| Crear Período | ✅ Funcional | CRUD completo implementado |
| Editar Período | ✅ Funcional | PATCH endpoint disponible |
| Eliminar Período | ✅ Funcional | DELETE endpoint disponible |
| Enviar Email | ⚠️ No disponible | Servicio no implementado localmente |
| Logout | ✅ Funcional | Limpia localStorage |

## 🔐 Seguridad

### CORS Configurado
Ambos servicios backend tienen CORS habilitado:
- `allow_origins=["*"]` (⚠️ solo para desarrollo)
- `allow_credentials=True`
- `allow_methods=["*"]`
- `allow_headers=["*"]`

### JWT Authentication
- Los tokens se almacenan en `localStorage`
- Los endpoints protegidos requieren header `Authorization: Bearer <token>`
- ⚠️ En producción, considerar usar httpOnly cookies

## 📦 Estructura de Archivos

```
project-calidad-software/
├── docker-compose.yml          # ✅ Actualizado con servicio frontend
├── front/
│   ├── Dockerfile              # ✅ Nuevo
│   ├── nginx.conf              # ✅ Nuevo
│   ├── index.html              # ✅ Sin cambios (solo página de inicio)
│   ├── login.html              # ✅ Actualizado (URLs locales)
│   ├── dashboard.html          # ✅ Actualizado (URLs locales)
│   ├── compose-email.html      # ✅ Actualizado (funcionalidad deshabilitada)
│   ├── logo-o.png              # ✅ Recursos locales
│   ├── logo-p.png
│   ├── logo.png
│   └── logo.jpeg
├── auth/                       # Auth service (sin cambios)
└── users/                      # Users service (sin cambios)
```

## 🎯 Próximos Pasos

### Implementar Servicio de Email
Para habilitar la funcionalidad de compose-email:

1. Crear endpoint en users-service:
   ```python
   @router.post("/email")
   async def send_email(email_data: EmailInput):
       # Implementar envío de email
       pass
   ```

2. Descomentar código en `compose-email.html`:
   ```javascript
   const response = await fetch('http://localhost:8001/email', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(data)
   });
   ```

### Mejorar Seguridad en Producción
- Cambiar `allow_origins=["*"]` a dominios específicos
- Usar httpOnly cookies en lugar de localStorage
- Implementar refresh tokens
- Agregar rate limiting

### Testing
- Crear tests end-to-end con Selenium/Playwright
- Tests de integración frontend-backend
- Tests de CORS

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica que todos los servicios estén corriendo: `docker-compose ps`
3. Revisa la consola del navegador (F12)
4. Consulta este documento y el README principal

---

**Autor**: Sistema de pruebas de calidad de software
**Fecha**: Diciembre 2025
**Branch**: `feature/implementation_front_functional_test`
