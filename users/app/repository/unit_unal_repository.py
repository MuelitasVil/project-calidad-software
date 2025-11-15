from sqlmodel import Session, insert, select
from typing import List, Optional

from app.domain.models.unit_unal import UnitUnal
from app.domain.dtos.unit_unal.unit_unal_input import UnitUnalInput


class UnitUnalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[UnitUnal]:
        return self.session.exec(select(UnitUnal)).all()

    def get_by_id(self, cod_unit: str) -> Optional[UnitUnal]:
        return self.session.get(UnitUnal, cod_unit)

    def create(self, unit: UnitUnal) -> UnitUnal:
        self.session.add(unit)
        self.session.commit()
        self.session.refresh(unit)
        return unit

    def update(self, cod_unit: str, data: UnitUnalInput) -> Optional[UnitUnal]:
        unit = self.get_by_id(cod_unit)
        if not unit:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(unit, key, value)

        self.session.add(unit)
        self.session.commit()
        self.session.refresh(unit)
        return unit

    def delete(self, cod_unit: str) -> bool:
        unit = self.get_by_id(cod_unit)
        if unit:
            self.session.delete(unit)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(
        self, unitUnal: List[UnitUnal]
    ):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(UnitUnal).values(
            [u.model_dump() for u in unitUnal]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
