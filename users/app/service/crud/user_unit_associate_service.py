from sqlalchemy.orm import Session
from typing import List, Optional

from app.domain.dtos.unit_unal.unit_unal_input import UnitUnalInput
from app.domain.dtos.user_unal.user_unal_input import UserUnalInput
from app.repository.user_unit_associate_repository import (
    UserUnitAssociateRepository,
)
from app.domain.models.user_unit_associate import UserUnitAssociate
from app.domain.dtos.user_unit_associate.user_unit_associate_input import (
    UserUnitAssociateInput
)
from app.service.crud.unit_unal_service import UnitUnalService
from app.service.crud.user_unal_service import UserUnalService


class UserUnitAssociateService:
    @staticmethod
    def get_all(session: Session) -> List[UserUnitAssociate]:
        return UserUnitAssociateRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        email_unal: str,
        cod_unit: str,
        cod_period: str,
        session: Session
    ) -> Optional[UserUnitAssociate]:
        return UserUnitAssociateRepository(session).get_by_keys(
            email_unal,
            cod_unit,
            cod_period
        )

    @staticmethod
    def saveWithUserAndUnit(
        userInput: UserUnalInput,
        unitInput: UnitUnalInput,
        cod_period: str,
        session: Session
    ) -> UserUnitAssociate:
        association = UserUnitAssociate(
            userInput.email_unal,
            unitInput.cod_unit,
            cod_period=cod_period
        )
        if not (
            UserUnalService.get_by_email(userInput.email_unal, session)
            and UnitUnalService.get_by_id(unitInput.cod_unit, session)
        ):
            return None

        if UserUnitAssociateRepository(session).exists(association):
            return None

        return UserUnitAssociateRepository(session).create(association)

    @staticmethod
    def create(
        input_data: UserUnitAssociateInput,
        session: Session
    ) -> UserUnitAssociate:
        association = UserUnitAssociate(**input_data.model_dump())
        return UserUnitAssociateRepository(session).create(association)

    @staticmethod
    def delete(
        email_unal: str,
        cod_unit: str,
        cod_period: str,
        session: Session
    ) -> bool:
        return UserUnitAssociateRepository(session).delete(
            email_unal,
            cod_unit,
            cod_period
        )

    @staticmethod
    def bulk_insert_ignore(
        users: List[UserUnitAssociateInput],
        session: Session
    ):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            UserUnitAssociate(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        UserUnitAssociateRepository(session).bulk_insert_ignore(user_models)
        return {"inserted": len(users), "duplicates_ignored": True}
