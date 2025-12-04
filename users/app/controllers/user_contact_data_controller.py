from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.domain.models.user_contact_data import UserContactData
from app.domain.dtos.user_contact_data.user_contact_data_input import UserContactDataInput
from app.domain.dtos.user_contact_data.user_contact_data_update import UserContactDataUpdate
from app.domain.dtos.user_contact_data.user_contact_data_sync import UserContactDataSync
from app.service.crud.user_contact_data_service import UserContactDataService

router = APIRouter(prefix="/contact_data", tags=["User Contact Data"])


@router.get("/", response_model=List[UserContactData])
def list_all_contacts(
    session: Session = Depends(get_session)
):
    """Listar todos los datos de contacto"""
    return UserContactDataService.get_all(session)


@router.get("/user/{email_unal}", response_model=List[UserContactData])
def list_user_contacts(
    email_unal: str,
    session: Session = Depends(get_session)
):
    """Listar todos los datos de contacto de un usuario específico"""
    return UserContactDataService.get_by_user_email(email_unal, session)


@router.get("/{contact_id}", response_model=UserContactData)
def get_contact(
    contact_id: int,
    session: Session = Depends(get_session)
):
    """Obtener un dato de contacto por ID"""
    contact = UserContactDataService.get_by_id(contact_id, session)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact data not found")
    return contact


@router.post("/", response_model=UserContactData, status_code=status.HTTP_201_CREATED)
def create_contact(
    data: UserContactDataInput,
    session: Session = Depends(get_session)
):
    """Crear un nuevo dato de contacto"""
    return UserContactDataService.create(data, session)


@router.post("/bulk", response_model=List[UserContactData], status_code=status.HTTP_201_CREATED)
def create_contacts_bulk(
    contacts: List[UserContactDataInput],
    session: Session = Depends(get_session)
):
    """Crear múltiples datos de contacto para un usuario"""
    return UserContactDataService.create_bulk(contacts, session)


@router.patch("/{contact_id}", response_model=UserContactData)
def update_contact(
    contact_id: int,
    data: UserContactDataUpdate,
    session: Session = Depends(get_session)
):
    """Actualizar un dato de contacto"""
    updated = UserContactDataService.update(contact_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact data not found")
    return updated


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    session: Session = Depends(get_session)
):
    """Eliminar un dato de contacto"""
    deleted = UserContactDataService.delete(contact_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact data not found")


@router.put("/user/{email_unal}/sync", response_model=List[UserContactData])
def sync_user_contacts(
    email_unal: str,
    contacts: List[UserContactDataSync],
    session: Session = Depends(get_session)
):
    """Sincronizar todos los contactos de un usuario (reemplaza existentes)"""
    return UserContactDataService.sync_user_contacts(email_unal, contacts, session)
