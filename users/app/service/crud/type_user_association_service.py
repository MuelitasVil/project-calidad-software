from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.type_user_association_repository import (
    TypeUserAssociationRepository
)
from app.domain.models.type_user_association import TypeUserAssociation
from app.domain.dtos.type_user_association.type_user_association_input import (
    TypeUserAssociationInput
)


class TypeUserAssociationService:
    @staticmethod
    def get_all(session: Session) -> List[TypeUserAssociation]:
        return TypeUserAssociationRepository(session).get_all()

    @staticmethod
    def get_by_ids(
        email_unal: str,
        type_user_id: str,
        cod_period: str,
        session: Session
    ) -> Optional[TypeUserAssociation]:
        return TypeUserAssociationRepository(session).get_by_ids(
            email_unal,
            type_user_id,
            cod_period
        )

    @staticmethod
    def create(
        input_data: TypeUserAssociationInput,
        session: Session
    ) -> TypeUserAssociation:
        assoc = TypeUserAssociation(**input_data.model_dump())
        return TypeUserAssociationRepository(session).create(assoc)

    @staticmethod
    def delete(
        email_unal: str,
        type_user_id: str,
        cod_period: str,
        session: Session
    ) -> bool:
        return TypeUserAssociationRepository(session).delete(
            email_unal,
            type_user_id,
            cod_period
            )
