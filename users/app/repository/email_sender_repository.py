from sqlmodel import Session, select
from typing import List, Optional

from app.domain.models.email_sender import EmailSender


class EmailSenderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[EmailSender]:
        return self.session.exec(select(EmailSender)).all()

    def get_by_id(self, id: str) -> Optional[EmailSender]:
        return self.session.get(EmailSender, id)

    def get_by_email(self, email: str) -> Optional[EmailSender]:
        return self.session.exec(
            select(EmailSender).where(EmailSender.email == email)
        ).first()

    def create(self, sender: EmailSender) -> EmailSender:
        self.session.add(sender)
        self.session.commit()
        self.session.refresh(sender)
        return sender

    def update(self, id: str, data: EmailSender) -> Optional[EmailSender]:
        sender = self.get_by_id(id)
        if not sender:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(sender, key, value)

        self.session.add(sender)
        self.session.commit()
        self.session.refresh(sender)
        return sender

    def delete(self, id: str) -> bool:
        sender = self.get_by_id(id)
        if sender:
            self.session.delete(sender)
            self.session.commit()
            return True
        return False
