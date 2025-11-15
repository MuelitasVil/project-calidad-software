from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.utils.auth import get_current_user
from app.domain.models.school import School
from app.domain.dtos.school.school_input import SchoolInput
from app.service.crud.school_service import SchoolService

router = APIRouter(prefix="/schools", tags=["Schools"])


@router.get("/", response_model=List[School])
def list_schools(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return SchoolService.get_all(session)


@router.get("/{cod_school}", response_model=School)
def get_school(
    cod_school: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    school = SchoolService.get_by_id(cod_school, session)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.post("/", response_model=School, status_code=status.HTTP_201_CREATED)
def create_school(
    data: SchoolInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return SchoolService.create(data, session)


@router.patch("/{cod_school}", response_model=School)
def update_school(
    cod_school: str,
    data: SchoolInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    updated = SchoolService.update(cod_school, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="School not found")
    return updated


@router.delete("/{cod_school}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(
    cod_school: str,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = SchoolService.delete(cod_school, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="School not found")
