from sqlmodel import Session, select
from app.domain.dtos.period.period_input import PeriodInput
from app.domain.models.period import Period
from typing import List, Optional


class PeriodRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Period]:
        return self.session.exec(select(Period)).all()

    def get_by_id(self, cod_period: str) -> Optional[Period]:
        return self.session.get(Period, cod_period)

    def create(self, period: Period) -> Period:
        self.session.add(period)
        self.session.commit()
        self.session.refresh(period)
        return period

    def delete(self, cod_period: str) -> bool:
        period = self.get_by_id(cod_period)
        if period:
            self.session.delete(period)
            self.session.commit()
            return True
        return False

    def update(self, cod_period: str, data: PeriodInput) -> Optional[Period]:
        period = self.get_by_id(cod_period)
        if not period:
            return None

        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(period, key, value)

        self.session.add(period)
        self.session.commit()
        self.session.refresh(period)
        return period
