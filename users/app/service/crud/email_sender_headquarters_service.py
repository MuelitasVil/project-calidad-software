from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.email_sender_headquarters_repository import ( 
    EmailSenderHeadquartersRepository
)
from app.domain.models.email_sender_headquarters import EmailSenderHeadquarters
from app.domain.dtos.email_sender_headquarters.email_sender_headquarters_input import (  # noqa: E501 ignora error flake8
    EmailSenderHeadquartersInput
)


class EmailSenderHeadquartersService:
    @staticmethod
    def get_all(session: Session) -> List[EmailSenderHeadquarters]:
        return EmailSenderHeadquartersRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        sender_id: str,
        cod_headquarters: str,
        session: Session
    ) -> Optional[EmailSenderHeadquarters]:
        return EmailSenderHeadquartersRepository(session).get_by_ids(
            sender_id, cod_headquarters
        )

    @staticmethod
    def create(
        input_data: EmailSenderHeadquartersInput,
        session: Session
    ) -> EmailSenderHeadquarters:
        assoc = EmailSenderHeadquarters(**input_data.model_dump())
        return EmailSenderHeadquartersRepository(session).create(assoc)

    @staticmethod
    def delete(
        sender_id: str,
        cod_headquarters: str,
        session: Session
    ) -> bool:
        return EmailSenderHeadquartersRepository(session).delete(
            sender_id, cod_headquarters
        )
