from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import auth_controller



app = FastAPI(
    title="PROYECTO_TEAM_B - Authentication Microservice",
    description="Microservicio de autenticación con FastAPI y DynamoDB",
    version="1.0.0"
)

# === 🔐 Configuración CORS Global ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en dev)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite cualquier encabezado (Content-Type, Authorization, etc.)
)

app.include_router(auth_controller.router)

