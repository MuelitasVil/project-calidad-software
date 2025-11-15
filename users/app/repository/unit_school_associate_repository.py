from sqlmodel import Session, insert, select
from typing import List, Optional

from app.domain.models.unit_school_associate import UnitSchoolAssociate


class UnitSchoolAssociateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[UnitSchoolAssociate]:
        return self.session.exec(select(UnitSchoolAssociate)).all()

    def get_by_ids(
        self,
        cod_unit: str,
        cod_school: str,
        cod_period: str
    ) -> Optional[UnitSchoolAssociate]:
        return self.session.get(
            UnitSchoolAssociate,
            (cod_unit, cod_school, cod_period)
        )

    def create(self, assoc: UnitSchoolAssociate) -> UnitSchoolAssociate:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(self, cod_unit: str, cod_school: str, cod_period: str) -> bool:
        assoc = self.get_by_ids(cod_unit, cod_school, cod_period)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(
        self, unitSchoolAssociate: List[UnitSchoolAssociate]
    ):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(UnitSchoolAssociate).values(
            [u.model_dump() for u in unitSchoolAssociate]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
