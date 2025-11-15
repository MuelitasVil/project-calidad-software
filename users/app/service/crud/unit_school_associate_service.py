from sqlalchemy.orm import Session
from typing import List, Optional

from app.domain.dtos.school.school_input import SchoolInput
from app.domain.dtos.unit_unal.unit_unal_input import UnitUnalInput
from app.repository.unit_school_associate_repository import (
    UnitSchoolAssociateRepository,
)
from app.domain.models.unit_school_associate import UnitSchoolAssociate
from app.domain.dtos.unit_school_associate.unit_school_associate_input import (
    UnitSchoolAssociateInput
)
from app.service.crud.school_service import SchoolService
from app.service.crud.unit_unal_service import UnitUnalService


class UnitSchoolAssociateService:
    @staticmethod
    def get_all(session: Session) -> List[UnitSchoolAssociate]:
        return UnitSchoolAssociateRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        cod_unit: str,
        cod_school: str,
        cod_period: str,
        session: Session
    ) -> Optional[UnitSchoolAssociate]:
        return UnitSchoolAssociateRepository(session).get_by_ids(
            cod_unit, cod_school, cod_period
        )

    @staticmethod
    def saveWithUnitAndSchool(
        unitInput: UnitUnalInput,
        schoolInput: SchoolInput,
        cod_period: str,
        session: Session
    ) -> UnitSchoolAssociate:
        association = UnitSchoolAssociate(
            unitInput.cod_unit,
            schoolInput.cod_school,
            cod_period=cod_period
        )

        if not (
            UnitUnalService.get_by_id(unitInput.cod_unit, session)
            and SchoolService.get_by_id(schoolInput.cod_school, session)
        ):
            return None

        if UnitSchoolAssociateRepository(session).get_by_ids(
            association.cod_unit,
            association.cod_school,
            association.cod_period
        ):
            return None

        return UnitSchoolAssociateRepository(session).create(association)

    @staticmethod
    def create(
        input_data: UnitSchoolAssociateInput,
        session: Session
    ) -> UnitSchoolAssociate:
        assoc = UnitSchoolAssociate(**input_data.model_dump())
        return UnitSchoolAssociateRepository(session).create(assoc)

    @staticmethod
    def delete(
        cod_unit: str,
        cod_school: str,
        cod_period: str,
        session: Session
    ) -> bool:
        return UnitSchoolAssociateRepository(session).delete(
            cod_unit,
            cod_school,
            cod_period
        )
    
    @staticmethod
    def bulk_insert_ignore(
        users: List[UnitSchoolAssociateInput],
        session: Session
    ):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            UnitSchoolAssociate(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        UnitSchoolAssociateRepository(session).bulk_insert_ignore(user_models)
        return {"inserted": len(users), "duplicates_ignored": True}
