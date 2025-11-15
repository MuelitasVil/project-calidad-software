from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.type_user_repository import TypeUserRepository
from app.domain.models.type_user import TypeUser
from app.domain.dtos.type_user.type_user_input import TypeUserInput


class TypeUserService:
    @staticmethod
    def get_all(session: Session) -> List[TypeUser]:
        return TypeUserRepository(session).get_all()

    @staticmethod
    def get_by_id(type_user_id: str, session: Session) -> Optional[TypeUser]:
        return TypeUserRepository(session).get_by_id(type_user_id)

    @staticmethod
    def create(input_data: TypeUserInput, session: Session) -> TypeUser:
        obj = TypeUser(**input_data.model_dump(exclude_unset=True))
        return TypeUserRepository(session).create(obj)

    @staticmethod
    def update(
        type_user_id: str,
        input_data: TypeUserInput,
        session: Session
    ) -> Optional[TypeUser]:
        return TypeUserRepository(session).update(type_user_id, input_data)

    @staticmethod
    def delete(type_user_id: str, session: Session) -> bool:
        return TypeUserRepository(session).delete(type_user_id)
