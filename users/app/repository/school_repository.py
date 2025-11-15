from sqlmodel import Session, insert, select
from typing import List, Optional

from app.domain.models.school import School
from app.domain.dtos.school.school_input import SchoolInput


class SchoolRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[School]:
        return self.session.exec(select(School)).all()

    def get_by_id(self, cod_school: str) -> Optional[School]:
        return self.session.get(School, cod_school)

    def create(self, school: School) -> School:
        self.session.add(school)
        self.session.commit()
        self.session.refresh(school)
        return school

    def update(self, cod_school: str, data: SchoolInput) -> Optional[School]:
        school = self.get_by_id(cod_school)
        if not school:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(school, key, value)

        self.session.add(school)
        self.session.commit()
        self.session.refresh(school)
        return school

    def delete(self, cod_school: str) -> bool:
        school = self.get_by_id(cod_school)
        if school:
            self.session.delete(school)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(
        self, unitUnal: List[School]
    ):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(School).values(
            [u.model_dump() for u in unitUnal]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
