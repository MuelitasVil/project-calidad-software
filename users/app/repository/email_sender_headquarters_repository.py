from sqlmodel import Session, select
from typing import List, Optional

from app.domain.models.email_sender_headquarters import EmailSenderHeadquarters


class EmailSenderHeadquartersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[EmailSenderHeadquarters]:
        return self.session.exec(select(EmailSenderHeadquarters)).all()

    def get_by_ids(
        self,
        sender_id: str,
        cod_headquarters: str
    ) -> Optional[EmailSenderHeadquarters]:
        return self.session.get(
            EmailSenderHeadquarters,
            (sender_id, cod_headquarters)
        )

    def create(
        self,
        assoc: EmailSenderHeadquarters
    ) -> EmailSenderHeadquarters:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(self, sender_id: str, cod_headquarters: str) -> bool:
        assoc = self.get_by_ids(sender_id, cod_headquarters)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False
