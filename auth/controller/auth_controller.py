from fastapi import APIRouter, HTTPException
from domain.dtos.auth.register_input import RegisterInput
from domain.dtos.auth.login_input import LoginInput
from service.crud.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterInput):
    user = AuthService.register(data.e_mail, data.password, data.type_user)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    if user == "admin_exists":
        raise HTTPException(status_code=400, detail="Admin user already exists. Only one admin is allowed.")
    return {"message": "User registered", "e_mail": user.e_mail}


@router.post("/login")
def login(data: LoginInput):
    result = AuthService.login(data.e_mail, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "Access Granted": result["user"]["email"],
        "Access_token": result["token"],
        "token_type": "bearer",
        "type_user": result["user"]["type_user"]
    }
    

@router.get("/validate-token")
def validatetoken(data:str):
    return AuthService.verify_token(data)
