from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.email_sender_unit import EmailSenderUnit
from app.domain.dtos.email_sender_unit.email_sender_unit_input import (
    EmailSenderUnitInput,
)
from app.service.crud.email_sender_unit_service import EmailSenderUnitService

router = APIRouter(prefix="/email_sender_units", tags=["Email Sender Unit"])


@router.get("/", response_model=List[EmailSenderUnit])
def list_associations(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return EmailSenderUnitService.get_all(session)


@router.get("/{sender_id}/{cod_unit}", response_model=EmailSenderUnit)
def get_association(
    sender_id: str,
    cod_unit: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    assoc = EmailSenderUnitService.get_by_ids(
        sender_id,
        cod_unit,
        session
    )
    if not assoc:
        raise HTTPException(
            status_code=404,
            detail="Association not found"
        )
    return assoc


@router.post(
    "/",
    response_model=EmailSenderUnit,
    status_code=status.HTTP_201_CREATED
)
def create_association(
    data: EmailSenderUnitInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return EmailSenderUnitService.create(data, session)


@router.delete(
    "/{sender_id}/{cod_unit}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_association(
    sender_id: str,
    cod_unit: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = EmailSenderUnitService.delete(sender_id, cod_unit, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
