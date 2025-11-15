from sqlmodel import Session, select
from typing import List, Optional

from app.domain.models.email_sender_school import EmailSenderSchool


class EmailSenderSchoolRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[EmailSenderSchool]:
        return self.session.exec(select(EmailSenderSchool)).all()

    def get_by_ids(
        self,
        sender_id: str,
        cod_school: str
    ) -> Optional[EmailSenderSchool]:
        return self.session.get(EmailSenderSchool, (sender_id, cod_school))

    def create(self, assoc: EmailSenderSchool) -> EmailSenderSchool:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(self, sender_id: str, cod_school: str) -> bool:
        assoc = self.get_by_ids(sender_id, cod_school)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False
