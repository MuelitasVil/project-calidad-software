from sqlmodel import Session, insert, select
from typing import List, Optional

from app.domain.models.user_unit_associate import UserUnitAssociate


class UserUnitAssociateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[UserUnitAssociate]:
        return self.session.exec(select(UserUnitAssociate)).all()

    def get_by_keys(
        self,
        email_unal: str,
        cod_unit: str,
        cod_period: str
    ) -> Optional[UserUnitAssociate]:
        return self.session.get(
            UserUnitAssociate,
            (email_unal, cod_unit, cod_period)
        )

    def create(self, assoc: UserUnitAssociate) -> UserUnitAssociate:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(self, email_unal: str, cod_unit: str, cod_period: str) -> bool:
        assoc = self.get_by_keys(email_unal, cod_unit, cod_period)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(self, userUnitAssocs: List[UserUnitAssociate]):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(UserUnitAssociate).values(
            [u.model_dump() for u in userUnitAssocs]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
