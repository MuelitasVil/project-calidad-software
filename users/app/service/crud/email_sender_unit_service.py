from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.email_sender_unit_repository import (
    EmailSenderUnitRepository
) 
from app.domain.models.email_sender_unit import EmailSenderUnit
from app.domain.dtos.email_sender_unit.email_sender_unit_input import (
    EmailSenderUnitInput
)


class EmailSenderUnitService:
    @staticmethod
    def get_all(session: Session) -> List[EmailSenderUnit]:
        return EmailSenderUnitRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        sender_id: str,
        cod_unit: str,
        session: Session
    ) -> Optional[EmailSenderUnit]:
        return EmailSenderUnitRepository(session).get_by_ids(
            sender_id, cod_unit
        )

    @staticmethod
    def create(
        input_data: EmailSenderUnitInput,
        session: Session
    ) -> EmailSenderUnit:
        assoc = EmailSenderUnit(**input_data.model_dump())
        return EmailSenderUnitRepository(session).create(assoc)

    @staticmethod
    def delete(sender_id: str, cod_unit: str, session: Session) -> bool:
        return EmailSenderUnitRepository(session).delete(sender_id, cod_unit)
