from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.email_sender_repository import EmailSenderRepository
from app.domain.models.email_sender import EmailSender
from app.domain.dtos.email_sender.email_sender_input import EmailSenderInput


class EmailSenderService:
    @staticmethod
    def get_all(session: Session) -> List[EmailSender]:
        return EmailSenderRepository(session).get_all()

    @staticmethod
    def get_by_id(id: str, session: Session) -> Optional[EmailSender]:
        return EmailSenderRepository(session).get_by_id(id)

    @staticmethod
    def create(input_data: EmailSenderInput, session: Session) -> EmailSender:
        sender = EmailSender(**input_data.model_dump(exclude_unset=True))
        return EmailSenderRepository(session).create(sender)

    @staticmethod
    def update(
        id: str,
        input_data: EmailSenderInput,
        session: Session
    ) -> Optional[EmailSender]:
        return EmailSenderRepository(session).update(id, input_data)

    @staticmethod
    def delete(id: str, session: Session) -> bool:
        return EmailSenderRepository(session).delete(id)
