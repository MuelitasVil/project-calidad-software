# app/controllers/period_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.domain.models.period import Period
from app.domain.dtos.period.period_input import PeriodInput
from app.service.crud.period_service import PeriodService
from app.utils.auth import get_current_user  # <--- autenticación
from app.utils.aws_sqs import send_message_to_sqs

router = APIRouter(prefix="/periods", tags=["Periods"])


@router.get("/", response_model=List[Period])
def list_periods(
    session: Session = Depends(get_session),
    ##user_email: str = Depends(get_current_user)
):
    message = {
        "event": "PERIOD_GET_LIST_ALL",
        "data": {
            "list": "all"
        }
    }
    ##send_message_to_sqs(message)
    return PeriodService.get_all(session)


@router.get("/{cod_period}", response_model=Period)
def get_period(
    cod_period: str,
    session: Session = Depends(get_session),
    ##user_email: str = Depends(get_current_user)
):
    period = PeriodService.get_by_id(cod_period, session)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    message = {
        "event": "PERIOD_GET_ONE",
        "data": {
            "cod_period": cod_period
        }
    }
    ##send_message_to_sqs(message)
    return period


@router.post("/", response_model=Period, status_code=status.HTTP_201_CREATED)
def create_period(
    data: PeriodInput,
    session: Session = Depends(get_session),
    ##user_email: str = Depends(get_current_user)
):
    period_created = PeriodService.create_period(data, session)

    message = {
        "event": "PERIOD_CREATED",
        "data": {
            "cod_period": period_created.cod_period,
            "description": getattr(period_created, "description", None),
        }
    }
    ##send_message_to_sqs(message)
    return period_created


@router.patch("/{cod_period}", response_model=Period)
def update_period(
    cod_period: str,
    data: PeriodInput,
    session: Session = Depends(get_session),
    ##user_email: str = Depends(get_current_user)
):
    updated = PeriodService.update_period(cod_period, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Period not found")
    
    message = {
        "event": "PERIOD_UPDATED",
        "data": {
            "cod_period": cod_period
        }
    }
    ##send_message_to_sqs(message)
    return updated


@router.delete("/{cod_period}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(
    cod_period: str,
    session: Session = Depends(get_session),
    ##user_email: str = Depends(get_current_user)
):
    deleted = PeriodService.delete_period(cod_period, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Period not found")
    message = {
        "event": "PERIOD_DELETED",
        "data": {
            "cod_period": cod_period
        }
    }
    ##send_message_to_sqs(message)
