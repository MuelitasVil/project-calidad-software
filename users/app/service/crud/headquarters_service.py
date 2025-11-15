from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.headquarters_repository import HeadquartersRepository
from app.domain.models.headquarters import Headquarters
from app.domain.dtos.headquarters.headquarters_input import HeadquartersInput


class HeadquartersService:
    @staticmethod
    def get_all(session: Session) -> List[Headquarters]:
        return HeadquartersRepository(session).get_all()

    @staticmethod
    def get_by_id(
        cod_headquarters: str,
        session: Session
    ) -> Optional[Headquarters]:
        return HeadquartersRepository(session).get_by_id(
            cod_headquarters
        )

    @staticmethod
    def create(
        input_data: HeadquartersInput,
        session: Session
    ) -> Headquarters:
        hq = Headquarters(**input_data.model_dump(exclude_unset=True))
        return HeadquartersRepository(session).create(hq)

    @staticmethod
    def update(
        cod_headquarters: str,
        input_data: HeadquartersInput,
        session: Session
    ) -> Optional[Headquarters]:
        return HeadquartersRepository(session).update(
            cod_headquarters,
            input_data
        )

    @staticmethod
    def save(input_data: HeadquartersInput, session: Session) -> Headquarters:
        if HeadquartersService.get_by_id(input_data.cod_headquarters, session):
            return HeadquartersService.update(
                input_data.cod_headquarters, input_data, session
            )
        return HeadquartersService.create(input_data, session)

    @staticmethod
    def delete(cod_headquarters: str, session: Session) -> bool:
        return HeadquartersRepository(session).delete(cod_headquarters)

    @staticmethod
    def bulk_insert_ignore(
        users: List[HeadquartersInput],
        session: Session
    ):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            Headquarters(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        HeadquartersRepository(session).bulk_insert_ignore(
            user_models
        )
        return {"inserted": len(users), "duplicates_ignored": True}
