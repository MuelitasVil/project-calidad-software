from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.school_headquarters_associate import (
    SchoolHeadquartersAssociate
)
from app.domain.dtos.school_headquarters_associate.school_headquarters_associate_input import (  # noqa: E501 ignora error flake8
    SchoolHeadquartersAssociateInput
)
from app.service.crud.school_headquarters_associate_service import (
    SchoolHeadquartersAssociateService
)

router = APIRouter(
    prefix="/school_headquarters_associates",
    tags=["School Headquarters Associate"]
)


@router.get("/", response_model=List[SchoolHeadquartersAssociate])
def list_associations(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return SchoolHeadquartersAssociateService.get_all(session)


@router.get("/{cod_school}/{cod_headquarters}/{cod_period}",
            response_model=SchoolHeadquartersAssociate)
def get_association(
    cod_school: str,
    cod_headquarters: str,
    cod_period: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    assoc = SchoolHeadquartersAssociateService.get_by_ids(
        cod_school,
        cod_headquarters,
        cod_period,
        session
    )
    if not assoc:
        raise HTTPException(status_code=404, detail="Association not found")
    return assoc


@router.post(
    "/", 
    response_model=SchoolHeadquartersAssociate,
    status_code=status.HTTP_201_CREATED
)
def create_association(
    data: SchoolHeadquartersAssociateInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return SchoolHeadquartersAssociateService.create(data, session)


@router.delete(
    "/{cod_school}/{cod_headquarters}/{cod_period}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_association(
    cod_school: str,
    cod_headquarters: str,
    cod_period: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = SchoolHeadquartersAssociateService.delete(
        cod_school,
        cod_headquarters,
        cod_period,
        session
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
