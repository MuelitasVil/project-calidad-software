from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.type_user import TypeUser
from app.domain.dtos.type_user.type_user_input import TypeUserInput
from app.service.crud.type_user_service import TypeUserService

router = APIRouter(prefix="/type_users", tags=["Type Users"])


@router.get("/", response_model=List[TypeUser])
def list_type_users(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return TypeUserService.get_all(session)


@router.get("/{type_user_id}", response_model=TypeUser)
def get_type_user(
    type_user_id: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    obj = TypeUserService.get_by_id(type_user_id, session)
    if not obj:
        raise HTTPException(status_code=404, detail="TypeUser not found")
    return obj


@router.post("/", response_model=TypeUser, status_code=status.HTTP_201_CREATED)
def create_type_user(
    data: TypeUserInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return TypeUserService.create(data, session)


@router.patch("/{type_user_id}", response_model=TypeUser)
def update_type_user(
    type_user_id: str,
    data: TypeUserInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    updated = TypeUserService.update(type_user_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="TypeUser not found")
    return updated


@router.delete("/{type_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_type_user(
    type_user_id: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = TypeUserService.delete(type_user_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="TypeUser not found")
