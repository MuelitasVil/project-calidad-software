from typing import List, Optional
from sqlmodel import Session, select

from app.domain.models.user_contact_data import UserContactData
from app.domain.dtos.user_contact_data.user_contact_data_input import UserContactDataInput
from app.domain.dtos.user_contact_data.user_contact_data_update import UserContactDataUpdate


class UserContactDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[UserContactData]:
        return self.session.exec(select(UserContactData)).all()

    def get_by_id(self, contact_id: int) -> Optional[UserContactData]:
        return self.session.get(UserContactData, contact_id)

    def get_by_user_email(self, email_unal: str) -> List[UserContactData]:
        statement = select(UserContactData).where(UserContactData.email_unal == email_unal)
        return self.session.exec(statement).all()

    def create(self, contact_data: UserContactData) -> UserContactData:
        self.session.add(contact_data)
        self.session.commit()
        self.session.refresh(contact_data)
        return contact_data

    def update(
        self,
        contact_id: int,
        data: UserContactDataUpdate
    ) -> Optional[UserContactData]:
        contact = self.get_by_id(contact_id)
        if not contact:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(contact, key, value)

        self.session.add(contact)
        self.session.commit()
        self.session.refresh(contact)
        return contact

    def delete(self, contact_id: int) -> bool:
        contact = self.get_by_id(contact_id)
        if contact:
            self.session.delete(contact)
            self.session.commit()
            return True
        return False
