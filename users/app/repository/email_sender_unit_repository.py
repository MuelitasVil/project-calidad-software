from sqlmodel import Session, select
from typing import List, Optional

from app.domain.models.email_sender_unit import EmailSenderUnit


class EmailSenderUnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[EmailSenderUnit]:
        return self.session.exec(select(EmailSenderUnit)).all()

    def get_by_ids(
        self,
        sender_id: str,
        cod_unit: str
    ) -> Optional[EmailSenderUnit]:
        return self.session.get(EmailSenderUnit, (sender_id, cod_unit))

    def create(self, assoc: EmailSenderUnit) -> EmailSenderUnit:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(self, sender_id: str, cod_unit: str) -> bool:
        assoc = self.get_by_ids(sender_id, cod_unit)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False
