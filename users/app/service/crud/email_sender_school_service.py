from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.email_sender_school_repository import (
    EmailSenderSchoolRepository
) 

from app.domain.models.email_sender_school import EmailSenderSchool

from app.domain.dtos.email_sender_school.email_sender_school_input import (
    EmailSenderSchoolInput
)


class EmailSenderSchoolService:
    @staticmethod
    def get_all(session: Session) -> List[EmailSenderSchool]:
        return EmailSenderSchoolRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        sender_id: str,
        cod_school: str,
        session: Session
    ) -> Optional[
        EmailSenderSchool
    ]:
        return EmailSenderSchoolRepository(session).get_by_ids(
            sender_id, cod_school
        )

    @staticmethod
    def create(
        input_data: EmailSenderSchoolInput,
        session: Session
    ) -> EmailSenderSchool:
        assoc = EmailSenderSchool(**input_data.model_dump())
        return EmailSenderSchoolRepository(session).create(assoc)

    @staticmethod
    def delete(sender_id: str, cod_school: str, session: Session) -> bool:
        return EmailSenderSchoolRepository(session).delete(
            sender_id, cod_school
        )
