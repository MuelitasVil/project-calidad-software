from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.user_unit_associate import UserUnitAssociate
from app.domain.dtos.user_unit_associate.user_unit_associate_input import (
    UserUnitAssociateInput
)
from app.service.crud.user_unit_associate_service import (
    UserUnitAssociateService,
)

router = APIRouter(
    prefix="/user_unit_associates",
    tags=["User Unit Associate"]
)


@router.get("/", response_model=List[UserUnitAssociate])
def list_associations(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return UserUnitAssociateService.get_all(session)


@router.get(
    "/{email_unal}/{cod_unit}/{cod_period}",
    response_model=UserUnitAssociate
)
def get_association(
    email_unal: str,
    cod_unit: str,
    cod_period: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    assoc = UserUnitAssociateService.get_by_ids(
        email_unal, cod_unit, cod_period, session
    )
    if not assoc:
        raise HTTPException(status_code=404, detail="Association not found")
    return assoc


@router.post(
    "/",
    response_model=UserUnitAssociate,
    status_code=status.HTTP_201_CREATED
)
def create_association(
    data: UserUnitAssociateInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return UserUnitAssociateService.create(data, session)


@router.delete(
    "/{email_unal}/{cod_unit}/{cod_period}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_association(
    email_unal: str,
    cod_unit: str,
    cod_period: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = UserUnitAssociateService.delete(
        email_unal, cod_unit, cod_period, session
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
