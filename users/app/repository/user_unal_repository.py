from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.dialects.mysql import insert

from app.domain.models.user_unal import UserUnal
from app.domain.dtos.user_unal.user_unal_input import UserUnalInput


class UserUnalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[UserUnal]:
        return self.session.exec(select(UserUnal)).all()

    def get_by_email(self, email_unal: str) -> Optional[UserUnal]:
        return self.session.get(UserUnal, email_unal)

    def create(self, user: UserUnal) -> UserUnal:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(
        self,
        email_unal: str,
        data: UserUnalInput
    ) -> Optional[UserUnal]:
        user = self.get_by_email(email_unal)
        if not user:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, email_unal: str) -> bool:
        user = self.get_by_email(email_unal)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(self, users: List[UserUnal]):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(UserUnal).values([u.model_dump() for u in users])
        stmt = stmt.prefix_with("IGNORE")
        self.session.execute(stmt)
        self.session.commit()
