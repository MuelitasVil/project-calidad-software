from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.unit_unal import UnitUnal
from app.domain.dtos.unit_unal.unit_unal_input import UnitUnalInput
from app.service.crud.unit_unal_service import UnitUnalService

router = APIRouter(prefix="/units_unal", tags=["Units UNAL"])


@router.get("/", response_model=List[UnitUnal])
def list_units(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return UnitUnalService.get_all(session)


@router.get("/{cod_unit}", response_model=UnitUnal)
def get_unit(
    cod_unit: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    unit = UnitUnalService.get_by_id(
        cod_unit,
        session
    )
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.post("/", response_model=UnitUnal, status_code=status.HTTP_201_CREATED)
def create_unit(
    data: UnitUnalInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return UnitUnalService.create(data, session)


@router.patch("/{cod_unit}", response_model=UnitUnal)
def update_unit(
    cod_unit: str,
    data: UnitUnalInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    updated = UnitUnalService.update(cod_unit, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Unit not found")
    return updated


@router.delete("/{cod_unit}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit(
    cod_unit: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = UnitUnalService.delete(cod_unit, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Unit not found")
