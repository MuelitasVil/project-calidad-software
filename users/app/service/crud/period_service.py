from app.domain.dtos.period.period_input import PeriodInput
from app.domain.models.period import Period
from app.repository.period_repository import PeriodRepository
from sqlalchemy.orm import Session
from typing import List, Optional


class PeriodService:
    @staticmethod
    def get_all(session: Session) -> List[Period]:
        repo = PeriodRepository(session)
        return repo.get_all()

    @staticmethod
    def get_by_id(cod_period: str, session: Session) -> Optional[Period]:
        repo = PeriodRepository(session)
        return repo.get_by_id(cod_period)

    @staticmethod
    def create_period(input_period: PeriodInput, session: Session) -> Period:
        repo = PeriodRepository(session)
        period = Period(**input_period.model_dump(exclude_unset=True))
        return repo.create(period)

    @staticmethod
    def update_period(
        cod_period: str,
        input_period: PeriodInput,
        session: Session
    ) -> Optional[Period]:
        repo = PeriodRepository(session)
        return repo.update(cod_period, input_period)

    @staticmethod
    def delete_period(cod_period: str, session: Session) -> bool:
        repo = PeriodRepository(session)
        return repo.delete(cod_period)
