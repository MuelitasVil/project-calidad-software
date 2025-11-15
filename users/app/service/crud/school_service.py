from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.school_repository import SchoolRepository
from app.domain.models.school import School
from app.domain.dtos.school.school_input import SchoolInput


class SchoolService:
    @staticmethod
    def get_all(session: Session) -> List[School]:
        return SchoolRepository(session).get_all()

    @staticmethod
    def get_by_id(cod_school: str, session: Session) -> Optional[School]:
        return SchoolRepository(session).get_by_id(cod_school)

    @staticmethod
    def create(input_data: SchoolInput, session: Session) -> School:
        school = School(**input_data.model_dump(exclude_unset=True))
        return SchoolRepository(session).create(school)

    @staticmethod
    def update(
        cod_school: str,
        input_data: SchoolInput,
        session: Session
    ) -> Optional[School]:
        return SchoolRepository(session).update(cod_school, input_data)

    @staticmethod
    def save(input_data: SchoolInput, session: Session) -> School:
        if SchoolService.get_by_id(input_data.cod_school, session):
            return SchoolService.update(
                input_data.cod_school, input_data, session
            )
        return SchoolService.create(input_data, session)

    @staticmethod
    def delete(cod_school: str, session: Session) -> bool:
        return SchoolRepository(session).delete(cod_school)
    
    @staticmethod
    def bulk_insert_ignore(
        users: List[SchoolInput],
        session: Session
    ):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            School(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        SchoolRepository(session).bulk_insert_ignore(
            user_models
        )
        return {"inserted": len(users), "duplicates_ignored": True}
