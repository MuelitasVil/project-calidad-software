from sqlmodel import Session, select
from typing import List, Optional

from app.domain.models.type_user import TypeUser
from app.domain.dtos.type_user.type_user_input import TypeUserInput


class TypeUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[TypeUser]:
        return self.session.exec(select(TypeUser)).all()

    def get_by_id(self, type_user_id: str) -> Optional[TypeUser]:
        return self.session.get(TypeUser, type_user_id)

    def create(self, type_user: TypeUser) -> TypeUser:
        self.session.add(type_user)
        self.session.commit()
        self.session.refresh(type_user)
        return type_user

    def update(
        self,
        type_user_id: str,
        data: TypeUserInput
    ) -> Optional[TypeUser]:
        record = self.get_by_id(type_user_id)
        if not record:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def delete(self, type_user_id: str) -> bool:
        record = self.get_by_id(type_user_id)
        if record:
            self.session.delete(record)
            self.session.commit()
            return True
        return False
