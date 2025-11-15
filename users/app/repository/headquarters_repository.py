from sqlmodel import Session, insert, select
from typing import List, Optional

from app.domain.models.headquarters import Headquarters
from app.domain.dtos.headquarters.headquarters_input import HeadquartersInput


class HeadquartersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Headquarters]:
        return self.session.exec(select(Headquarters)).all()

    def get_by_id(self, cod_headquarters: str) -> Optional[Headquarters]:
        return self.session.get(Headquarters, cod_headquarters)

    def create(self, headquarters: Headquarters) -> Headquarters:
        self.session.add(headquarters)
        self.session.commit()
        self.session.refresh(headquarters)
        return headquarters

    def update(
        self,
        cod_headquarters: str,
        data: HeadquartersInput
    ) -> Optional[Headquarters]:
        hq = self.get_by_id(cod_headquarters)
        if not hq:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(hq, key, value)

        self.session.add(hq)
        self.session.commit()
        self.session.refresh(hq)
        return hq

    def delete(self, cod_headquarters: str) -> bool:
        hq = self.get_by_id(cod_headquarters)
        if hq:
            self.session.delete(hq)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(
        self, unitUnal: List[Headquarters]
    ):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(Headquarters).values(
            [u.model_dump() for u in unitUnal]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
