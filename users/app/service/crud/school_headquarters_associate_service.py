from sqlalchemy.orm import Session
from typing import List, Optional

from app.domain.dtos.headquarters.headquarters_input import HeadquartersInput
from app.domain.dtos.school.school_input import SchoolInput
from app.repository.school_headquarters_associate_repository import (
    SchoolHeadquartersAssociateRepository
)
from app.domain.models.school_headquarters_associate import (
    SchoolHeadquartersAssociate
)
from app.domain.dtos.school_headquarters_associate.school_headquarters_associate_input import (   # noqa: E501 ignora error flake8
    SchoolHeadquartersAssociateInput
)
from app.service.crud.headquarters_service import HeadquartersService
from app.service.crud.school_service import SchoolService


class SchoolHeadquartersAssociateService:
    @staticmethod
    def get_all(session: Session) -> List[SchoolHeadquartersAssociate]:
        return SchoolHeadquartersAssociateRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        cod_school: str,
        cod_headquarters: str,
        cod_period: str,
        session: Session
    ) -> Optional[SchoolHeadquartersAssociate]:
        return SchoolHeadquartersAssociateRepository(session).get_by_ids(
            cod_school,
            cod_headquarters,
            cod_period
        )

    @staticmethod
    def saveWithSchoolAndHeadquarters(
        schoolInput: SchoolInput,
        headquartersInput: HeadquartersInput,
        cod_period: str,
        session: Session
    ) -> SchoolHeadquartersAssociate:
        association = SchoolHeadquartersAssociate(
            schoolInput.cod_school,
            headquartersInput.cod_headquarters,
            cod_period=cod_period
        )

        if not (
            SchoolService.get_by_id(schoolInput.cod_school, session)
            and HeadquartersService.get_by_id(
                headquartersInput.cod_headquarters, session
            )
        ):
            return None

        if SchoolHeadquartersAssociateRepository(session).get_by_ids(
            association.cod_school,
            association.cod_headquarters,
            association.cod_period
        ):
            return None

        return SchoolHeadquartersAssociateRepository(session).create(
            association
        )

    @staticmethod
    def create(
        input_data: SchoolHeadquartersAssociateInput,
        session: Session
    ) -> SchoolHeadquartersAssociate:
        assoc = SchoolHeadquartersAssociate(**input_data.model_dump())
        return SchoolHeadquartersAssociateRepository(session).create(assoc)

    @staticmethod
    def delete(
        cod_school: str,
        cod_headquarter: str,
        cod_period: str,
        session: Session
    ) -> bool:
        return SchoolHeadquartersAssociateRepository(session).delete(
            cod_school,
            cod_headquarter,
            cod_period
        )

    @staticmethod
    def bulk_insert_ignore(
        users: List[SchoolHeadquartersAssociateInput],
        session: Session
    ):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            SchoolHeadquartersAssociate(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        SchoolHeadquartersAssociateRepository(session).bulk_insert_ignore(
            user_models
        )
        return {"inserted": len(users), "duplicates_ignored": True}
