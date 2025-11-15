from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.email_sender import EmailSender
from app.domain.dtos.email_sender.email_sender_input import EmailSenderInput
from app.service.crud.email_sender_service import EmailSenderService

router = APIRouter(prefix="/email_senders", tags=["Email Senders"])


@router.get("/", response_model=List[EmailSender])
def list_email_senders(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return EmailSenderService.get_all(session)


@router.get("/{id}", response_model=EmailSender)
def get_email_sender(
    id: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    sender = EmailSenderService.get_by_id(id, session)
    if not sender:
        raise HTTPException(status_code=404, detail="Email sender not found")
    return sender


@router.post(
    "/",
    response_model=EmailSender,
    status_code=status.HTTP_201_CREATED
)
def create_email_sender(
    data: EmailSenderInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return EmailSenderService.create(data, session)


@router.patch("/{id}", response_model=EmailSender)
def update_email_sender(
    id: str,
    data: EmailSenderInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    updated = EmailSenderService.update(id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Email sender not found")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email_sender(
    id: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = EmailSenderService.delete(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Email sender not found")
