from sqlmodel import Session, select
from typing import List, Optional

from app.domain.models.type_user_association import TypeUserAssociation


class TypeUserAssociationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[TypeUserAssociation]:
        return self.session.exec(select(TypeUserAssociation)).all()

    def get_by_ids(
            self,
            email_unal: str,
            type_user_id: str,
            cod_period: str
    ) -> Optional[TypeUserAssociation]:
        return self.session.get(
            TypeUserAssociation,
            (email_unal, type_user_id, cod_period)
        )

    def create(self, assoc: TypeUserAssociation) -> TypeUserAssociation:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(
            self,
            email_unal: str,
            type_user_id: str,
            cod_period: str
    ) -> bool:
        assoc = self.get_by_ids(email_unal, type_user_id, cod_period)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False
