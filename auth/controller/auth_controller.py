from fastapi import APIRouter, HTTPException
from domain.dtos.auth.register_input import RegisterInput
from domain.dtos.auth.login_input import LoginInput
from domain.dtos.auth.update_user_input import UpdateUserInput
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


@router.patch("/user/{e_mail}")
def update_user(e_mail: str, data: UpdateUserInput):
    """Actualiza contraseña y/o tipo de usuario"""
    result = AuthService.update_user(
        e_mail=e_mail,
        password=data.password,
        type_user=data.type_user
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    if result == "admin_exists":
        raise HTTPException(
            status_code=400, 
            detail="Admin user already exists. Only one admin is allowed."
        )
    
    return {
        "message": "User updated successfully",
        "e_mail": result.e_mail,
        "type_user": result.type_user
    }


@router.get("/user/{e_mail}/type")
def get_user_type(e_mail: str):
    """Obtiene el tipo/rol de un usuario"""
    type_user = AuthService.get_user_type(e_mail)
    
    if not type_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"e_mail": e_mail, "type_user": type_user}
